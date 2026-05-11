import sqlite3
from langgraph.checkpoint.sqlite import SqliteSaver


# =====================================================
# SQLITE CHECKPOINTER (FIXED VERSION)
# =====================================================

# Create actual SQLite connection (NOT string)
conn = sqlite3.connect(
    "checkpoints.db",
    check_same_thread=False
)

# Pass connection to LangGraph
checkpointer = SqliteSaver(conn)