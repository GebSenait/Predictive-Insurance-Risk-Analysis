# Changelog

All notable changes to the Predictive Insurance Risk Analysis (ACIS) project are documented here.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-02-17

### Added

- Model benchmark summary artifact (`results/model_benchmark_summary.json`) for reproducible performance reporting.
- Git commit hash in decision summary (`results/decision_summary.json`) for full traceability.
- Reproducibility test enforcing `random_state=42` in config.
- Sample dataset (`data/raw/MachineLearningRating_sample.txt`) and `scripts/generate_sample_data.py` for local/CI runs without DVC or full 529 MB data.
- Config option `analysis.task4.use_sample_data` and `data.sample_filename` to switch between sample and production data.
- Dependency lock file `requirements/lock.txt` for reproducible installs.
- Final README sections: Model Performance Summary, Governance & Auditability, Reproducibility Guarantee, Operational Readiness, Known Limitations, Release Notes.

### Changed

- Pipeline logging (loguru): start/end and selected model logged in `scripts/run_pipeline.py`.
- README: 32 tests, sample data and benchmark summary in structure; no notebooks.

### Fixed

- Task4 `save_results` dict comprehension for interpretability (NameError on `model_name`).
- Benchmark summarizer uses `best_model_name` from task4 results JSON.

## [0.1.0] - 2024–2025

### Added

- Task 1–4 implementation: repository setup, DVC pipeline, Task 3 hypothesis testing, Task 4 predictive modeling (severity, premium, claim probability).
- Modular pipeline: `src/{data,models,evaluation,decision,analysis}`, automated decision justification, CI (GitHub Actions), 32 unit tests.
- Documentation: docs/task2, task3, task4, guides, config-driven behaviour.
