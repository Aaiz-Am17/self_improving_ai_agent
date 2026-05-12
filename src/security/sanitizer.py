# src/security/sanitizer.py

"""
Sanitizes outputs before they are shown to users.
"""

import re


def sanitize_output(output: str) -> str:
    """
    Removes sensitive paths and internal metadata.
    """

    # Remove Windows-style paths
    output = re.sub(r"[A-Z]:\\\\[^\\s]+", "[REDACTED_PATH]", output)

    # Remove Unix-style paths
    output = re.sub(r"/[^\\s]+", "[REDACTED_PATH]", output)

    # Remove metadata-like fields
    sensitive_terms = [
        "api_key",
        "token",
        "password",
        "metadata",
        "internal_path",
    ]

    for term in sensitive_terms:
        output = output.replace(term, "[REDACTED]")

    return output