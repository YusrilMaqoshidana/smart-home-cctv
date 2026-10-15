"""Indonesian ANPR/LPR Worker for TNKB plate detection and whitelist verification."""

from typing import Any, Dict, Optional
from services.common.database import DatabaseManager, normalize_tnkb_plate


class ANPRWorker:
    """Handles Indonesian TNKB vehicle plate parsing and whitelist matching."""

    def __init__(self, db: DatabaseManager):
        """Initialize ANPRWorker.

        Args:
            db: DatabaseManager instance with vehicle whitelist.
        """
        self.db = db

    def process_plate_text(self, raw_plate_text: str) -> Dict[str, Any]:
        """Validate and classify Indonesian plate text against the whitelist.

        Args:
            raw_plate_text: Extracted text from plate OCR.

        Returns:
            Classification dictionary with plate number, family status, and owner.
        """
        try:
            norm_plate, display_plate = normalize_tnkb_plate(raw_plate_text)
        except ValueError:
            return {
                "status": "invalid_plate",
                "normalized_plate": None,
                "display_plate": None,
                "is_family": False,
                "owner_label": None,
            }

        plate_record = self.db.find_plate(norm_plate)
        if plate_record:
            return {
                "status": "family_vehicle" if plate_record["is_family"] else "registered_guest",
                "normalized_plate": norm_plate,
                "display_plate": display_plate,
                "is_family": plate_record["is_family"],
                "owner_label": plate_record["owner_label"],
            }

        return {
            "status": "foreign_vehicle",
            "normalized_plate": norm_plate,
            "display_plate": display_plate,
            "is_family": False,
            "owner_label": "Kendaraan Asing",
        }
