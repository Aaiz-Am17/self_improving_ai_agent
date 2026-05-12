# src/security/validators.py

from pydantic import BaseModel, Field
from typing import List

from src.security.attack_patterns import (
    JAILBREAK_PATTERNS,
    RESTRICTED_KEYWORDS,
)

from src.security.guardrails_config import MAX_PROMPT_LENGTH


class SecurityValidationResult(BaseModel):
    is_safe: bool = Field(..., description="Whether the input is safe")
    detected_issues: List[str] = Field(default_factory=list)


def validate_user_input(user_input: str) -> SecurityValidationResult:
    """
    Validates user prompts against known jailbreak
    and malicious instruction patterns.
    """

    issues = []

    normalized_input = user_input.lower()

    if len(user_input) > MAX_PROMPT_LENGTH:
        issues.append("Prompt exceeds maximum allowed length.")

    for pattern in JAILBREAK_PATTERNS:
        if pattern in normalized_input:
            issues.append(f"Detected jailbreak pattern: '{pattern}'")

    for keyword in RESTRICTED_KEYWORDS:
        if keyword in normalized_input:
            issues.append(f"Detected restricted keyword: '{keyword}'")

    return SecurityValidationResult(
        is_safe=len(issues) == 0,
        detected_issues=issues,
    )