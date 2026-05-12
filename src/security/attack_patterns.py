# src/security/attack_patterns.py

"""
Contains known jailbreak and prompt injection patterns.

These patterns are used by the guardrail system
to detect malicious or unsafe prompts before they
reach the LangGraph agent system.
"""

JAILBREAK_PATTERNS = [
    "ignore previous instructions",
    "ignore all previous instructions",
    "disregard safety",
    "bypass restrictions",
    "pretend you are",
    "act as root",
    "developer mode",
    "dan mode",
    "do anything now",
    "system prompt",
    "reveal hidden instructions",
    "show hidden prompt",
    "disable guardrails",
    "turn off safety",
    "jailbreak",
]

RESTRICTED_KEYWORDS = [
    "delete database",
    "drop table",
    "shutdown system",
    "remove all files",
    "os.system",
    "subprocess",
    "rm -rf",
    "format disk",
]