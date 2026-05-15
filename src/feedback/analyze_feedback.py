"""
Feedback drift analysis.
"""
import sqlite3
from src.configs.settings import settings

DB_PATH = settings.FEEDBACK_DB_PATH

def analyze_failures():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        # 1. Count total responses
        cursor.execute("SELECT COUNT(*) FROM feedback_logs")
        total_responses = cursor.fetchone()[0]

        # 2. Count negative feedback
        cursor.execute("SELECT COUNT(*) FROM feedback_logs WHERE feedback_score = -1")
        total_negative = cursor.fetchone()[0]

        # 3. Print Top 3 failed queries
        cursor.execute(
            """
            SELECT timestamp, user_input, agent_response, optional_comment
            FROM feedback_logs
            WHERE feedback_score = -1
            ORDER BY timestamp DESC
            LIMIT 3
            """
        )
        failed_logs = cursor.fetchall()

        print("\n📊 --- DRIFT ANALYSIS REPORT --- 📊")
        print(f"Total Responses: {total_responses}")
        print(f"Total Negative Feedback: {total_negative}")
        print("=" * 50)
        print("🚨 TOP 3 FAILED QUERIES 🚨\n")

        for log in failed_logs:
            print(f"Timestamp: {log[0]}")
            print(f"User Input: {log[1]}")
            print(f"Agent Response: {log[2][:150]}...") # Truncated for readability
            print(f"Comment: {log[3]}")
            print("-" * 50)

    except sqlite3.OperationalError:
        print("Database not found or empty. Please log some feedback first.")
    finally:
        conn.close()

if __name__ == "__main__":
    analyze_failures()