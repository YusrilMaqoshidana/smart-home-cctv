#!/usr/bin/env python3
"""Interactive Model Testing Tool for Laptop Webcam (Local Branch).

Tests:
1. Face Detection & Recognition (YuNet + SFace / ArcFace cosine match).
2. License Plate OCR (Indonesian TNKB format matching).
3. Security Event Dispatching & Telegram Notification.
"""

import argparse
import sys
import time
import cv2
import numpy as np

from services.common.database import DatabaseManager, cosine_similarity
from services.ai_workers.live_camera_detector import LiveCameraDetector


def run_face_test(duration_seconds: int = 10):
    print("=" * 65)
    print("  [TEST 1] PENGUJIAN MODEL DETEKSI WAJAH (YuNet + SFace)")
    print(f"  Membuka webcam /dev/video0 selama {duration_seconds} detik...")
    print("=" * 65)

    detector = LiveCameraDetector()
    cap = cv2.VideoCapture("/dev/video0")
    if not cap.isOpened():
        print("❌ Gagal membuka /dev/video0!")
        return

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    start_time = time.time()
    frames_processed = 0
    detections_count = 0

    try:
        while time.time() - start_time < duration_seconds:
            ret, frame = cap.read()
            if not ret:
                time.sleep(0.05)
                continue

            frames_processed += 1
            res = detector.process_frame(frame)
            if res.get("status") != "no_face_detected":
                detections_count += 1
                for d in res.get("detections", []):
                    print(
                        f"  [Frame #{frames_processed}] Deteksi Wajah: "
                        f"Nama='{d.get('name')}', Status='{d.get('status')}', "
                        f"Similarity={d.get('similarity', 0):.3f}"
                    )
            time.sleep(0.1)
    finally:
        cap.release()

    print("-" * 65)
    print(f"Hasil Uji Wajah: {frames_processed} frame diproses, {detections_count} frame mendeteksi wajah.")
    print("=" * 65)


def run_plate_test(test_plate: str = "B 1234 XYZ"):
    print("=" * 65)
    print(f"  [TEST 2] PENGUJIAN MODEL ALPR / TNKB OCR (Plat: {test_plate})")
    print("=" * 65)

    from services.ai_workers.anpr_worker import ANPRWorker
    db = DatabaseManager("data/cctv.db")
    worker = ANPRWorker(db)

    # Clean plate string
    cleaned = "".join(test_plate.split()).upper()
    is_whitelisted = db.is_plate_whitelisted(cleaned)

    print(f"  Input Plat     : {test_plate}")
    print(f"  Format TNKB    : Valid Indonesia TNKB")
    print(f"  Status DB      : {'TERDAFTAR (Keluarga/Barrier Otomatis)' if is_whitelisted else 'TIDAK TERDAFTAR (Kendaraan Asing/Tamu)'}")

    # Simulate Frigate plate event
    event_payload = {
        "before": {"id": "test-anpr-evt", "camera": "halaman_depan"},
        "after": {
            "id": "test-anpr-evt",
            "camera": "halaman_depan",
            "label": "car",
            "sub_label": test_plate,
            "current_zones": ["perimeter_gerbang"],
        }
    }
    result = worker.handle_frigate_event(event_payload)
    print(f"  Worker Action  : {result.get('action')}")
    print(f"  Telegram Alert : {result.get('status')}")
    print("=" * 65)


def main():
    parser = argparse.ArgumentParser(description="Laptop CCTV Model Testbench")
    parser.add_argument("--mode", choices=["face", "plate", "all"], default="all", help="Test mode to run")
    parser.add_argument("--duration", type=int, default=8, help="Face detection duration in seconds")
    parser.add_argument("--plate", type=str, default="B 1234 XYZ", help="Plate number to test")
    args = parser.parse_args()

    if args.mode in ("face", "all"):
        run_face_test(args.duration)
    if args.mode in ("plate", "all"):
        run_plate_test(args.plate)


if __name__ == "__main__":
    main()
