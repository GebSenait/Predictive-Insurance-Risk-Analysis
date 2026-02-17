"""Build a reproducible model benchmark summary artifact.

Reads task4 results and extracts the best model for each sub-task into
a compact JSON artifact at ``results/model_benchmark_summary.json``.
"""

import json
from pathlib import Path

RESULTS_PATH = Path("results/task4/task4_results.json")
OUTPUT_PATH = Path("results/model_benchmark_summary.json")


def build_benchmark_summary() -> None:
    """Extract best-model names from task4 results and persist as JSON."""
    with open(RESULTS_PATH) as f:
        results = json.load(f)

    summary = {
        "severity_model": results["severity"]["best_model_name"],
        "premium_model": results["premium"]["best_model_name"],
        "claim_probability_model": results["claim_probability"]["best_model_name"],
    }

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_PATH, "w") as f:
        json.dump(summary, f, indent=4)


if __name__ == "__main__":
    build_benchmark_summary()
