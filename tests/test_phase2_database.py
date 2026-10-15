"""Test suite for Phase 2: Database initialization, Face Vector Whitelist, and Indonesian TNKB Plate Validation."""

import math
import os
import tempfile
import unittest

from services.common.database import DatabaseManager


class TestPhase2Database(unittest.TestCase):
    """Test expectations for Phase 2 Database & Whitelist Manager."""

    def setUp(self):
        """Set up a fresh temporary SQLite database for testing."""
        self.temp_dir = tempfile.TemporaryDirectory()
        self.db_path = os.path.join(self.temp_dir.name, "test_cctv.db")
        self.db = DatabaseManager(self.db_path)

    def tearDown(self):
        """Clean up the temporary directory."""
        self.db.close()
        self.temp_dir.cleanup()

    def test_database_initialization(self):
        """Verify tables (faces, plates, event_logs) are created properly."""
        tables = self.db.get_table_names()
        self.assertIn("faces", tables)
        self.assertIn("plates", tables)
        self.assertIn("event_logs", tables)

    def test_face_whitelist_crud_and_cosine_matching(self):
        """Verify adding face embeddings and matching by cosine similarity."""
        # Create dummy 512-d normalized vectors
        dim = 512
        vec_ayah = [1.0 / math.sqrt(dim)] * dim
        vec_ibu = [-1.0 / math.sqrt(dim)] * dim

        # Add Ayah (Resident)
        face_id = self.db.add_face(
            name="Ayah",
            role="resident",
            embedding=vec_ayah,
        )
        self.assertGreater(face_id, 0)

        # Query matching with exact same vector -> similarity should be ~1.0 >= 0.68
        match, similarity = self.db.find_matching_face(vec_ayah, threshold=0.68)
        self.assertIsNotNone(match)
        self.assertEqual(match["name"], "Ayah")
        self.assertEqual(match["role"], "resident")
        self.assertAlmostEqual(similarity, 1.0, places=3)

        # Query matching with opposite vector -> similarity should be -1.0 < 0.68
        match_none, sim_low = self.db.find_matching_face(vec_ibu, threshold=0.68)
        self.assertIsNone(match_none)
        self.assertLess(sim_low, 0.68)

        # List faces
        faces = self.db.list_faces()
        self.assertEqual(len(faces), 1)

        # Delete face
        deleted = self.db.delete_face(face_id)
        self.assertTrue(deleted)
        self.assertEqual(len(self.db.list_faces()), 0)

    def test_plate_whitelist_crud_and_tnkb_validation(self):
        """Verify plate registration with Indonesian TNKB regex validation."""
        # Valid plate numbers
        valid_plates = [
            ("B 1234 XYZ", "Avanza Hitam Ayah", "car", True),
            ("D 8888 ZZ", "Vespa Merah Ibu", "motorcycle", True),
            ("L 1029 XY", "Mobil Tamu", "car", False),
        ]
        for plate_str, label, v_type, is_fam in valid_plates:
            plate_id = self.db.add_plate(
                plate_number=plate_str,
                owner_label=label,
                vehicle_type=v_type,
                is_family=is_fam,
            )
            self.assertGreater(plate_id, 0, f"Failed to add valid plate {plate_str}")

        # Invalid plate numbers must raise ValueError
        invalid_plates = ["1234", "ABCDEFG", "XYZ 123456", "B 12345678 AA"]
        for invalid in invalid_plates:
            with self.assertRaises(ValueError, msg=f"Should reject invalid plate {invalid}"):
                self.db.add_plate(plate_number=invalid, owner_label="Invalid")

        # Test plate lookup (case and space insensitive)
        matched_plate = self.db.find_plate("b1234xyz")
        self.assertIsNotNone(matched_plate)
        self.assertEqual(matched_plate["owner_label"], "Avanza Hitam Ayah")
        self.assertTrue(matched_plate["is_family"])

        unknown_plate = self.db.find_plate("B 9999 NON")
        self.assertIsNone(unknown_plate)

    def test_event_logging(self):
        """Verify inserting and querying event logs."""
        self.db.log_event(
            event_id="1729000000.123456-abc123",
            camera="halaman_depan",
            label="person",
            sub_label="Ayah",
            confidence=0.88,
            zone="perimeter_gerbang",
            status="family_suppressed",
            snapshot_path="/media/frigate/clips/1729000000.jpg",
        )
        logs = self.db.list_events(limit=10)
        self.assertEqual(len(logs), 1)
        self.assertEqual(logs[0]["sub_label"], "Ayah")
        self.assertEqual(logs[0]["status"], "family_suppressed")


if __name__ == "__main__":
    unittest.main()
