"""Database Manager for Face Whitelist, Indonesian TNKB Plate Registry, and Event Logs."""

import datetime
import json
import math
import os
import re
import sqlite3
from typing import Any, Dict, List, Optional, Tuple

# Indonesian TNKB format: 1-2 letters, 1-4 numbers, 1-3 letters
TNKB_REGEX = re.compile(r"^([A-Z]{1,2})\s*([0-9]{1,4})\s*([A-Z]{1,3})$")


def normalize_tnkb_plate(raw_plate: str) -> Tuple[str, str]:
    """Validate and normalize Indonesian TNKB plate number.

    Args:
        raw_plate: Raw plate text (e.g., "b 1234 xyz" or "B-1234-XYZ").

    Returns:
        Tuple of (normalized_no_space, display_formatted), e.g. ("B1234XYZ", "B 1234 XYZ").

    Raises:
        ValueError: If plate format does not match TNKB pattern.
    """
    cleaned = raw_plate.upper().strip().replace("-", " ")
    match = TNKB_REGEX.match(cleaned)
    if not match:
        raise ValueError(
            f"Invalid Indonesian TNKB plate format: '{raw_plate}'. "
            "Expected format e.g. 'B 1234 XYZ' or 'D 8888 ZZ'."
        )

    prefix, number, suffix = match.groups()
    normalized = f"{prefix}{number}{suffix}"
    display = f"{prefix} {number} {suffix}"
    return normalized, display


def cosine_similarity(vec_a: List[float], vec_b: List[float]) -> float:
    """Calculate cosine similarity between two vector lists."""
    if len(vec_a) != len(vec_b) or not vec_a:
        return 0.0

    dot_product = sum(a * b for a, b in zip(vec_a, vec_b))
    norm_a = math.sqrt(sum(a * a for a in vec_a))
    norm_b = math.sqrt(sum(b * b for b in vec_b))

    if norm_a == 0.0 or norm_b == 0.0:
        return 0.0

    return dot_product / (norm_a * norm_b)


