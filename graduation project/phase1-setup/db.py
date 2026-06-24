"""
db.py — SQLite Database Manager for Review Discovery Engine
============================================================
Creates and manages the SQLite database with 4 tables:
  1. raw_reviews        — As-scraped reviews from all sources
  2. processed_reviews  — Cleaned, PII-free, deduplicated reviews
  3. analysis_results   — LLM classification output (theme + sentiment)
  4. pipeline_runs      — Aggregated insights per pipeline execution

Usage:
  python db.py              # Creates database with all tables
  python db.py --verify     # Verifies existing database structure
"""

import sys
import sqlite3
import uuid
from pathlib import Path
from datetime import datetime

# Import config (handles path resolution)
sys.path.insert(0, str(Path(__file__).resolve().parent))
import config


# ──────────────────────────────────────────────
# SQL Schema Definitions
# ──────────────────────────────────────────────

CREATE_RAW_REVIEWS = """
CREATE TABLE IF NOT EXISTS raw_reviews (
    id TEXT PRIMARY KEY,
    source TEXT NOT NULL,            -- play_store | app_store | reddit | community
    rating INTEGER,
    title TEXT,
    text TEXT NOT NULL,
    date TEXT,                       -- ISO 8601
    metadata JSON,                  -- thumbs_up, subreddit, reply_count, etc.
    scraped_at TEXT DEFAULT (datetime('now'))
);
"""

CREATE_PROCESSED_REVIEWS = """
CREATE TABLE IF NOT EXISTS processed_reviews (
    id TEXT PRIMARY KEY,
    source TEXT NOT NULL,
    rating INTEGER,
    text TEXT NOT NULL,              -- PII-stripped
    date TEXT,
    word_count INTEGER,
    discovery_keywords JSON,
    engagement_score INTEGER,
    processed_at TEXT DEFAULT (datetime('now'))
);
"""

CREATE_ANALYSIS_RESULTS = """
CREATE TABLE IF NOT EXISTS analysis_results (
    review_id TEXT PRIMARY KEY,
    theme_ids JSON,                 -- ["T1", "T3"]
    theme_confidence REAL,
    sentiment TEXT,                  -- positive | neutral | negative | frustrated
    sentiment_confidence REAL,
    signal_phrases JSON,
    analyzed_at TEXT DEFAULT (datetime('now')),
    FOREIGN KEY (review_id) REFERENCES processed_reviews(id)
);
"""

CREATE_PIPELINE_RUNS = """
CREATE TABLE IF NOT EXISTS pipeline_runs (
    run_id TEXT PRIMARY KEY,
    started_at TEXT,
    completed_at TEXT,
    total_raw INTEGER,
    total_processed INTEGER,
    total_analyzed INTEGER,
    themes_summary JSON,
    sentiment_summary JSON,
    top_quotes JSON,
    behavior_patterns JSON,
    status TEXT DEFAULT 'running'    -- running | completed | failed
);
"""

# All schema statements in order
SCHEMA_STATEMENTS = [
    ("raw_reviews", CREATE_RAW_REVIEWS),
    ("processed_reviews", CREATE_PROCESSED_REVIEWS),
    ("analysis_results", CREATE_ANALYSIS_RESULTS),
    ("pipeline_runs", CREATE_PIPELINE_RUNS),
]

# Create indexes for common queries
CREATE_INDEXES = [
    "CREATE INDEX IF NOT EXISTS idx_raw_source ON raw_reviews(source);",
    "CREATE INDEX IF NOT EXISTS idx_raw_date ON raw_reviews(date);",
    "CREATE INDEX IF NOT EXISTS idx_processed_source ON processed_reviews(source);",
    "CREATE INDEX IF NOT EXISTS idx_analysis_sentiment ON analysis_results(sentiment);",
    "CREATE INDEX IF NOT EXISTS idx_pipeline_status ON pipeline_runs(status);",
]


# ──────────────────────────────────────────────
# Database Manager Class
# ──────────────────────────────────────────────

