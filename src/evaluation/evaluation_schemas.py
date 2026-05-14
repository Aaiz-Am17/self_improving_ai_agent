from pydantic import BaseModel, Field
from typing import List


class EvaluationCase(BaseModel):

    id: int

    query: str

    expected_keywords: List[str]

    expected_tools: List[str]


class EvaluationResult(BaseModel):

    case_id: int

    query: str

    response: str

    keyword_score: float

    tool_score: float

    hallucination_score: float

    final_score: float