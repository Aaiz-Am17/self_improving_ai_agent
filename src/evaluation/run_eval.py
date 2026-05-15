import json
import sys

from src.agent.graph import graph


# =====================================================
# LOAD THRESHOLDS
# =====================================================

with open(
    "src/evaluation/eval_threshold_config.json",
    "r",
    encoding="utf-8"
) as f:

    thresholds = json.load(f)


# =====================================================
# TEST STATE
# =====================================================

initial_state = {

    "dataset_path":
        "data/datasets/titanic.csv",

    "thread_id":
        "ci_evaluation_session",
        
    "runtime_mode": 
        "ci"  # <--- ADD THIS LINE
}


config = {

    "configurable": {

        "thread_id":
            "ci_evaluation_session"
    }
}


# =====================================================
# RUN GRAPH
# =====================================================

result = graph.invoke(

    initial_state,

    config=config
)


# =====================================================
# EXTRACT SCORES
# =====================================================

metrics = result.get(
    "evaluation_metrics",
    {}
)

relevancy = metrics.get(
    "relevancy_score",
    0
)

hallucination = metrics.get(
    "hallucination_score",
    0
)

tool_accuracy = metrics.get(
    "tool_accuracy_score",
    0
)

final_score = metrics.get(
    "final_score",
    0
)


# =====================================================
# DISPLAY RESULTS
# =====================================================

print("\n============================")
print("CI/CD EVALUATION RESULTS")
print("============================")

print(f"Relevancy Score: {relevancy}")
print(f"Hallucination Score: {hallucination}")
print(f"Tool Accuracy Score: {tool_accuracy}")
print(f"Final Score: {final_score}")


# =====================================================
# THRESHOLD CHECKING
# =====================================================

passed = (

    relevancy >= thresholds["min_relevancy"]

    and hallucination >= thresholds["min_hallucination"]

    and tool_accuracy >= thresholds["min_tool_accuracy"]

    and final_score >= thresholds["min_final_score"]
)


# =====================================================
# EXIT CODE
# =====================================================

if passed:

    print("\nCI/CD CHECK PASSED")

    sys.exit(0)

else:

    print("\nCI/CD CHECK FAILED")

    sys.exit(1)