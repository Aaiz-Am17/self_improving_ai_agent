import chromadb
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent.parent

DB_PATH = BASE_DIR / "chroma_db"

print(f"\nUSING CHROMA DB PATH: {DB_PATH}\n")


client = chromadb.PersistentClient(
    path=str(DB_PATH)
)

collection = client.get_or_create_collection(
    name="ml_knowledge"
)