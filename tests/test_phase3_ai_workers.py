"""Test suite for Phase 3: AI Workers (Face Recognition, Indonesian ANPR, and Audio Modular Add-on)."""

import math
import os
import tempfile
import unittest

from services.common.database import DatabaseManager
from services.ai_workers.face_worker import FaceWorker
from services.ai_workers.anpr_worker import ANPRWorker
from services.ai_workers.audio_worker import AudioWorker


class TestPhase3AIWorkers(unittest.TestCase):
    """Test expectations for FaceWorker, ANPRWorker, and AudioWorker."""

    def setUp(self):
        """Set up test database and worker instances."""
        self.temp_dir = tempfile.TemporaryDirectory()
        self.db_path = os.path.join(self.temp_dir.name, "test_ai.db")
        self.db = DatabaseManager(self.db_path)

        # Seed face whitelist
        dim = 512
        self.vec_ayah = [1.0 / math.sqrt(dim)] * dim
        self.db.add_face("Ayah", "resident", self.vec_ayah)

        # Seed plate whitelist
        self.db.add_plate("B 1234 XYZ", "Mobil Avanza Ayah", vehicle_type="car", is_family=True)

        self.face_worker = FaceWorker(self.db)
        self.anpr_worker = ANPRWorker(self.db)

    def tearDown(self):
        """Clean up test resources."""
        self.db.close()
        self.temp_dir.cleanup()

    def test_face_worker_resident_and_unknown_loitering(self):
        """Verify face worker matches residents and detects loitering for unknown faces."""
        # 1. Matching Resident
        result_resident = self.face_worker.classify_face(self.vec_ayah, dwell_time_seconds=10)
        self.assertEqual(result_resident["status"], "resident")
        self.assertEqual(result_resident["name"], "Ayah")
        self.assertFalse(result_resident["is_loitering"])

        # 2. Unknown Face (short dwell time -> not loitering)
        vec_unknown = [0.0] * 512
        vec_unknown[0] = 1.0
        result_unknown_short = self.face_worker.classify_face(vec_unknown, dwell_time_seconds=20)
        self.assertEqual(result_unknown_short["status"], "unknown")
        self.assertFalse(result_unknown_short["is_loitering"])

        # 3. Unknown Face (dwell time > 45s -> loitering alert)
        result_unknown_loitering = self.face_worker.classify_face(vec_unknown, dwell_time_seconds=50)
        self.assertEqual(result_unknown_loitering["status"], "unknown")
        self.assertTrue(result_unknown_loitering["is_loitering"])

    def test_anpr_worker_family_and_foreign_vehicles(self):
        """Verify ANPR worker correctly classifies registered family vs unknown foreign vehicles."""
        # 1. Family car with slightly messy OCR spacing
        res_family = self.anpr_worker.process_plate_text("b-1234-xyz")
        self.assertEqual(res_family["status"], "family_vehicle")
        self.assertEqual(res_family["display_plate"], "B 1234 XYZ")
        self.assertTrue(res_family["is_family"])
        self.assertEqual(res_family["owner_label"], "Mobil Avanza Ayah")

        # 2. Foreign car with valid Indonesian TNKB
        res_foreign = self.anpr_worker.process_plate_text("D 5678 EFG")
        self.assertEqual(res_foreign["status"], "foreign_vehicle")
        self.assertEqual(res_foreign["display_plate"], "D 5678 EFG")
        self.assertFalse(res_foreign["is_family"])

        # 3. Garbage / Non-plate OCR text
        res_invalid = self.anpr_worker.process_plate_text("GARBAGE12345")
        self.assertEqual(res_invalid["status"], "invalid_plate")
        self.assertIsNone(res_invalid["display_plate"])

    def test_audio_worker_modular_toggle_and_graceful_fallback(self):
        """Verify audio worker graceful degradation when disabled via feature flag."""
        # 1. When audio module is disabled
        audio_disabled = AudioWorker(enabled=False)
        self.assertFalse(audio_disabled.is_enabled())
        res_disabled = audio_disabled.process_audio_sample(b"mock_audio_bytes")
        self.assertEqual(res_disabled["status"], "disabled")
        self.assertIsNone(res_disabled["detected_intent"])

        # 2. When audio module is enabled
        audio_enabled = AudioWorker(enabled=True)
        self.assertTrue(audio_enabled.is_enabled())

        # Test guest greeting keyword
        res_salam = audio_enabled.process_transcript("assalamualaikum pak")
        self.assertEqual(res_salam["status"], "detected")
        self.assertEqual(res_salam["detected_intent"], "guest_greeting")

        # Test courier keyword
        res_paket = audio_enabled.process_transcript("ada paket permisi")
        self.assertEqual(res_paket["status"], "detected")
        self.assertEqual(res_paket["detected_intent"], "courier_arrival")

        # Test emergency keyword
        res_tolong = audio_enabled.process_transcript("tolong ada maling")
        self.assertEqual(res_tolong["status"], "detected")
        self.assertEqual(res_tolong["detected_intent"], "emergency_alert")


if __name__ == "__main__":
    unittest.main()
