"""
Evaluation scoring utilities.
"""

from typing import List


def keyword_relevancy_score(
    response: str,
    expected_keywords: List[str]
) -> float:
    """
    Measures keyword overlap.
    """

    response_lower = response.lower()

    matches = 0

    for keyword in expected_keywords:

        if keyword.lower() in response_lower:
            matches += 1

    return matches / len(expected_keywords)