class DatabaseManager:
    """Manages SQLite database connections and operations."""

    def __init__(self, db_path: Path = None):
        self.db_path = db_path or config.DB_PATH
        self._ensure_data_dir()

    def _ensure_data_dir(self):
        """Create the data directory if it doesn't exist."""
        self.db_path.parent.mkdir(parents=True, exist_ok=True)

    def get_connection(self) -> sqlite3.Connection:
        """Get a database connection with row factory enabled."""
        conn = sqlite3.connect(str(self.db_path))
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA journal_mode=WAL;")       # Write-ahead logging
        conn.execute("PRAGMA foreign_keys=ON;")         # Enforce FK constraints
        return conn

    def initialize(self) -> bool:
        """Create all tables and indexes. Returns True on success."""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()

            for table_name, create_sql in SCHEMA_STATEMENTS:
                cursor.execute(create_sql)
                print(f"  [OK] Table '{table_name}' ready")

            for index_sql in CREATE_INDEXES:
                cursor.execute(index_sql)
            print(f"  [OK] {len(CREATE_INDEXES)} indexes created")

            conn.commit()
            conn.close()
            return True

        except sqlite3.Error as e:
            print(f"  [X] Database error: {e}")
            return False

    def verify(self) -> dict:
        """
        Verify database structure. Returns a dict with table names
        and their column counts.
        """
        if not self.db_path.exists():
            return {"error": "Database file does not exist"}

        conn = self.get_connection()
        cursor = conn.cursor()

        # Get all tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [row[0] for row in cursor.fetchall()]

        result = {}
        for table in tables:
            cursor.execute(f"PRAGMA table_info({table});")
            columns = cursor.fetchall()
            result[table] = {
                "column_count": len(columns),
                "columns": [col[1] for col in columns],
                "row_count": cursor.execute(
                    f"SELECT COUNT(*) FROM {table}"
                ).fetchone()[0],
            }

        conn.close()
        return result

    def create_pipeline_run(self) -> str:
        """Create a new pipeline run record. Returns the run_id."""
        run_id = str(uuid.uuid4())[:8]
        conn = self.get_connection()
        conn.execute(
            "INSERT INTO pipeline_runs (run_id, started_at, status) VALUES (?, ?, ?)",
            (run_id, datetime.now().isoformat(), "running"),
        )
        conn.commit()
        conn.close()
        return run_id

    def get_table_counts(self) -> dict:
        """Get row counts for all tables."""
        conn = self.get_connection()
        cursor = conn.cursor()
        counts = {}
        for table_name, _ in SCHEMA_STATEMENTS:
            count = cursor.execute(
                f"SELECT COUNT(*) FROM {table_name}"
            ).fetchone()[0]
            counts[table_name] = count
        conn.close()
        return counts


# ──────────────────────────────────────────────
# CLI Entry Point
# ──────────────────────────────────────────────

def main():
    """Initialize or verify the database."""
    print("=" * 50)
    print("  Review Discovery Engine -- Database Setup")
    print("=" * 50)
    print()

    db = DatabaseManager()
    print(f"  Database: {db.db_path}")
    print()

    if "--verify" in sys.argv:
        # Verification mode
        print("  Verifying database structure...")
        print()
        info = db.verify()

        if "error" in info:
            print(f"  [X] {info['error']}")
            sys.exit(1)

        for table_name, details in info.items():
            print(f"  [TABLE] {table_name}")
            print(f"     Columns ({details['column_count']}): {', '.join(details['columns'])}")
            print(f"     Rows: {details['row_count']}")
            print()

        print("  [OK] Verification complete.")

    else:
        # Initialization mode
        print("  Creating tables...")
        print()
        success = db.initialize()
        print()

        if success:
            db_size = db.db_path.stat().st_size
            print(f"  [OK] Database created successfully ({db_size:,} bytes)")
            print(f"  [OK] Location: {db.db_path}")
            print()

            # Verify what we just created
            print("  Verifying...")
            info = db.verify()
            for table_name, details in info.items():
                cols = ", ".join(details["columns"])
                print(f"    {table_name}: {details['column_count']} columns — [{cols}]")
            print()
            print("  [OK] All tables verified. Phase 1 database setup complete.")
        else:
            print("  [X] Database creation failed.")
            sys.exit(1)

    print()
    print("=" * 50)


if __name__ == "__main__":
    main()
