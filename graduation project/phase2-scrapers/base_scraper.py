"""
base_scraper.py -- Abstract Base Scraper
=========================================
Defines the interface all scrapers must implement.
Provides shared utilities: DB save, dedup check, logging.
"""

import sys
import uuid
import hashlib
import sqlite3
import logging
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path

# Allow imports from phase1-setup
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "phase1-setup"))
import config

logging.basicConfig(
    level=getattr(logging, config.LOG_LEVEL, logging.INFO),
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)


class BaseScraper(ABC):
    """
    Abstract base class for all review scrapers.
    Subclasses must implement: fetch()
    """

    def __init__(self, source_name: str):
        self.source_name = source_name
        self.logger = logging.getLogger(source_name)
        self.db_path = config.DB_PATH
        self._saved_count = 0
        self._skipped_count = 0

    # ------------------------------------------------------------------
    # Abstract interface — subclasses must implement
    # ------------------------------------------------------------------

    @abstractmethod
    def fetch(self, count: int = 1000) -> list[dict]:
        """
        Fetch raw reviews from the source.
        Must return a list of dicts conforming to the raw_review schema:
        {
            "id": str,           # unique identifier
            "source": str,       # play_store | app_store | reddit | community
            "rating": int|None,  # 1-5 or None for Reddit posts
            "title": str|None,
            "text": str,         # required
            "date": str|None,    # ISO 8601
            "metadata": dict,    # source-specific extras
        }
        """
        ...

    # ------------------------------------------------------------------
    # Shared utilities
    # ------------------------------------------------------------------

    def generate_id(self, text: str, source: str) -> str:
        """Generate a stable UUID-like ID from source + text content hash."""
        hash_input = f"{source}::{text[:200]}".encode("utf-8")
        return hashlib.md5(hash_input).hexdigest()

    def already_exists(self, review_id: str) -> bool:
        """Check if a review with this ID already exists in raw_reviews."""
        conn = sqlite3.connect(str(self.db_path))
        cursor = conn.cursor()
        cursor.execute("SELECT 1 FROM raw_reviews WHERE id = ?", (review_id,))
        exists = cursor.fetchone() is not None
        conn.close()
        return exists

    def save_to_db(self, reviews: list[dict]) -> int:
        """
        Save a list of review dicts to raw_reviews table.
        Skips duplicates. Returns number of newly saved reviews.
        """
        if not reviews:
            return 0

        conn = sqlite3.connect(str(self.db_path))
        conn.execute("PRAGMA foreign_keys=ON;")
        cursor = conn.cursor()
        saved = 0

        for review in reviews:
            # Validate required fields
            if not review.get("text", "").strip():
                self.logger.debug("Skipping review with empty text")
                self._skipped_count += 1
                continue

            review_id = review.get("id") or self.generate_id(
                review["text"], self.source_name
            )

            # Skip duplicates
            cursor.execute("SELECT 1 FROM raw_reviews WHERE id = ?", (review_id,))
            if cursor.fetchone():
                self._skipped_count += 1
                continue

            import json
            try:
                cursor.execute(
                    """
                    INSERT INTO raw_reviews (id, source, rating, title, text, date, metadata)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        review_id,
                        review.get("source", self.source_name),
                        review.get("rating"),
                        review.get("title"),
                        review["text"].strip(),
                        review.get("date"),
                        json.dumps(review.get("metadata", {})),
                    ),
                )
                saved += 1
                self._saved_count += 1
            except sqlite3.IntegrityError:
                self._skipped_count += 1

        conn.commit()
        conn.close()
        return saved

    def get_db_count(self) -> int:
        """Return current count of raw_reviews for this source."""
        conn = sqlite3.connect(str(self.db_path))
        cursor = conn.cursor()
        cursor.execute(
            "SELECT COUNT(*) FROM raw_reviews WHERE source = ?", (self.source_name,)
        )
        count = cursor.fetchone()[0]
        conn.close()
        return count

    def run(self, count: int = None) -> dict:
        """
        Main entry point. Fetches and saves reviews.
        Returns a summary dict.
        """
        target = count or config.SCRAPER_TARGETS.get(self.source_name, 1000)
        self.logger.info(f"Starting {self.source_name} scraper (target: {target})")

        start = datetime.now()
        reviews = self.fetch(count=target)

        fetched = len(reviews)
        saved = self.save_to_db(reviews)
        duration = (datetime.now() - start).total_seconds()

        summary = {
            "source": self.source_name,
            "fetched": fetched,
            "saved": saved,
            "skipped": self._skipped_count,
            "total_in_db": self.get_db_count(),
            "duration_seconds": round(duration, 2),
        }

        self.logger.info(
            f"Done. Fetched: {fetched} | Saved: {saved} | "
            f"Skipped: {self._skipped_count} | Time: {duration:.1f}s"
        )
        return summary
