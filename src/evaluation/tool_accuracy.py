"""
Tool usage evaluation utilities.
"""

from typing import List


def evaluate_tool_usage(
    used_tools: List[str],
    expected_tools: List[str]
) -> float:
    """
    Measures overlap between expected
    and actually used tools.
    """

    if not expected_tools:
        return 1.0

    matched = 0

    for tool in expected_tools:

        if tool in used_tools:
            matched += 1

    return matched / len(expected_tools)