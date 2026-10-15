"""Face Worker for InsightFace embedding extraction, matching, and loitering detection."""

from typing import Any, Dict, List, Optional
from services.common.database import DatabaseManager


class FaceWorker:
    """Handles face recognition matching and loitering anomaly detection."""

    def __init__(self, db: DatabaseManager, similarity_threshold: float = 0.68):
        """Initialize FaceWorker.

        Args:
            db: DatabaseManager instance with whitelist records.
            similarity_threshold: Cosine similarity cutoff for recognition (default 0.68).
        """
        self.db = db
        self.similarity_threshold = similarity_threshold

    def classify_face(
        self,
        embedding: List[float],
        dwell_time_seconds: float = 0.0,
    ) -> Dict[str, Any]:
        """Classify a face embedding into resident, guest, or unknown loiterer.

        Args:
            embedding: 512-d normalized face embedding vector.
            dwell_time_seconds: Time the person has spent inside the perimeter.

        Returns:
            Dictionary containing match status, name, role, and loitering flag.
        """
        match, similarity = self.db.find_matching_face(
            embedding, threshold=self.similarity_threshold
        )

        if match:
            role = match.get("role", "resident")
            return {
                "status": role,
                "name": match.get("name"),
                "similarity": similarity,
                "is_loitering": False,
                "suppress_alert": (role == "resident"),
            }

        # Unknown person
        is_loitering = dwell_time_seconds >= 45.0
        return {
            "status": "unknown",
            "name": None,
            "similarity": similarity,
            "is_loitering": is_loitering,
            "suppress_alert": False,
        }
