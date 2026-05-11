from pathlib import Path
from uuid import uuid4

from sentence_transformers import SentenceTransformer

from langchain_text_splitters import (
    RecursiveCharacterTextSplitter
)

from src.vector_db.chroma_client import collection


# =====================================================
# LOAD EMBEDDING MODEL
# =====================================================

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)


# =====================================================
# KNOWLEDGE BASE PATH
# =====================================================

BASE_DIR = Path(__file__).resolve().parent.parent.parent

KNOWLEDGE_DIR = BASE_DIR / "knowledge_base"


# =====================================================
# TEXT SPLITTER
# =====================================================

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)


# =====================================================
# LOAD DOCUMENTS
# =====================================================

documents = []

metadata_list = []

print("\nLoading knowledge files...\n")


for file_path in KNOWLEDGE_DIR.glob("*.txt"):

    print(f"Reading: {file_path.name}")

    with open(file_path, "r", encoding="utf-8") as file:

        text = file.read()

    chunks = text_splitter.split_text(text)

    for chunk in chunks:

        documents.append(chunk)

        metadata_list.append({
            "source_file": file_path.name,
            "topic": file_path.stem
        })


print(f"\nTotal chunks created: {len(documents)}\n")


# =====================================================
# GENERATE EMBEDDINGS
# =====================================================

print("\nGenerating embeddings...\n")

embeddings = model.encode(documents)


# =====================================================
# STORE IN CHROMADB
# =====================================================

print("\nAdding chunks to ChromaDB...\n")


for idx, doc in enumerate(documents):

    collection.add(

        ids=[str(uuid4())],

        documents=[doc],

        embeddings=[embeddings[idx].tolist()],

        metadatas=[metadata_list[idx]]
    )


print("\nChecking collection count...\n")

count = collection.count()

print(f"\nTOTAL DOCUMENTS IN DB: {count}\n")


print("\nKnowledge base ingestion completed.\n")