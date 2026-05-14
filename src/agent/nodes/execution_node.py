import pandas as pd

from sklearn.impute import SimpleImputer

from sklearn.preprocessing import (
    OneHotEncoder,
    StandardScaler
)

from sklearn.compose import ColumnTransformer

from sklearn.pipeline import Pipeline

from sklearn.model_selection import (
    train_test_split
)

from sklearn.ensemble import RandomForestClassifier

from sklearn.metrics import accuracy_score

from joblib import dump

from src.evaluation.timing_utils import (
    start_timer,
    end_timer
)

from src.observability.telemetry import (
    build_telemetry_payload
)


def execution_node(state):

    """
    Execution Agent

    Responsible for:
    - building sklearn pipeline
    - preprocessing dataset
    - training ML model
    - evaluating performance
    """

    timer = start_timer()

    dataset_path = state.get(
        "dataset_path"
    )

    preprocessing_plan = state.get(
        "preprocessing_plan"
    )

    tool_usage_log = state.get(
        "tool_usage_log",
        []
    )

    # ============================================
    # LOAD DATASET
    # ============================================

    df = pd.read_csv(dataset_path)

    # ============================================
    # TARGET COLUMN
    # ============================================

    target_column = "Survived"

    X = df.drop(columns=[target_column])

    y = df[target_column]

    # ============================================
    # STRATEGIES
    # ============================================

    numeric_columns = preprocessing_plan[
        "missing_value_strategy"
    ]["numeric_columns"]["columns"]

    categorical_columns = preprocessing_plan[
        "encoding_strategy"
    ]["one_hot_encoding"]

    # ============================================
    # NUMERIC PIPELINE
    # ============================================

    numeric_pipeline = Pipeline([

        (
            "imputer",
            SimpleImputer(strategy="median")
        ),

        (
            "scaler",
            StandardScaler()
        )
    ])

    # ============================================
    # CATEGORICAL PIPELINE
    # ============================================

    categorical_pipeline = Pipeline([

        (
            "imputer",
            SimpleImputer(
                strategy="most_frequent"
            )
        ),

        (
            "encoder",
            OneHotEncoder(
                handle_unknown="ignore"
            )
        )
    ])

    # ============================================
    # COLUMN TRANSFORMER
    # ============================================

    preprocessor = ColumnTransformer([

        (
            "num",
            numeric_pipeline,
            numeric_columns
        ),

        (
            "cat",
            categorical_pipeline,
            categorical_columns
        )
    ])

    # ============================================
    # TRAIN TEST SPLIT
    # ============================================

    X_train, X_test, y_train, y_test = train_test_split(

        X,
        y,

        test_size=0.2,

        random_state=42
    )

    # ============================================
    # FULL PIPELINE
    # ============================================

    model_pipeline = Pipeline([

        (
            "preprocessor",
            preprocessor
        ),

        (
            "classifier",
            RandomForestClassifier(
                random_state=42
            )
        )
    ])

    # ============================================
    # TRAIN MODEL
    # ============================================

    model_pipeline.fit(
        X_train,
        y_train
    )

    # ============================================
    # PREDICTIONS
    # ============================================

    predictions = model_pipeline.predict(
        X_test
    )

    accuracy = accuracy_score(
        y_test,
        predictions
    )

    # ============================================
    # SAVE MODEL
    # ============================================

    model_path = "trained_model.pkl"

    dump(
        model_pipeline,
        model_path
    )

    # ============================================
    # PIPELINE OUTPUT
    # ============================================

    pipeline_output = {

        "model_type": "RandomForestClassifier",

        "accuracy": float(accuracy),

        "target_column": target_column,

        "numeric_columns": numeric_columns,

        "categorical_columns": categorical_columns
    }

    # ============================================
    # TOOL TRACKING
    # ============================================

    tool_usage_log.extend([

        "SimpleImputer",

        "StandardScaler",

        "OneHotEncoder",

        "RandomForestClassifier"
    ])

    # ============================================
    # OBSERVABILITY
    # ============================================

    execution_time = end_timer(timer)

    node_execution_times = state.get(
        "node_execution_times",
        {}
    )

    workflow_path = state.get(
        "workflow_path",
        []
    )

    node_execution_times[
        "execution_agent"
    ] = execution_time

    workflow_path.append(
        "execution_agent"
    )

    telemetry_payload = build_telemetry_payload(

        thread_id=state.get("thread_id", ""),

        current_agent="execution_agent",

        execution_status="completed"
    )

    print("\n==========================")
    print("MODEL TRAINED SUCCESSFULLY")
    print("==========================")

    print(f"\nAccuracy: {accuracy}")

    return {

        "execution_status": "completed",

        "model_accuracy": float(accuracy),

        "trained_model_path": model_path,

        "pipeline_output": pipeline_output,

        "tool_usage_log": tool_usage_log,

        "current_agent": "execution_agent",

        "node_execution_times": node_execution_times,

        "workflow_path": workflow_path,

        "telemetry_data": telemetry_payload
    }