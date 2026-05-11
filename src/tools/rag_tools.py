from langchain_core.tools import tool
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any

from sentence_transformers import SentenceTransformer

from src.vector_db.chroma_client import collection


# =====================================================
# LOAD EMBEDDING MODEL
# =====================================================

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)


# =====================================================
# INPUT SCHEMA
# =====================================================

class RAGQueryInput(BaseModel):
    """
    Input schema for ML knowledge retrieval.
    """

    query: str = Field(
        ...,
        description="Query for retrieving ML knowledge"
    )

    topic: Optional[str] = Field(
        default=None,
        description="""
        Optional metadata filter.

        Examples:
        - encoding
        - scaling
        - missing_values
        - imbalance
        """
    )

    top_k: int = Field(
        default=3,
        description="Number of chunks to retrieve"
    )


# =====================================================
# RAG RETRIEVAL TOOL
# =====================================================

@tool(args_schema=RAGQueryInput)
def retrieve_ml_knowledge(
    query: str,
    topic: Optional[str] = None,
    top_k: int = 3
) -> Dict[str, Any]:
    """
    Retrieve relevant ML preprocessing knowledge
    from the vector database.

    Supports:
    - semantic retrieval
    - metadata filtering
    - top-k retrieval
    """

    try:

        query_embedding = model.encode(query).tolist()

        where_filter = None

        # =================================================
        # OPTIONAL METADATA FILTERING
        # =================================================

        if topic:

            where_filter = {
                "topic": topic
            }

        results = collection.query(

            query_embeddings=[query_embedding],

            n_results=top_k,

            where=where_filter
        )

        documents = results.get(
            "documents",
            [[]]
        )[0]

        metadata = results.get(
            "metadatas",
            [[]]
        )[0]

        return {
            "status": "success",
            "query": query,
            "topic_filter": topic,
            "documents": documents,
            "metadata": metadata
        }

    except Exception as e:

        return {
            "status": "error",
            "message": str(e)
        }