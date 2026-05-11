def planner_node(state):
    """
    Pipeline Architect Agent

    Responsible for:
    - preprocessing planning
    - encoding decisions
    - scaling decisions
    - missing value strategies
    """

    feature_analysis = state.get(
        "feature_analysis",
        {}
    )

    missing_values = state.get(
        "missing_values",
        {}
    )

    # =====================================================
    # EXTRACT INFORMATION
    # =====================================================

    numeric_columns = feature_analysis.get(
        "numeric_columns",
        []
    )

    categorical_columns = feature_analysis.get(
        "categorical_columns",
        []
    )

    low_cardinality = feature_analysis.get(
        "low_cardinality_columns",
        []
    )

    high_cardinality = feature_analysis.get(
        "high_cardinality_columns",
        []
    )

    missing_dict = missing_values.get(
        "missing_values",
        {}
    )

    # =====================================================
    # BUILD STRUCTURED PLAN
    # =====================================================

    preprocessing_plan = {

        # ---------------------------------------------
        # Missing value handling
        # ---------------------------------------------

        "missing_value_strategy": {

            "numeric_columns": {

                "strategy": "median_imputation",

                "columns": [

                    col

                    for col in numeric_columns

                    if missing_dict.get(col, 0) > 0
                ]
            },

            "categorical_columns": {

                "strategy": "most_frequent",

                "columns": [

                    col

                    for col in categorical_columns

                    if missing_dict.get(col, 0) > 0
                ]
            }
        },

        # ---------------------------------------------
        # Encoding strategy
        # ---------------------------------------------

        "encoding_strategy": {

            "one_hot_encoding": low_cardinality,

            "target_encoding": high_cardinality
        },

        # ---------------------------------------------
        # Scaling strategy
        # ---------------------------------------------

        "scaling_strategy": {

            "method": "StandardScaler",

            "columns": numeric_columns
        }
    }

    return {

        "preprocessing_plan": preprocessing_plan,

        "current_agent": "pipeline_architect"
    }