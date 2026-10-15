"""Test suite for Phase 4: Event Dispatcher and Telegram Bot Gateway."""

import math
import os
import tempfile
import unittest

from services.common.database import DatabaseManager
from services.ai_workers.face_worker import FaceWorker
from services.ai_workers.anpr_worker import ANPRWorker
from services.dispatcher.event_dispatcher import EventDispatcher
from services.dispatcher.telegram_gateway import TelegramGateway


class TestPhase4DispatcherTelegram(unittest.TestCase):
    """Test expectations for Event Dispatcher, cooldown debounce, and Telegram payload formatting."""

    def setUp(self):
        """Set up test environment with seeded database and workers."""
        self.temp_dir = tempfile.TemporaryDirectory()
        self.db_path = os.path.join(self.temp_dir.name, "test_dispatcher.db")
        self.db = DatabaseManager(self.db_path)

        # Seed family face
        dim = 512
        self.vec_ayah = [1.0 / math.sqrt(dim)] * dim
        self.db.add_face("Ayah", "resident", self.vec_ayah)

        # Seed family car
        self.db.add_plate("B 1234 XYZ", "Avanza Ayah", vehicle_type="car", is_family=True)

        self.face_worker = FaceWorker(self.db)
        self.anpr_worker = ANPRWorker(self.db)
        self.tg_gateway = TelegramGateway(bot_token="mock_token", chat_id="123456")
        self.dispatcher = EventDispatcher(
            db=self.db,
            face_worker=self.face_worker,
            anpr_worker=self.anpr_worker,
            telegram_gateway=self.tg_gateway,
            cooldown_seconds=180,
        )

    def tearDown(self):
        """Clean up test resources."""
        self.db.close()
        self.temp_dir.cleanup()

    def test_family_person_event_suppressed(self):
        """Verify resident face detection suppresses emergency alert and logs status."""
        frigate_event = {
            "type": "update",
            "after": {
                "id": "event-101",
                "camera": "halaman_depan",
                "label": "person",
                "top_score": 0.89,
                "current_zones": ["perimeter_gerbang"],
            },
        }

        # Dispatch with Ayah's face embedding
        action = self.dispatcher.handle_frigate_event(frigate_event, face_embedding=self.vec_ayah)
        self.assertEqual(action["action"], "suppressed")
        self.assertEqual(action["reason"], "resident_detected")
        self.assertEqual(action["name"], "Ayah")

        # Verify event logged in DB
        logs = self.db.list_events()
        self.assertEqual(len(logs), 1)
        self.assertEqual(logs[0]["status"], "family_suppressed")

    def test_unknown_loitering_triggers_emergency_alert(self):
        """Verify unknown person loitering > 45s generates emergency Telegram payload."""
        vec_unknown = [0.0] * 512
        vec_unknown[0] = 1.0

        frigate_event = {
            "type": "update",
            "after": {
                "id": "event-102",
                "camera": "halaman_depan",
                "label": "person",
                "top_score": 0.85,
                "current_zones": ["perimeter_gerbang"],
            },
        }

        # 50 seconds dwell time -> loitering
        action = self.dispatcher.handle_frigate_event(
            frigate_event, face_embedding=vec_unknown, dwell_time_seconds=50.0
        )
        self.assertEqual(action["action"], "alert_sent")
        self.assertEqual(action["alert_level"], "emergency")
        self.assertIn("Loitering", action["message"])

        # Check Telegram payload format
        payload = action["telegram_payload"]
        self.assertIn("🔴", payload["caption"])
        self.assertIn("Halaman Depan", payload["caption"])
        self.assertIn("inline_keyboard", payload["reply_markup"])

    def test_foreign_vehicle_triggers_warning_alert(self):
        """Verify foreign vehicle plate detection generates warning Telegram payload."""
        frigate_event = {
            "type": "update",
            "after": {
                "id": "event-103",
                "camera": "carport",
                "label": "car",
                "top_score": 0.92,
                "current_zones": ["area_parkir"],
            },
        }

        action = self.dispatcher.handle_frigate_event(
            frigate_event, raw_plate_text="B 9999 NON"
        )
        self.assertEqual(action["action"], "alert_sent")
        self.assertEqual(action["alert_level"], "warning")
        self.assertIn("B 9999 NON", action["message"])

        payload = action["telegram_payload"]
        self.assertIn("🚗", payload["caption"])
        self.assertIn("B 9999 NON", payload["caption"])

    def test_event_cooldown_prevents_alert_spam(self):
        """Verify same object event within cooldown window is skipped."""
        vec_unknown = [0.0] * 512
        vec_unknown[0] = 1.0

        event_a = {
            "type": "update",
            "after": {
                "id": "event-104",
                "camera": "halaman_depan",
                "label": "person",
                "top_score": 0.85,
                "current_zones": ["perimeter_gerbang"],
            },
        }

        # First alert fires
        act_1 = self.dispatcher.handle_frigate_event(
            event_a, face_embedding=vec_unknown, dwell_time_seconds=50.0
        )
        self.assertEqual(act_1["action"], "alert_sent")

        # Second alert immediately after with same object/camera should be debounced
        act_2 = self.dispatcher.handle_frigate_event(
            event_a, face_embedding=vec_unknown, dwell_time_seconds=55.0
        )
        self.assertEqual(act_2["action"], "cooldown_debounced")


if __name__ == "__main__":
    unittest.main()
