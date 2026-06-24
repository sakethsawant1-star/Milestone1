"""
config.py — Centralized Configuration for Review Discovery Engine
=================================================================
Loads environment variables from `.env` and defines project-wide constants
including theme taxonomy, rate limits, batch sizes, and file paths.
"""

import os
import json
from pathlib import Path
from dotenv import load_dotenv

# ──────────────────────────────────────────────
# 1. Environment Setup
# ──────────────────────────────────────────────

# Project root is one level above phase1-setup/
PROJECT_ROOT = Path(__file__).resolve().parent.parent
ENV_PATH = PROJECT_ROOT / ".env"

# Load .env from project root
load_dotenv(dotenv_path=ENV_PATH)

# ──────────────────────────────────────────────
# 2. API Keys & Credentials
# ──────────────────────────────────────────────

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID", "")
REDDIT_CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET", "")
REDDIT_USER_AGENT = os.getenv("REDDIT_USER_AGENT", "SpotifyReviewEngine/1.0")

# ──────────────────────────────────────────────
# 3. Database
# ──────────────────────────────────────────────

DATA_DIR = PROJECT_ROOT / "data"
DB_PATH = DATA_DIR / "database.sqlite"
LEXICON_PATH = DATA_DIR / "lexicon" / "discovery_keywords.json"

# ──────────────────────────────────────────────
# 4. LLM Configuration (Groq)
# ──────────────────────────────────────────────

# Primary model — best for complex classification
LLM_PRIMARY_MODEL = "llama3-70b-8192"

# Secondary model — faster, for simpler tasks
LLM_SECONDARY_MODEL = "mixtral-8x7b-32768"

# Rate limits (Groq free tier)
GROQ_RATE_LIMIT_RPM = 30          # requests per minute
GROQ_RATE_LIMIT_RPD = 14_400      # requests per day
GROQ_REQUEST_DELAY = 2.0          # seconds between requests (safe margin)

# Batch processing
BATCH_SIZE = int(os.getenv("BATCH_SIZE", "50"))
LLM_TEMPERATURE = 0.2             # Low temperature for consistent classification
LLM_MAX_TOKENS = 2000

# ──────────────────────────────────────────────
# 5. Theme Taxonomy (T1–T7)
# ──────────────────────────────────────────────

THEME_TAXONOMY = {
    "T1": "Algorithm Accuracy",
    "T2": "Search Usability",
    "T3": "Library Management",
    "T4": "Feature Discovery",
    "T5": "UI Navigation",
    "T6": "Audio Quality & Playback",
    "T7": "Ads & Premium Friction",
}

# ──────────────────────────────────────────────
# 6. Sentiment Classes
# ──────────────────────────────────────────────

SENTIMENT_CLASSES = ["positive", "neutral", "negative", "frustrated"]

# ──────────────────────────────────────────────
# 7. Scraper Configuration
# ──────────────────────────────────────────────

# Target app identifiers
SPOTIFY_PLAY_STORE_ID = "com.spotify.music"
SPOTIFY_APP_STORE_ID = "324684580"

# Target subreddits for Reddit scraper (quality-first set; see reddit_scraper.py)
REDDIT_SUBREDDITS = [
    "spotify",
    "truespotify",
    "spotifyplaylists",
    "SpotifyPremium",
    "ifyoulikeblank",
    "MusicRecommendations",
    "listentothis",
    "streaming",
]

# Review count targets per source
SCRAPER_TARGETS = {
    "play_store": 3000,
    "app_store": 2000,
    "reddit": 400,       # quality over quantity for Reddit
    "community": 500,     # Stretch goal
}

# ──────────────────────────────────────────────
# 8. Pipeline Configuration
# ──────────────────────────────────────────────

# Deduplication
FUZZY_DEDUP_THRESHOLD = 0.85      # Jaccard similarity threshold

# Relevance filter: ≥1 primary OR ≥2 secondary keywords
MIN_PRIMARY_KEYWORDS = 1
MIN_SECONDARY_KEYWORDS = 2

# PII patterns to strip
PII_EMAIL_REGEX = r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+"
PII_PHONE_REGEX = r"\b\d{3}[-.\s]?\d{3}[-.\s]?\d{4}\b"
PII_URL_REGEX = r"https?://\S+"

# ──────────────────────────────────────────────
# 9. Logging
# ──────────────────────────────────────────────

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# ──────────────────────────────────────────────
# 10. Utility Functions
# ──────────────────────────────────────────────

def load_discovery_keywords() -> dict:
    """Load discovery keywords lexicon from JSON file."""
    if LEXICON_PATH.exists():
        with open(LEXICON_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"primary": [], "secondary": []}


def validate_env() -> dict:
    """
    Validate that required environment variables are set.
    Returns a dict of {variable_name: is_set} for reporting.
    """
    checks = {
        "GROQ_API_KEY": bool(GROQ_API_KEY),
        "REDDIT_CLIENT_ID": bool(REDDIT_CLIENT_ID),
        "REDDIT_CLIENT_SECRET": bool(REDDIT_CLIENT_SECRET),
    }
    return checks


# ──────────────────────────────────────────────
# 11. Self-Test (run directly to verify config)
# ──────────────────────────────────────────────

if __name__ == "__main__":
    print("=" * 50)
    print("  Review Discovery Engine -- Config Check")
    print("=" * 50)
    print()

    print(f"  Project Root:    {PROJECT_ROOT}")
    print(f"  .env Path:       {ENV_PATH} ({'[OK] exists' if ENV_PATH.exists() else '[X] missing'})")
    print(f"  DB Path:         {DB_PATH}")
    print(f"  Lexicon Path:    {LEXICON_PATH} ({'[OK] exists' if LEXICON_PATH.exists() else '[X] missing'})")
    print()

    print("  API Keys:")
    env_status = validate_env()
    for key, is_set in env_status.items():
        status = "[OK] set" if is_set else "[X] NOT SET"
        print(f"    {key}: {status}")
    print()

    print(f"  Primary LLM:     {LLM_PRIMARY_MODEL}")
    print(f"  Secondary LLM:   {LLM_SECONDARY_MODEL}")
    print(f"  Batch Size:      {BATCH_SIZE}")
    print(f"  Rate Limit:      {GROQ_RATE_LIMIT_RPM} req/min")
    print()

    print("  Theme Taxonomy:")
    for tid, name in THEME_TAXONOMY.items():
        print(f"    {tid}: {name}")
    print()

    keywords = load_discovery_keywords()
    print(f"  Discovery Keywords: {len(keywords.get('primary', []))} primary, {len(keywords.get('secondary', []))} secondary")
    print()
    print("=" * 50)
    print("  Config loaded successfully.")
    print("=" * 50)

