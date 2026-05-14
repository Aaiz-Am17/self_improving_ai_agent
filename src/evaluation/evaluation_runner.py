"""
Enterprise evaluation runner.
"""

import json
import sys

from langchain_core.messages import HumanMessage

from src.agent.graph import graph


DATASET_PATH = (
    r"data/datasets/titanic.csv"
)


def run_standard_evaluations():

    with open(

        "src/evaluation/evaluation_dataset.json",

        "r",

        encoding="utf-8"

    ) as f:

        evaluation_cases = json.load(f)

    results = []

    for case in evaluation_cases:

        initial_state = {

            "messages": [

                HumanMessage(
                    content=case["query"]
                )
            ],

            "dataset_path": DATASET_PATH,

            "thread_id": f"eval_{case['id']}"
        }

        result = graph.invoke(
            initial_state
        )

        results.append({

            "case_id": case["id"],

            "metrics": result.get(
                "evaluation_metrics",
                {}
            )
        })

    return results


def run_adversarial_evaluations():

    with open(

        "src/evaluation/adversarial_dataset.json",

        "r",

        encoding="utf-8"

    ) as f:

        adversarial_cases = json.load(f)

    blocked_count = 0

    for case in adversarial_cases:

        initial_state = {

            "messages": [

                HumanMessage(
                    content=case["query"]
                )
            ],

            "dataset_path": DATASET_PATH,

            "thread_id": f"adv_{case['id']}"
        }

        result = graph.invoke(
            initial_state
        )

        execution_status = result.get(
            "execution_status",
            ""
        )

        if execution_status == "BLOCKED":
            blocked_count += 1

    return {

        "blocked_attacks": blocked_count,

        "total_attacks": len(adversarial_cases)
    }


def main():

    standard_results = run_standard_evaluations()

    adversarial_results = run_adversarial_evaluations()

    print("\nSTANDARD EVALUATIONS:\n")

    for result in standard_results:

        print(result)

    print("\nADVERSARIAL RESULTS:\n")

    print(adversarial_results)

    # =====================================================
    # CI/CD EXIT CODE
    # =====================================================

    failed_cases = 0

    for result in standard_results:

        metrics = result["metrics"]

        if not metrics.get(
            "passed_thresholds",
            False
        ):

            failed_cases += 1

    if failed_cases > 0:

        print(
            f"\nFAILED CASES: {failed_cases}"
        )

        sys.exit(1)

    print("\nALL EVALUATIONS PASSED")

    sys.exit(0)


if __name__ == "__main__":

    main()