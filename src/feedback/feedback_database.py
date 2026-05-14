"""
Persistent feedback database layer.
"""

import sqlite3
from datetime import datetime

from src.configs.settings import settings


DB_PATH = settings.FEEDBACK_DB_PATH


def initialize_feedback_database():
    """
    Creates feedback table if it does not exist.
    """

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS feedback_logs (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            timestamp TEXT,

            thread_id TEXT,

            user_input TEXT,

            agent_response TEXT,

            feedback_score INTEGER,

            optional_comment TEXT
        )
        """
    )

    conn.commit()

    conn.close()


def insert_feedback_log(
    thread_id: str,
    user_input: str,
    agent_response: str,
    feedback_score: int,
    optional_comment: str = ""
):
    """
    Stores user feedback interaction.
    """

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO feedback_logs (
            timestamp,
            thread_id,
            user_input,
            agent_response,
            feedback_score,
            optional_comment
        )
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            datetime.utcnow().isoformat(),
            thread_id,
            user_input,
            agent_response,
            feedback_score,
            optional_comment
        )
    )

    conn.commit()

    conn.close()