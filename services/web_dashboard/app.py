"""Dashboard REST API Application for Face Whitelist, Indonesian Plates, and Live Monitoring."""

import json
import re
from typing import Any, Dict, Optional, Tuple
from services.common.database import DatabaseManager


class DashboardAPIApp:
    """REST API Application for managing Smart Home CCTV whitelist and monitoring events."""

    def __init__(self, db: DatabaseManager):
        """Initialize with DatabaseManager instance.

        Args:
            db: DatabaseManager instance.
        """
        self.db = db

    def handle_request(
        self,
        method: str,
        path: str,
        payload: Optional[Dict[str, Any]] = None,
    ) -> Tuple[int, Dict[str, Any]]:
        """Dispatch API requests to corresponding handlers.

        Args:
            method: HTTP method ('GET', 'POST', 'DELETE').
            path: Request URI path.
            payload: Optional JSON dictionary payload for POST/PUT.

        Returns:
            Tuple of (HTTP_status_code, response_dict).
        """
        method = method.upper()

        # ----------------------------------------------------------------------
        # 1. Health & Server Status
        # ----------------------------------------------------------------------
        if method == "GET" and path == "/api/status":
            return 200, {
                "status": "healthy",
                "server": "Lenovo ThinkCentre M70q",
                "cpu": "Intel Core i7-9700T (8C/8T)",
                "ram_total": "32 GB",
                "storage_quota_cctv": "300 GB NVMe",
                "cameras": ["halaman_depan", "carport"],
                "hwaccel": "Intel UHD 630 (QuickSync/VAAPI)",
            }

        # ----------------------------------------------------------------------
        # 2. Face Whitelist API
        # ----------------------------------------------------------------------
        if path == "/api/faces":
            if method == "GET":
                return 200, {"faces": self.db.list_faces()}

            if method == "POST":
                if not payload or "name" not in payload or "embedding" not in payload:
                    return 400, {"success": False, "error": "Missing 'name' or 'embedding'"}

                face_id = self.db.add_face(
                    name=payload["name"],
                    role=payload.get("role", "resident"),
                    embedding=payload["embedding"],
                )
                return 201, {"success": True, "id": face_id}

        # Match /api/faces/<id>
        face_del_match = re.match(r"^/api/faces/(\d+)$", path)
        if face_del_match and method == "DELETE":
            f_id = int(face_del_match.group(1))
            deleted = self.db.delete_face(f_id)
            return (200, {"success": True}) if deleted else (404, {"success": False, "error": "Face not found"})

        # ----------------------------------------------------------------------
        # 3. Plate Whitelist API (Indonesian TNKB)
        # ----------------------------------------------------------------------
        if path == "/api/plates":
            if method == "GET":
                return 200, {"plates": self.db.list_plates()}

            if method == "POST":
                if not payload or "plate_number" not in payload or "owner_label" not in payload:
                    return 400, {"success": False, "error": "Missing 'plate_number' or 'owner_label'"}

                try:
                    plate_id = self.db.add_plate(
                        plate_number=payload["plate_number"],
                        owner_label=payload["owner_label"],
                        vehicle_type=payload.get("vehicle_type", "car"),
                        is_family=payload.get("is_family", True),
                    )
                    return 201, {"success": True, "id": plate_id}
                except ValueError as err:
                    return 400, {"success": False, "error": str(err)}

        # Match /api/plates/<id>
        plate_del_match = re.match(r"^/api/plates/(\d+)$", path)
        if plate_del_match and method == "DELETE":
            p_id = int(plate_del_match.group(1))
            deleted = self.db.delete_plate(p_id)
            return (200, {"success": True}) if deleted else (404, {"success": False, "error": "Plate not found"})

        # ----------------------------------------------------------------------
        # 4. Event Logs API
        # ----------------------------------------------------------------------
        if method == "GET" and path == "/api/events":
            return 200, {"events": self.db.list_events(limit=50)}

        return 404, {"success": False, "error": f"Endpoint not found: {method} {path}"}

    def __call__(self, environ: Dict[str, Any], start_response: Any) -> Any:
        """WSGI entry point for web servers."""
        method = environ.get("REQUEST_METHOD", "GET")
        path = environ.get("PATH_INFO", "/")

        payload = None
        if method in ("POST", "PUT", "PATCH"):
            try:
                content_len = int(environ.get("CONTENT_LENGTH", 0))
                body = environ["wsgi.input"].read(content_len)
                payload = json.loads(body.decode("utf-8")) if body else {}
            except (ValueError, KeyError):
                payload = {}

        status_code, res_dict = self.handle_request(method, path, payload)
        status_text = {200: "200 OK", 201: "201 Created", 400: "400 Bad Request", 404: "404 Not Found"}.get(
            status_code, f"{status_code} Status"
        )
        response_body = json.dumps(res_dict).encode("utf-8")
        headers = [
            ("Content-Type", "application/json; charset=utf-8"),
            ("Content-Length", str(len(response_body))),
            ("Access-Control-Allow-Origin", "*"),
        ]
        start_response(status_text, headers)
        return [response_body]
