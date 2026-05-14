"""
Feedback drift analysis.
"""

import sqlite3

from src.configs.settings import settings


DB_PATH = settings.FEEDBACK_DB_PATH


def analyze_failures():

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            timestamp,
            user_input,
            agent_response,
            optional_comment

        FROM feedback_logs

        WHERE feedback_score = -1
        """
    )

    failed_logs = cursor.fetchall()

    conn.close()

    print("\nFAILED INTERACTIONS:\n")

    for log in failed_logs:

        print("=" * 50)

        print(f"Timestamp: {log[0]}")

        print(f"User Input: {log[1]}")

        print(f"Agent Response: {log[2]}")

        print(f"Comment: {log[3]}")

        print("=" * 50)


if __name__ == "__main__":

    analyze_failures()