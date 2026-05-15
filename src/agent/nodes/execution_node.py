import pandas as pd

from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from joblib import dump

from src.evaluation.timing_utils import start_timer, end_timer
from src.observability.telemetry import build_telemetry_payload


def execution_node(state):

    timer = start_timer()

    dataset_path = state.get("dataset_path")
    preprocessing_plan = state.get("preprocessing_plan", {})

    tool_usage_log = state.get("tool_usage_log", [])

    df = pd.read_csv(dataset_path)

    target_column = "Survived"

    X = df.drop(columns=[target_column])
    y = df[target_column]

    numeric_columns = preprocessing_plan.get(
        "missing_value_strategy", {}
    ).get("numeric_columns", {}).get("columns", [])

    categorical_columns = preprocessing_plan.get(
        "encoding_strategy", {}
    ).get("one_hot_encoding", [])

    numeric_pipeline = Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler())
    ])

    categorical_pipeline = Pipeline([
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("encoder", OneHotEncoder(handle_unknown="ignore"))
    ])

    preprocessor = ColumnTransformer([
        ("num", numeric_pipeline, numeric_columns),
        ("cat", categorical_pipeline, categorical_columns)
    ])

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model_pipeline = Pipeline([
        ("preprocessor", preprocessor),
        ("classifier", RandomForestClassifier(random_state=42))
    ])

    model_pipeline.fit(X_train, y_train)

    predictions = model_pipeline.predict(X_test)

    accuracy = accuracy_score(y_test, predictions)

    model_path = "trained_model.pkl"
    dump(model_pipeline, model_path)

    tool_usage_log.extend([
        "SimpleImputer",
        "StandardScaler",
        "OneHotEncoder",
        "RandomForestClassifier"
    ])

    execution_time = end_timer(timer)

    node_execution_times = state.get("node_execution_times", {})
    workflow_path = state.get("workflow_path", [])

    node_execution_times["execution_agent"] = execution_time
    workflow_path.append("execution_agent")

    telemetry_payload = build_telemetry_payload(
        thread_id=state.get("thread_id", ""),
        current_agent="execution_agent",
        execution_status="completed"
    )

    return {
        "execution_status": "completed",
        "model_accuracy": float(accuracy),
        "trained_model_path": model_path,
        "tool_usage_log": tool_usage_log,
        "node_execution_times": node_execution_times,
        "workflow_path": workflow_path,
        "telemetry_data": telemetry_payload,
        "current_agent": "execution_agent"
    }