class DatabaseManager:
    """Manages SQLite storage for faces, vehicles, and events."""

    def __init__(self, db_path: str):
        """Initialize database connection and schema.

        Args:
            db_path: Path to SQLite database file.
        """
        self.db_path = db_path
        os.makedirs(os.path.dirname(os.path.abspath(db_path)), exist_ok=True)
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self._init_schema()

    def _init_schema(self) -> None:
        """Create necessary tables if they do not exist."""
        cursor = self.conn.cursor()

        # 1. Faces Whitelist Table
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS faces (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                role TEXT NOT NULL DEFAULT 'resident',
                embedding TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                expire_at TIMESTAMP NULL
            )
            """
        )

        # 2. Plates Whitelist Table
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS plates (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                plate_number TEXT NOT NULL UNIQUE,
                display_plate TEXT NOT NULL,
                owner_label TEXT NOT NULL,
                vehicle_type TEXT NOT NULL DEFAULT 'car',
                is_family INTEGER NOT NULL DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )

        # 3. Event Logs Table
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS event_logs (
                id TEXT PRIMARY KEY,
                camera TEXT NOT NULL,
                label TEXT NOT NULL,
                sub_label TEXT NULL,
                confidence REAL NULL,
                zone TEXT NULL,
                status TEXT NOT NULL,
                snapshot_path TEXT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )

        self.conn.commit()

    def get_table_names(self) -> List[str]:
        """Return list of existing table names in database."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        return [row["name"] for row in cursor.fetchall()]

    # --------------------------------------------------------------------------
    # Face Management
    # --------------------------------------------------------------------------
    def add_face(
        self,
        name: str,
        role: str,
        embedding: List[float],
        expire_at: Optional[datetime.datetime] = None,
    ) -> int:
        """Add a face embedding to the whitelist database.

        Args:
            name: Label/name of the person.
            role: 'resident', 'guest_temporary', or 'unknown'.
            embedding: 512-d list of floats.
            expire_at: Optional expiration timestamp for temporary guests.

        Returns:
            Inserted face ID.
        """
        cursor = self.conn.cursor()
        expire_str = expire_at.isoformat() if expire_at else None
        cursor.execute(
            """
            INSERT INTO faces (name, role, embedding, expire_at)
            VALUES (?, ?, ?, ?)
            """,
            (name, role, json.dumps(embedding), expire_str),
        )
        self.conn.commit()
        return cursor.lastrowid

    def list_faces(self) -> List[Dict[str, Any]]:
        """List all active face records."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT id, name, role, created_at, expire_at FROM faces")
        return [dict(row) for row in cursor.fetchall()]

    def delete_face(self, face_id: int) -> bool:
        """Delete a face record by ID."""
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM faces WHERE id = ?", (face_id,))
        self.conn.commit()
        return cursor.rowcount > 0

    def find_matching_face(
        self,
        query_embedding: List[float],
        threshold: float = 0.68,
    ) -> Tuple[Optional[Dict[str, Any]], float]:
        """Find the closest face in database matching query embedding.

        Args:
            query_embedding: 512-d list of floats.
            threshold: Minimum cosine similarity required to match.

        Returns:
            Tuple of (matched_face_dict or None, highest_similarity_score).
        """
        cursor = self.conn.cursor()
        cursor.execute("SELECT id, name, role, embedding, expire_at FROM faces")
        rows = cursor.fetchall()

        now = datetime.datetime.now(datetime.timezone.utc)
        best_match = None
        best_sim = -1.0

        for row in rows:
            # Check expiration if set
            if row["expire_at"]:
                try:
                    exp = datetime.datetime.fromisoformat(row["expire_at"])
                    if exp.tzinfo is None:
                        exp = exp.replace(tzinfo=datetime.timezone.utc)
                    if exp < now:
                        continue
                except ValueError:
                    pass

            target_vec = json.loads(row["embedding"])
            sim = cosine_similarity(query_embedding, target_vec)
            if sim > best_sim:
                best_sim = sim
                if sim >= threshold:
                    best_match = {
                        "id": row["id"],
                        "name": row["name"],
                        "role": row["role"],
                    }

        return best_match, best_sim

    # --------------------------------------------------------------------------
    # Plate Management (Indonesian TNKB)
    # --------------------------------------------------------------------------
    def add_plate(
        self,
        plate_number: str,
        owner_label: str,
        vehicle_type: str = "car",
        is_family: bool = True,
    ) -> int:
        """Register an Indonesian vehicle plate into the whitelist database.

        Args:
            plate_number: Raw or formatted plate string.
            owner_label: Description or owner name.
            vehicle_type: 'car' or 'motorcycle'.
            is_family: True if family vehicle, False if guest.

        Returns:
            Inserted plate ID.
        """
        norm_plate, display_plate = normalize_tnkb_plate(plate_number)
        cursor = self.conn.cursor()
        cursor.execute(
            """
            INSERT INTO plates (plate_number, display_plate, owner_label, vehicle_type, is_family)
            VALUES (?, ?, ?, ?, ?)
            """,
            (norm_plate, display_plate, owner_label, vehicle_type, 1 if is_family else 0),
        )
        self.conn.commit()
        return cursor.lastrowid

    def list_plates(self) -> List[Dict[str, Any]]:
        """List all registered vehicle plates."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM plates ORDER BY created_at DESC")
        return [dict(row) for row in cursor.fetchall()]

    def find_plate(self, query_plate: str) -> Optional[Dict[str, Any]]:
        """Find vehicle plate info by normalized plate query."""
        try:
            norm_query, _ = normalize_tnkb_plate(query_plate)
        except ValueError:
            norm_query = query_plate.upper().replace(" ", "").replace("-", "")

        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM plates WHERE plate_number = ?", (norm_query,))
        row = cursor.fetchone()
        if row:
            res = dict(row)
            res["is_family"] = bool(res["is_family"])
            return res
        return None

    def delete_plate(self, plate_id: int) -> bool:
        """Delete a plate record by ID."""
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM plates WHERE id = ?", (plate_id,))
        self.conn.commit()
        return cursor.rowcount > 0

    # --------------------------------------------------------------------------
    # Event Logs
    # --------------------------------------------------------------------------
    def log_event(
        self,
        event_id: str,
        camera: str,
        label: str,
        sub_label: Optional[str] = None,
        confidence: Optional[float] = None,
        zone: Optional[str] = None,
        status: str = "detected",
        snapshot_path: Optional[str] = None,
    ) -> None:
        """Record an anomaly detection or surveillance event."""
        cursor = self.conn.cursor()
        cursor.execute(
            """
            INSERT OR REPLACE INTO event_logs 
            (id, camera, label, sub_label, confidence, zone, status, snapshot_path)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (event_id, camera, label, sub_label, confidence, zone, status, snapshot_path),
        )
        self.conn.commit()

    def list_events(self, limit: int = 50) -> List[Dict[str, Any]]:
        """List recent events ordered by newest first."""
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT * FROM event_logs ORDER BY created_at DESC, rowid DESC LIMIT ?", (limit,)
        )
        return [dict(row) for row in cursor.fetchall()]

    def close(self) -> None:
        """Close database connection."""
        self.conn.close()
