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


def execution_node(state):
    """
    Execution Agent

    Responsible for:
    - building sklearn pipeline
    - preprocessing dataset
    - training ML model
    - evaluating performance
    """

    dataset_path = state.get(
        "dataset_path"
    )

    preprocessing_plan = state.get(
        "preprocessing_plan"
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

    print("\n==========================")
    print("MODEL TRAINED SUCCESSFULLY")
    print("==========================")

    print(f"\nAccuracy: {accuracy}")

    return {

        "execution_status": "completed",

        "model_accuracy": float(accuracy),

        "current_agent": "execution_agent"
    }