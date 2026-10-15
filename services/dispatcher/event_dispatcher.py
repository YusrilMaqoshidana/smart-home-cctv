"""Event Dispatcher: Consumes Frigate events, coordinates AI workers, applies cooldowns, and routes alerts."""

import time
from typing import Any, Dict, List, Optional
from services.common.database import DatabaseManager
from services.ai_workers.face_worker import FaceWorker
from services.ai_workers.anpr_worker import ANPRWorker
from services.dispatcher.telegram_gateway import TelegramGateway


class EventDispatcher:
    """Processes detection events, enforces debounce cooldowns, and dispatches Telegram notifications."""

    def __init__(
        self,
        db: DatabaseManager,
        face_worker: FaceWorker,
        anpr_worker: ANPRWorker,
        telegram_gateway: TelegramGateway,
        cooldown_seconds: int = 180,
    ):
        """Initialize EventDispatcher.

        Args:
            db: DatabaseManager instance for event logging.
            face_worker: FaceWorker instance.
            anpr_worker: ANPRWorker instance.
            telegram_gateway: TelegramGateway instance.
            cooldown_seconds: Minimum seconds before repeating an alert for the same camera/object.
        """
        self.db = db
        self.face_worker = face_worker
        self.anpr_worker = anpr_worker
        self.telegram_gateway = telegram_gateway
        self.cooldown_seconds = cooldown_seconds
        self._cooldown_cache: Dict[str, float] = {}

    def _is_cooling_down(self, key: str) -> bool:
        """Check if an alert key is within active cooldown window."""
        now = time.time()
        last_time = self._cooldown_cache.get(key, 0.0)
        if now - last_time < self.cooldown_seconds:
            return True
        self._cooldown_cache[key] = now
        return False

    def handle_frigate_event(
        self,
        frigate_event: Dict[str, Any],
        face_embedding: Optional[List[float]] = None,
        raw_plate_text: Optional[str] = None,
        dwell_time_seconds: float = 0.0,
        snapshot_path: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Process incoming Frigate detection event dictionary.

        Args:
            frigate_event: Dictionary with keys 'type' and 'after' (Frigate MQTT schema).
            face_embedding: Optional 512-d face vector from snapshot crop.
            raw_plate_text: Optional vehicle plate text from OCR.
            dwell_time_seconds: Seconds object has remained in zone.
            snapshot_path: Path to snapshot file.

        Returns:
            Dictionary describing dispatched action.
        """
        after = frigate_event.get("after", {})
        event_id = after.get("id", "unknown_event")
        camera = after.get("camera", "unknown_camera")
        label = after.get("label", "unknown_label")
        confidence = after.get("top_score", 0.0)
        zones = after.get("current_zones", [])
        primary_zone = zones[0] if zones else None

        # ----------------------------------------------------------------------
        # 1. Person Detection Flow
        # ----------------------------------------------------------------------
        if label == "person":
            if face_embedding:
                face_result = self.face_worker.classify_face(
                    face_embedding, dwell_time_seconds=dwell_time_seconds
                )
            else:
                face_result = {
                    "status": "unknown",
                    "name": None,
                    "is_loitering": (dwell_time_seconds >= 45.0),
                    "suppress_alert": False,
                }

            # A. Resident recognized -> suppress alarm
            if face_result.get("suppress_alert"):
                self.db.log_event(
                    event_id=event_id,
                    camera=camera,
                    label="person",
                    sub_label=face_result.get("name"),
                    confidence=confidence,
                    zone=primary_zone,
                    status="family_suppressed",
                    snapshot_path=snapshot_path,
                )
                return {
                    "action": "suppressed",
                    "reason": "resident_detected",
                    "name": face_result.get("name"),
                }

            # B. Unknown person loitering (> 45s) -> Emergency Alert
            if face_result.get("is_loitering"):
                cooldown_key = f"{camera}:loitering:{event_id}"
                if self._is_cooling_down(cooldown_key):
                    return {"action": "cooldown_debounced"}

                msg_title = "Terdeteksi Orang Mencurigakan (Loitering)"
                msg_desc = (
                    f"Orang tidak dikenal berdiam di area perimeter "
                    f"selama lebih dari {int(dwell_time_seconds)} detik."
                )
                tg_payload = self.telegram_gateway.build_alert_payload(
                    camera=camera,
                    title=msg_title,
                    description=msg_desc,
                    alert_level="emergency",
                    photo_path=snapshot_path,
                    event_id=event_id,
                )

                self.db.log_event(
                    event_id=event_id,
                    camera=camera,
                    label="person",
                    sub_label="Unknown Loiterer",
                    confidence=confidence,
                    zone=primary_zone,
                    status="unknown_loitering",
                    snapshot_path=snapshot_path,
                )

                return {
                    "action": "alert_sent",
                    "alert_level": "emergency",
                    "message": msg_title,
                    "telegram_payload": tg_payload,
                }

            # C. Transient unknown person (not yet loitering)
            return {"action": "monitoring", "status": "unknown_transient"}

        # ----------------------------------------------------------------------
        # 2. Vehicle Detection Flow (Car / Motorcycle)
        # ----------------------------------------------------------------------
        if label in ("car", "motorcycle"):
            anpr_result = (
                self.anpr_worker.process_plate_text(raw_plate_text)
                if raw_plate_text
                else {"status": "unreadable", "is_family": False}
            )

            if anpr_result.get("is_family"):
                self.db.log_event(
                    event_id=event_id,
                    camera=camera,
                    label=label,
                    sub_label=anpr_result.get("owner_label"),
                    confidence=confidence,
                    zone=primary_zone,
                    status="family_vehicle",
                    snapshot_path=snapshot_path,
                )
                return {
                    "action": "suppressed",
                    "reason": "family_vehicle",
                    "plate": anpr_result.get("display_plate"),
                }

            # Foreign vehicle detected
            plate_display = anpr_result.get("display_plate") or "Plat Tidak Terbaca"
            cooldown_key = f"{camera}:vehicle:{plate_display}"
            if self._is_cooling_down(cooldown_key):
                return {"action": "cooldown_debounced"}

            msg_title = "Kendaraan Asing Terdeteksi"
            msg_desc = f"Terdeteksi kendaraan ({label.upper()}) dengan nomor polisi: {plate_display}."
            tg_payload = self.telegram_gateway.build_alert_payload(
                camera=camera,
                title=f"🚗 {msg_title}",
                description=msg_desc,
                alert_level="warning",
                photo_path=snapshot_path,
                event_id=event_id,
            )

            self.db.log_event(
                event_id=event_id,
                camera=camera,
                label=label,
                sub_label=plate_display,
                confidence=confidence,
                zone=primary_zone,
                status="foreign_vehicle",
                snapshot_path=snapshot_path,
            )

            return {
                "action": "alert_sent",
                "alert_level": "warning",
                "message": f"Kendaraan Asing: {plate_display}",
                "telegram_payload": tg_payload,
            }

        return {"action": "ignored", "reason": "untracked_label"}
