"""
Timing utilities for observability.
"""

import time


def start_timer() -> float:
    """
    Returns current timer value.
    """

    return time.perf_counter()


def end_timer(start_time: float) -> float:
    """
    Returns elapsed execution time.
    """

    return round(
        time.perf_counter() - start_time,
        4
    )