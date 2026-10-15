"""Test suite for Phase 5: REST API endpoints and End-to-End Simulation Pipeline."""

import json
import math
import os
import tempfile
import unittest

from services.common.database import DatabaseManager
from services.ai_workers.face_worker import FaceWorker
from services.ai_workers.anpr_worker import ANPRWorker
from services.dispatcher.event_dispatcher import EventDispatcher
from services.dispatcher.telegram_gateway import TelegramGateway
from services.web_dashboard.app import DashboardAPIApp


class TestPhase5APIAndE2E(unittest.TestCase):
    """Test expectations for Web Dashboard REST API and End-to-End surveillance flow."""

    def setUp(self):
        """Set up test environment."""
        self.temp_dir = tempfile.TemporaryDirectory()
        self.db_path = os.path.join(self.temp_dir.name, "test_api_e2e.db")
        self.db = DatabaseManager(self.db_path)

        self.face_worker = FaceWorker(self.db)
        self.anpr_worker = ANPRWorker(self.db)
        self.tg_gateway = TelegramGateway(bot_token="test_token", chat_id="99999")
        self.dispatcher = EventDispatcher(
            db=self.db,
            face_worker=self.face_worker,
            anpr_worker=self.anpr_worker,
            telegram_gateway=self.tg_gateway,
            cooldown_seconds=180,
        )
        self.app = DashboardAPIApp(self.db)

    def tearDown(self):
        """Clean up test resources."""
        self.db.close()
        self.temp_dir.cleanup()

    def test_api_status_endpoint(self):
        """Verify GET /api/status returns system health and camera list."""
        status_code, data = self.app.handle_request("GET", "/api/status")
        self.assertEqual(status_code, 200)
        self.assertEqual(data["status"], "healthy")
        self.assertIn("halaman_depan", data["cameras"])
        self.assertIn("carport", data["cameras"])
        self.assertEqual(data["server"], "Lenovo ThinkCentre M70q")

    def test_api_faces_crud(self):
        """Verify REST API face whitelist endpoints (GET, POST, DELETE)."""
        dim = 512
        vec = [1.0 / math.sqrt(dim)] * dim

        # POST /api/faces
        post_code, post_res = self.app.handle_request(
            "POST",
            "/api/faces",
            payload={"name": "Kakak", "role": "resident", "embedding": vec},
        )
        self.assertEqual(post_code, 201)
        self.assertTrue(post_res["success"])
        face_id = post_res["id"]

        # GET /api/faces
        get_code, get_res = self.app.handle_request("GET", "/api/faces")
        self.assertEqual(get_code, 200)
        self.assertEqual(len(get_res["faces"]), 1)
        self.assertEqual(get_res["faces"][0]["name"], "Kakak")

        # DELETE /api/faces/<id>
        del_code, del_res = self.app.handle_request("DELETE", f"/api/faces/{face_id}")
        self.assertEqual(del_code, 200)
        self.assertTrue(del_res["success"])

        # Check empty
        _, list_after = self.app.handle_request("GET", "/api/faces")
        self.assertEqual(len(list_after["faces"]), 0)

    def test_api_plates_crud_and_tnkb_validation(self):
        """Verify REST API plate whitelist endpoints with validation."""
        # Valid plate
        code_valid, res_valid = self.app.handle_request(
            "POST",
            "/api/plates",
            payload={
                "plate_number": "B 1234 ABC",
                "owner_label": "Mobil Kakak",
                "vehicle_type": "car",
                "is_family": True,
            },
        )
        self.assertEqual(code_valid, 201)
        self.assertTrue(res_valid["success"])

        # Invalid plate format must return 400 Bad Request
        code_bad, res_bad = self.app.handle_request(
            "POST",
            "/api/plates",
            payload={"plate_number": "INVALID999", "owner_label": "Test"},
        )
        self.assertEqual(code_bad, 400)
        self.assertFalse(res_bad["success"])

        # GET /api/plates
        get_code, get_res = self.app.handle_request("GET", "/api/plates")
        self.assertEqual(get_code, 200)
        self.assertEqual(len(get_res["plates"]), 1)
        self.assertEqual(get_res["plates"][0]["display_plate"], "B 1234 ABC")

    def test_end_to_end_surveillance_flow(self):
        """Verify full end-to-end pipeline: Registration -> Frigate Event -> Dispatcher -> DB Log -> API."""
        dim = 512
        vec_ibu = [1.0 / math.sqrt(dim)] * dim

        # Step 1: Admin registers Ibu's face and family motorcycle via API
        self.app.handle_request(
            "POST",
            "/api/faces",
            payload={"name": "Ibu", "role": "resident", "embedding": vec_ibu},
        )
        self.app.handle_request(
            "POST",
            "/api/plates",
            payload={
                "plate_number": "D 1234 AB",
                "owner_label": "Scoopy Merah Ibu",
                "vehicle_type": "motorcycle",
                "is_family": True,
            },
        )

        # Step 2: Ibu walks past front yard -> Suppressed (no false alarm)
        event_person = {
            "type": "update",
            "after": {
                "id": "e2e-event-1",
                "camera": "halaman_depan",
                "label": "person",
                "top_score": 0.91,
                "current_zones": ["perimeter_gerbang"],
            },
        }
        res_person = self.dispatcher.handle_frigate_event(event_person, face_embedding=vec_ibu)
        self.assertEqual(res_person["action"], "suppressed")
        self.assertEqual(res_person["name"], "Ibu")

        # Step 3: Ibu drives motorcycle into carport -> Family vehicle recognized
        event_motor = {
            "type": "update",
            "after": {
                "id": "e2e-event-2",
                "camera": "carport",
                "label": "motorcycle",
                "top_score": 0.95,
                "current_zones": ["area_parkir"],
            },
        }
        res_motor = self.dispatcher.handle_frigate_event(
            event_motor, raw_plate_text="D 1234 AB"
        )
        self.assertEqual(res_motor["action"], "suppressed")
        self.assertEqual(res_motor["reason"], "family_vehicle")

        # Step 4: Unknown car stops at carport -> Emergency/warning alert sent
        event_foreign = {
            "type": "update",
            "after": {
                "id": "e2e-event-3",
                "camera": "carport",
                "label": "car",
                "top_score": 0.88,
                "current_zones": ["area_parkir"],
            },
        }
        res_foreign = self.dispatcher.handle_frigate_event(
            event_foreign, raw_plate_text="B 7777 ZZZ"
        )
        self.assertEqual(res_foreign["action"], "alert_sent")
        self.assertEqual(res_foreign["alert_level"], "warning")

        # Step 5: Verify all events appear in Dashboard API GET /api/events
        code_events, data_events = self.app.handle_request("GET", "/api/events")
        self.assertEqual(code_events, 200)
        events = data_events["events"]
        self.assertEqual(len(events), 3)
        # Most recent first
        self.assertEqual(events[0]["id"], "e2e-event-3")
        self.assertEqual(events[0]["status"], "foreign_vehicle")
        self.assertEqual(events[1]["id"], "e2e-event-2")
        self.assertEqual(events[2]["id"], "e2e-event-1")


if __name__ == "__main__":
    unittest.main()
