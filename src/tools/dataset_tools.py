from langchain_core.tools import tool
from pydantic import BaseModel, Field
from typing import Dict, Any
import pandas as pd


# =========================================================
# TOOL 1 INPUT SCHEMA
# =========================================================

class DatasetInput(BaseModel):
    """
    Input schema for dataset inspection tool.
    """

    file_path: str = Field(
        ...,
        description="Path to the CSV dataset file"
    )


# =========================================================
# TOOL 1 - DATASET INSPECTION
# =========================================================

@tool(args_schema=DatasetInput)
def inspect_dataset(file_path: str) -> Dict[str, Any]:
    """
    Inspect a dataset and return structured dataset statistics.

    This tool should be used when the agent needs to:
    - understand dataset structure
    - inspect column names
    - analyze data types
    - determine dataset dimensions
    """

    try:
        df = pd.read_csv(file_path)

        rows = df.shape[0]
        cols = df.shape[1]
        columns = list(df.columns)

        return {
            "status": "success",
            "rows": rows,
            "columns": cols,
            "column_names": columns,
            "data_types": df.dtypes.astype(str).to_dict()
        }

    except Exception as e:

        return {
            "status": "error",
            "message": str(e)
        }


# =========================================================
# TOOL 2 INPUT SCHEMA
# =========================================================

class MissingInput(BaseModel):
    """
    Input schema for missing value detection tool.
    """

    file_path: str = Field(
        ...,
        description="Path to the CSV dataset file"
    )


# =========================================================
# TOOL 2 - MISSING VALUE DETECTION
# =========================================================

@tool(args_schema=MissingInput)
def detect_missing_values(file_path: str) -> Dict[str, Any]:
    """
    Detect missing values in the dataset.

    This tool should be used to:
    - analyze dataset quality
    - identify incomplete columns
    - support preprocessing decisions
    """

    try:
        df = pd.read_csv(file_path)

        missing = df.isnull().sum()

        missing_percentage = (
            (df.isnull().sum() / len(df)) * 100
        ).round(2)

        return {
            "status": "success",
            "missing_values": missing.to_dict(),
            "missing_percentage": missing_percentage.to_dict()
        }

    except Exception as e:

        return {
            "status": "error",
            "message": str(e)
        }


# =========================================================
# TOOL 3 INPUT SCHEMA
# =========================================================

class FeatureAnalysisInput(BaseModel):
    """
    Input schema for feature analysis tool.
    """

    file_path: str = Field(
        ...,
        description="Path to the CSV dataset file"
    )


# =========================================================
# TOOL 3 - FEATURE ANALYSIS
# =========================================================

@tool(args_schema=FeatureAnalysisInput)
def analyze_features(file_path: str) -> Dict[str, Any]:
    """
    Analyze dataset features and determine:
    - numerical columns
    - categorical columns
    - low-cardinality features
    - high-cardinality features

    Helps the agent decide preprocessing strategies.
    """

    try:
        df = pd.read_csv(file_path)

        numeric_cols = df.select_dtypes(
            include=["int64", "float64"]
        ).columns.tolist()

        categorical_cols = df.select_dtypes(
            include=["object"]
        ).columns.tolist()

        high_cardinality = []
        low_cardinality = []

        for col in categorical_cols:

            unique_count = df[col].nunique()

            if unique_count > 20:
                high_cardinality.append(col)

            else:
                low_cardinality.append(col)

        return {
            "status": "success",
            "numeric_columns": numeric_cols,
            "categorical_columns": categorical_cols,
            "low_cardinality_columns": low_cardinality,
            "high_cardinality_columns": high_cardinality
        }

    except Exception as e:

        return {
            "status": "error",
            "message": str(e)
        }