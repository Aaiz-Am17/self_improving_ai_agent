# src/security/guardrails_config.py

"""
Configuration settings for the security guardrail system.
"""

MAX_PROMPT_LENGTH = 5000

BLOCKED_FILE_PATTERNS = [
    "..",
    "/etc/passwd",
    "C:\\Windows",
]

ALLOWED_DATASET_EXTENSIONS = [
    ".csv",
    ".xlsx",
    ".parquet",
]