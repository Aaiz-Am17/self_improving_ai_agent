"""
Centralized reusable paths.
"""

from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent.parent

DATA_DIR = BASE_DIR / "data"

DATASET_DIR = DATA_DIR / "datasets"

LOG_DIR = BASE_DIR / "logs"

REPORT_DIR = BASE_DIR / "reports"

VECTOR_DB_DIR = BASE_DIR / "chroma_db"

EVALUATION_DIR = BASE_DIR / "src" / "evaluation"