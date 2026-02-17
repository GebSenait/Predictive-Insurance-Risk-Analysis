# Predictive Insurance Risk Analysis

[![CI](https://github.com/GebSenait/Predictive-Insurance-Risk-Analysis/actions/workflows/ci.yml/badge.svg?branch=task-dev)](https://github.com/GebSenait/Predictive-Insurance-Risk-Analysis/actions/workflows/ci.yml)

**Description:** production-ready pipeline for AlphaCare Insurance Solutions (ACIS) that turns raw insurance data into statistically validated risk insights and model-backed pricing decisions, with full reproducibility and audit-ready artifacts.

## Executive Summary

This capstone delivers an end-to-end Predictive Insurance Risk Analysis system: data ingestion, hypothesis testing on risk drivers, multi-model pricing and severity estimation, and automated decision justification (JSON artifacts that explain which model was chosen and why). All of it is versioned (DVC), tested (32 unit tests), and CI-validated so that pricing recommendations are traceable to a specific commit, dataset, and metric.

## Table of Contents

- [Executive Summary](#executive-summary)
- [Business Problem](#business-problem)
- [Why This Matters for Finance](#why-this-matters-for-finance)
- [Solution Overview](#solution-overview)
- [Key Results](#key-results)
- [What Makes This Different](#what-makes-this-different)
- [Evidence & Reliability](#evidence--reliability)
- [Project Structure](#project-structure)
- [Quick Start](#quick-start)
- [Technical Details](#technical-details)
- [Future Improvements](#future-improvements)
- [Lessons Learned](#lessons-learned)
- [Author](#author)
- [License & Contributing](#license--contributing)

## Business Problem

Pricing and risk decisions depend on models, but stakeholders often cannot see why a model was chosen or what it means for the business. In addition:

- **Model choice is opaque** — no single artifact that explains selection and impact.
- **Results are hard to reproduce** — changing data or code can silently change outputs.
- **Validation is manual** — logic changes can slip through without automated checks.
- **Workflows are fragmented** — hypothesis testing and modeling live in separate, unaligned flows.

## Why This Matters for Finance

- **Auditability:** Regulators and internal audit need to see why a price was chosen. This project produces structured decision artifacts (e.g. `decision_summary.json`) with model name, metric score, timestamp, and git commit — not just a number.
- **Reproducibility:** Re-running on the same commit and DVC state yields the same outputs. That supports compliance and dispute resolution.
- **Trust:** Actuarial and underwriting teams get plain-language business impact for the chosen model, plus SHAP/LIME-style interpretability for Task 4, so technical choices are explainable.

## Solution Overview

The project tackles these with a modular, config-driven pipeline:

1. **Automated decision justification** — After training, the best model is selected by a fixed metric (e.g. R² or F1); a JSON artifact records the choice, score, timestamp, git commit, and a short business interpretation.
2. **DVC for data** — Production data is versioned; config and code live in Git. Same commit + same DVC state ⇒ same results.
3. **Shared data and evaluation** — One `src/` layout: `data/`, `models/`, `evaluation/`, `decision/`, plus task-specific `analysis/task3/` and `analysis/task4/`. All tasks use the same loaders and metrics.
4. **CI and tests** — 32 unit tests run on every push (Python 3.9–3.11); no DVC or production data required for tests.

Further implementation detail (design principles, code quality tools, branch strategy) is in [docs/](docs/) and [CONTRIBUTING.md](CONTRIBUTING.md).

## Key Results

- **Task 3 (Statistical validation):** Four hypotheses tested (provinces, zip codes, margin by region, gender) at α = 0.05. Geographic risk differences were significant; province- and postal-code-level pricing tiers are supported. See [docs/task3/README.md](docs/task3/README.md).
- **Task 4 (Predictive modeling):** Three tasks — claim severity (regression), premium (regression), claim probability (classification). Each compares five algorithms; best model is chosen by test R² or F1. Risk-based formula: *Premium = P(Claim) × Predicted Severity + expense loading + margin.* SHAP/LIME used for interpretability. See [docs/task4/README.md](docs/task4/README.md).
- **Decision artifact:** Each pipeline run produces `results/decision_summary.json` (and optionally `results/model_benchmark_summary.json`) with selected model, metric, timestamp, and git commit for full traceability.

## What Makes This Different

- **Decision artifact, not just a model:** Every run writes a JSON summary (selected model, score, business impact). No "black box" recommendation.
- **One pipeline, one data contract:** Task 3 (hypothesis testing) and Task 4 (predictive modeling) share the same loaders, preprocessing, and config — no disconnected scripts.
- **Data versioning with DVC:** The 529 MB production dataset is tracked; any historical version can be restored for re-runs or audits.
- **Automated quality gate:** 32 tests and GitHub Actions CI; a failing test blocks the pipeline. No "continue on error."

## Evidence & Reliability

- **32 tests** cover data loading, preprocessing, model training/selection, metrics, decision JSON structure, and config (e.g. fixed `random_state=42`). Run: `pytest tests/ -v`. Tests use synthetic or sample data only; no DVC pull required.
- **CI:** GitHub Actions runs the full suite on push to `task-dev` and on PRs to `main`. Any failure blocks the pipeline.
- **Reproducibility:** Same Git commit, DVC state, and `config/config.yaml` produce the same outputs (fixed seed, config-driven splits, and lock file).

## Project Structure

```
├── src/           # data, models, evaluation, decision, analysis (task3, task4), utils
├── scripts/       # run_pipeline.py, run_task3.py, run_task4.py, generate_sample_data.py, setup.py
├── tests/         # 32 unit tests (data, metrics, selector, justification, config, loaders, validators, reproducibility)
├── config/        # config.yaml (paths, alpha, random_state, task4 hyperparameters)
├── data/raw/      # DVC-tracked production data + optional MachineLearningRating_sample.txt for local/CI
├── results/       # decision_summary.json, model_benchmark_summary.json, task4/task3 outputs
├── docs/          # task2, task3, task4, guides, architecture
└── requirements/  # base.txt, dev.txt, prod.txt, lock.txt
```

Full directory tree and design principles: [docs/IMPLEMENTATION_GUIDE.md](docs/IMPLEMENTATION_GUIDE.md) · [docs/architecture/README.md](docs/architecture/README.md)

## Quick Start

```bash
git clone https://github.com/GebSenait/Predictive-Insurance-Risk-Analysis.git
cd Predictive-Insurance-Risk-Analysis
python -m venv venv
# Windows: venv\Scripts\activate   |   Unix: source venv/bin/activate
pip install -r requirements/base.txt
pip install -r requirements/dev.txt
```

Run tests (no data download):

```bash
pytest tests/ -v
```

Run the pipeline (after `dvc pull` for full data, or use the included sample data with `use_sample_data: true` in config):

```bash
python scripts/run_pipeline.py
python scripts/run_task3.py
python scripts/run_task4.py
python src/evaluation/benchmark_summary.py
```

## Technical Details

- **Data:** Production: `data/raw/MachineLearningRating_v3.txt` (DVC, ~529 MB). Sample: `MachineLearningRating_sample.txt` (12k rows, same schema) for local/CI. Tests use `tests/fixtures/sample_insurance_data.csv` or in-memory DataFrames.
- **Models:** Task 4: Linear Regression, Decision Tree, Random Forest, Gradient Boosting, XGBoost (regression and classification). Best model by test R² (regression) or F1 (classification). Hyperparameters in `config/config.yaml` (e.g. `random_state: 42`, `test_size: 0.3`).
- **Evaluation:** RMSE, R², accuracy, precision, recall, F1, loss ratio. Decision logic and benchmark summary in `src/decision/` and `src/evaluation/`.

More: [docs/task3/README.md](docs/task3/README.md) · [docs/task4/README.md](docs/task4/README.md) · [docs/task2/README.md](docs/task2/README.md)

## Future Improvements

With more time, next steps would be:

- REST API scoring endpoint for real-time quotes
- Drift detection on inputs and targets
- Scheduled retraining (e.g. quarterly)
- Docker containerization for deployment

The current design (modular pipeline, config-driven, lock file, traceability) supports these extensions without a rewrite.

## Lessons Learned

- One artifact that explains the decision (the decision JSON) reduced "why this model?" questions and aligned DS with business.
- DVC + fixed seed + config made re-runs and audits straightforward; the lock file and reproducibility test lock the environment and seed.
- Unifying Task 3 and Task 4 around shared data and evaluation reduced duplication and ensured metric consistency.
- Sample dataset (same schema as production) enabled CI and development without requiring the full 529 MB file.

## Author

**Senait Gebreab** — Data Science & ML Test Engineer  
Repository: [https://github.com/GebSenait/Predictive-Insurance-Risk-Analysis](https://github.com/GebSenait/Predictive-Insurance-Risk-Analysis)

## License & Contributing

- **License:** [LICENSE](LICENSE)
- **Contributing:** [CONTRIBUTING.md](CONTRIBUTING.md)
