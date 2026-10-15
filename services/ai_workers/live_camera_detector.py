"""Live Camera Detector: Uses YuNet & SFace models to detect faces from laptop webcam in real-time, matches with DatabaseManager whitelist, sends alerts to Telegram, and updates event logs."""

import os
import sys
import time
import cv2
import numpy as np

from services.common.database import DatabaseManager, cosine_similarity
from services.dispatcher.telegram_gateway import TelegramGateway

YUNET_MODEL = "data/models/face_detection_yunet_2023mar.onnx"
SFACE_MODEL = "data/models/face_recognition_sface_2021dec.onnx"


class LiveCameraDetector:
    """Detects and recognizes faces in real-time from webcam or RTSP stream."""

    def __init__(self, db_path: str = "data/cctv.db"):
        self.db = DatabaseManager(db_path)
        self.bot_token = os.getenv("TELEGRAM_BOT_TOKEN", "8851351486:AAEcPB7rZYmA1SX1gcEKITpiqouHzFd77vg")
        self.chat_id = os.getenv("TELEGRAM_CHAT_ID", "-1003933666444")
        self.telegram = TelegramGateway(self.bot_token, self.chat_id)

        # Initialize YuNet Detector
        self.detector = cv2.FaceDetectorYN_create(
            model=YUNET_MODEL,
            config="",
            input_size=(1280, 720),
            score_threshold=0.6,
            nms_threshold=0.3,
            top_k=5
        )

        # Initialize SFace Recognizer
        self.recognizer = cv2.FaceRecognizerSF_create(
            model=SFACE_MODEL,
            config=""
        )

        self.last_alert_time = 0.0
        self.cooldown_seconds = 30.0  # 30s debounce for local live test

    def process_frame(self, frame: np.ndarray) -> dict:
        """Run face detection and recognition on a single image frame."""
        h, w, _ = frame.shape
        self.detector.setInputSize((w, h))

        # 1. Detect faces
        _, faces = self.detector.detect(frame)
        if faces is None or len(faces) == 0:
            return {"status": "no_face_detected", "faces_count": 0}

        results = []
        for face_info in faces:
            bbox = face_info[0:4].astype(int)
            x, y, bw, bh = bbox
            conf = float(face_info[-1])

            # 2. Align and extract feature embedding
            aligned_face = self.recognizer.alignCrop(frame, face_info)
            feature = self.recognizer.feature(aligned_face)
            embedding_list = feature.flatten().tolist()

            # 3. Match against Whitelist in Database
            match, sim = self.db.find_matching_face(embedding_list, threshold=0.36)

            is_family = False
            person_name = "Orang Tidak Dikenal"
            status = "unknown_loitering"

            if match:
                is_family = (match.get("role") == "resident")
                person_name = match.get("name", "Penghuni")
                status = "family_suppressed" if is_family else "guest_detected"

            # Draw bounding box and label on snapshot
            color = (0, 255, 0) if is_family else (0, 0, 255)
            cv2.rectangle(frame, (x, y), (x + bw, y + bh), color, 2)
            cv2.putText(
                frame,
                f"{person_name} ({sim:.2f})",
                (x, max(y - 10, 20)),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                color,
                2
            )

            # Save snapshot
            os.makedirs("data/snapshots", exist_ok=True)
            snapshot_path = f"data/snapshots/face_{int(time.time())}.jpg"
            cv2.imwrite(snapshot_path, frame)

            # Log to DB
            event_id = f"evt_{int(time.time() * 1000)}"
            self.db.log_event(
                event_id=event_id,
                camera="halaman_depan",
                label="person",
                sub_label=person_name,
                confidence=conf,
                zone="perimeter_gerbang",
                status=status,
                snapshot_path=snapshot_path
            )

            # Send Telegram alert if unregistered and cooldown passed
            now = time.time()
            if not is_family and (now - self.last_alert_time > self.cooldown_seconds):
                self.last_alert_time = now
                caption = (
                    f"🔴 *Terdeteksi Wajah Tidak Dikenal!*\n"
                    f"📍 *Kamera*: Halaman Depan (Webcam Laptop)\n"
                    f"⏱️ *Skor Deteksi*: {conf:.2%}\n"
                    f"📝 _Wajah ini belum terdaftar di whitelist keluarga._"
                )
                self.send_telegram_photo(snapshot_path, caption)

            results.append({
                "name": person_name,
                "confidence": conf,
                "similarity": sim,
                "is_family": is_family,
                "status": status,
                "bbox": [x, y, bw, bh],
                "snapshot": snapshot_path
            })

        return {"status": "detected", "faces_count": len(results), "detections": results}

    def send_telegram_photo(self, photo_path: str, caption: str):
        """Send snapshot photo to Telegram group."""
        import requests
        url = f"https://api.telegram.org/bot{self.bot_token}/sendPhoto"
        try:
            with open(photo_path, "rb") as f:
                requests.post(
                    url,
                    data={"chat_id": self.chat_id, "caption": caption, "parse_mode": "Markdown"},
                    files={"photo": f},
                    timeout=5
                )
        except Exception as e:
            print("Telegram alert error:", e)


def run_live_test_single_shot(source="rtsp://localhost:8554/halaman_depan"):
    """Grab a frame from RTSP stream (or webcam) and run detection."""
    # Ensure RTSP transport is TCP
    os.environ["OPENCV_FFMPEG_CAPTURE_OPTIONS"] = "rtsp_transport;tcp"
    cap = cv2.VideoCapture(source)
    if not cap.isOpened():
        print(f"Notice: Could not open {source}, falling back to /dev/video0...")
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print("Error: Could not open webcam /dev/video0")
            return None

    ret, frame = cap.read()
    cap.release()

    if not ret or frame is None:
        print("Error: Could not read frame from video stream")
        return None

    detector = LiveCameraDetector()
    result = detector.process_frame(frame)
    print("Detection Result:", result)
    return result


if __name__ == "__main__":
    run_live_test_single_shot()
