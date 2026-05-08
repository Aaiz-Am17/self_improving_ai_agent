from langchain_core.tools import tool
from pydantic import BaseModel
import pandas as pd


# ------------------------------
# TOOL 1 INPUT SCHEMA
# ------------------------------

class DatasetInput(BaseModel):
    file_path: str


# ------------------------------
# TOOL 1
# ------------------------------

@tool(args_schema=DatasetInput)
def inspect_dataset(file_path: str) -> str:
    """
    Inspect a dataset and return basic statistics such as number of rows,
    columns, and column names.

    Use this tool when you need to understand the structure of a dataset.
    """

    df = pd.read_csv(file_path)

    rows = df.shape[0]
    cols = df.shape[1]
    columns = list(df.columns)

    return f"Rows: {rows}, Columns: {cols}, Column Names: {columns}"


# ------------------------------
# TOOL 2 INPUT SCHEMA
# ------------------------------

class MissingInput(BaseModel):
    file_path: str


# ------------------------------
# TOOL 2
# ------------------------------

@tool(args_schema=MissingInput)
def detect_missing_values(file_path: str) -> str:
    """
    Detect missing values in a dataset.

    Use this tool when analyzing dataset quality.
    """

    df = pd.read_csv(file_path)

    missing = df.isnull().sum()

    return missing.to_string()
# ------------------------------
# TOOL 3 INPUT SCHEMA
# ------------------------------

class FeatureAnalysisInput(BaseModel):
    file_path: str


# ------------------------------
# TOOL 3
# ------------------------------

@tool(args_schema=FeatureAnalysisInput)
def analyze_features(file_path: str) -> str:
    """
    Analyze dataset features and determine column data types.
    Helps the agent decide preprocessing steps.
    """

    df = pd.read_csv(file_path)

    numeric_cols = df.select_dtypes(include=["int64", "float64"]).columns.tolist()
    categorical_cols = df.select_dtypes(include=["object"]).columns.tolist()

    high_cardinality = []
    low_cardinality = []

    for col in categorical_cols:
        unique_count = df[col].nunique()

        if unique_count > 20:
            high_cardinality.append(col)
        else:
            low_cardinality.append(col)

    result = f"""
NUMERIC COLUMNS:
{numeric_cols}

CATEGORICAL COLUMNS:
{categorical_cols}

LOW CARDINALITY (Good for OneHotEncoding):
{low_cardinality}

HIGH CARDINALITY (Consider Target Encoding):
{high_cardinality}
"""

    return result
