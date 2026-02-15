# Predictive Insurance Risk Analysis

[![CI](https://github.com/GebSenait/Predictive-Insurance-Risk-Analysis/actions/workflows/ci.yml/badge.svg?branch=task-dev)](https://github.com/GebSenait/Predictive-Insurance-Risk-Analysis/actions/workflows/ci.yml)

**Author:** Senait Gebreab | Data Science Engineer

## Project Overview

This repository implements a **production-ready Predictive Insurance Risk Analysis pipeline** for AlphaCare Insurance Solutions (ACIS). The project delivers a full data science lifecycle -- from raw data ingestion and statistical validation through predictive modeling to automated, business-aligned decision outputs -- all backed by reproducible data versioning, modular architecture, and continuous integration.

**Project Status:**

| Task | Description | Status |
|------|-------------|--------|
| Task 1 | Repository infrastructure and code quality setup | Complete |
| Task 2 | Reproducible & Auditable Data Pipeline with DVC | Complete |
| Task 3 | Statistical Validation of Risk Drivers (A/B Hypothesis Testing) | Complete |
| Task 4 | Predictive Modeling for Risk-Based Pricing and Severity Estimation | Complete |
| Enhancement | Modular pipeline with automated decision justification, CI/CD, and test suite | Complete |

---

## Business Problem

Insurance pricing decisions rely on predictive models, but stakeholders across actuarial, underwriting, and executive teams struggle to **interpret and trust technical outputs**. The core gaps are:

- **Opaque model selection** -- Models are trained and compared, but there is no structured artifact explaining *why* a particular model was chosen and *what it means* for the business.
- **Fragile reproducibility** -- Without data versioning, results change silently when underlying data is updated, eroding trust in pricing recommendations.
- **No automated validation** -- Manual testing allows regressions to slip into production logic undetected.
- **Disconnected analysis stages** -- Statistical validation (hypothesis testing) and predictive modeling exist as separate workflows with no unified pipeline or shared data contract.

## Proposed Solution

This project addresses each gap with a layered, modular architecture:

| Gap | Solution | Implementation |
|-----|----------|----------------|
| Opaque model selection | **Automated decision justification** -- a JSON artifact with selected model, score, timestamp, and plain-language business impact | `src/decision/justification.py` |
| Fragile reproducibility | **DVC data versioning** -- 529 MB production dataset tracked with content-addressable storage; any historical version recoverable | `data/raw/*.dvc` |
| No automated validation | **31 unit tests + GitHub Actions CI** -- tests run on every push; pipeline fails on any test failure | `tests/` + `.github/workflows/ci.yml` |
| Disconnected stages | **Unified modular pipeline** -- shared data loaders, preprocessing, and evaluation metrics across all tasks | `src/{data,models,evaluation,decision}/` |

---

## Key Results and Insights

### Task 3: Statistical Validation of Risk Drivers

Four null hypotheses were tested using appropriate statistical methods (t-test, chi-square, Mann-Whitney U) at significance level alpha = 0.05:

| Hypothesis | Metric Tested | Statistical Test | Key Finding |
|------------|---------------|------------------|-------------|
| H0: No risk differences across **provinces** | Claim Frequency, Severity | Chi-square, Mann-Whitney U | Significant differences detected -- geographic pricing tiers recommended |
| H0: No risk differences between **zip codes** | Claim Frequency, Severity | Chi-square, Mann-Whitney U | Significant variation -- supports postal-code-based risk segmentation |
| H0: No margin difference between **zip codes** | Margin (Premium - Claims) | t-test / Mann-Whitney U | Profitability varies by region -- pricing adjustments warranted |
| H0: No risk difference between **genders** | Claim Frequency, Severity | Chi-square, Mann-Whitney U | Results inform gender-based risk assessment (subject to regulatory constraints) |

**Business Implication:** Geographic location is a statistically significant risk driver. ACIS should consider province-level and postal-code-level premium adjustments while maintaining regulatory compliance for demographic factors.

### Task 4: Predictive Modeling for Risk-Based Pricing

Three modeling tasks were completed, each comparing 5 algorithms:

**1. Claim Severity Model (Regression)**
- Target: `TotalClaims` for policies with claims > 0
- Algorithms: Linear Regression, Decision Tree, Random Forest, Gradient Boosting, XGBoost
- Selection metric: Highest test R-squared
- Use case: Reserve setting and expected loss estimation

**2. Premium Optimization Model (Regression)**
- Target: `TotalPremium`
- Algorithms: Linear Regression, Decision Tree, Random Forest, Gradient Boosting, XGBoost
- Selection metric: Highest test R-squared
- Use case: Dynamic, data-driven premium pricing

**3. Claim Probability Model (Classification)**
- Target: Binary indicator (1 if claim occurred, 0 otherwise)
- Algorithms: Logistic Regression, Decision Tree, Random Forest, Gradient Boosting, XGBoost
- Selection metric: Highest test F1 score
- Use case: Risk segmentation and the core premium formula

**Risk-Based Premium Formula:**

```
Premium = P(Claim) x Predicted Severity + Expense Loading + Profit Margin
```

**Model Interpretability:** SHAP and LIME analyses identified the top 5-10 features driving each model's predictions, enabling actuaries and underwriters to validate model logic against domain knowledge.

### Pipeline Enhancement: Automated Decision Justification

The pipeline now auto-generates `results/decision_summary.json` after every run:

```json
{
  "selected_model": "RandomForestRegressor",
  "task_type": "regression",
  "metric_name": "r2",
  "metric_score": 0.8523,
  "timestamp": "2026-02-15T16:15:24.964656+00:00",
  "business_impact": "The selected regression model (RandomForestRegressor) achieves an R-squared of 0.8523 on the hold-out test set, explaining 85.2% of the variance in the target variable. This level of accuracy supports data-driven premium pricing and reserve estimation.",
  "model_rankings": [
    { "rank": 1, "model_name": "RandomForestRegressor", "score": 0.8523 }
  ]
}
```

This artifact serves as the bridge between data science outputs and business decision-making -- every pricing recommendation is traceable to a specific model, metric, and timestamp.

---

## Architecture and Code Structure

```
predictive-insurance-risk-analysis/
│
├── .github/workflows/
│   └── ci.yml                          # CI: pytest on push, fails on failure
│
├── src/
│   ├── data/
│   │   ├── loaders.py                  # Data loading (accepts file_path for test injection)
│   │   ├── preprocessing.py            # Missing values, feature engineering, encoding, split
│   │   └── validators.py               # Schema and data quality validation
│   │
│   ├── models/
│   │   ├── trainer.py                  # Regression + classification model training suite
│   │   └── selector.py                 # Automated best-model selection and ranking
│   │
│   ├── evaluation/
│   │   └── metrics.py                  # RMSE, R², accuracy, precision, recall, F1, loss ratio
│   │
│   ├── decision/
│   │   └── justification.py            # Structured JSON decision summary builder
│   │
│   ├── analysis/
│   │   ├── task3/                      # Statistical hypothesis testing modules
│   │   │   ├── hypothesis_testing.py   # Main runner for 4 hypotheses
│   │   │   ├── metrics.py             # Claim frequency, severity, margin, loss ratio
│   │   │   ├── segmentation.py        # A/B group creation
│   │   │   ├── statistical_tests.py   # t-test, Mann-Whitney U, chi-square
│   │   │   ├── reporting.py           # Markdown report with business interpretations
│   │   │   └── visualizations.py      # Summary plots
│   │   └── task4/                      # Predictive modeling modules
│   │       ├── task4_runner.py         # Pipeline orchestrator
│   │       ├── data_preparation.py     # Full preprocessing (508 lines)
│   │       ├── models.py              # 5-algorithm training suite (636 lines)
│   │       ├── interpretability.py    # SHAP and LIME analysis
│   │       └── reporting.py           # Model comparison reports
│   │
│   └── utils/
│       ├── config.py                   # YAML config with dot-notation access
│       └── logger.py                   # Loguru-based structured logging
│
├── scripts/
│   ├── run_pipeline.py                 # End-to-end pipeline (load → train → select → justify)
│   ├── run_task3.py                    # Task 3 statistical testing entry point
│   ├── run_task4.py                    # Task 4 predictive modeling entry point
│   └── check_dependencies.py          # Dependency verification utility
│
├── tests/
│   ├── test_data.py                    # 6 tests: loading, missing values, features, encoding, pipeline
│   ├── test_model_selector.py          # 5 tests: training, selection, ranking, edge cases
│   ├── test_metrics.py                 # 6 tests: regression, classification, loss ratio
│   ├── test_justification.py           # 4 tests: JSON structure, rounding, persistence
│   ├── conftest.py                     # Shared fixtures (synthetic DataFrame, CSV path)
│   └── fixtures/
│       └── sample_insurance_data.csv   # 12-row synthetic dataset (no DVC needed)
│
├── results/
│   └── decision_summary.json           # Auto-generated decision artifact
│
├── config/
│   └── config.yaml                     # Centralized configuration (paths, hyperparameters, alpha)
│
├── data/
│   └── raw/
│       └── MachineLearningRating_v3.txt.dvc  # DVC pointer to 529 MB production dataset
│
├── docs/
│   ├── task3/README.md                 # Detailed Task 3 documentation
│   └── task4/README.md                 # Detailed Task 4 documentation
│
├── requirements/
│   ├── base.txt                        # Core: numpy, pandas, scikit-learn, xgboost, shap, lime, dvc
│   ├── dev.txt                         # Dev: pytest, black, flake8, mypy, pre-commit
│   └── prod.txt                        # Production dependencies
│
└── pyproject.toml                      # Build config, tool settings (black, isort, mypy, pytest)
```

### Design Principles

- **Type hints and docstrings** on every public function
- **Named constants** -- no magic numbers (e.g., `DEFAULT_RANDOM_STATE = 42`, `DEFAULT_TEST_SIZE = 0.3`)
- **Separation of concerns** -- data, models, evaluation, and decision layers are independently testable
- **Dependency injection** -- `load_insurance_data(file_path=...)` lets tests inject synthetic data without touching production files
- **Fail-fast CI** -- no `continue-on-error` in the test job; a broken test blocks the pipeline

---

## Getting Started

### Prerequisites

- Python 3.9+
- Git
- pip

### Installation

```bash
git clone https://github.com/GebSenait/Predictive-Insurance-Risk-Analysis.git
cd Predictive-Insurance-Risk-Analysis
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements/base.txt
pip install -r requirements/dev.txt
```

### Running Tests (no DVC data needed)

```bash
pytest tests/ -v
```

### Running the Analysis

```bash
# Pull production data (529 MB, one-time)
dvc pull

# Run statistical hypothesis testing
python scripts/run_task3.py

# Run predictive modeling (claim severity, premium, claim probability)
python scripts/run_task4.py

# Run the unified pipeline (train → select → decision JSON)
python scripts/run_pipeline.py
```

### Output Files

| Script | Output | Description |
|--------|--------|-------------|
| `run_task3.py` | `results/task3_results.json` | Complete hypothesis test results |
| | `results/reports/task3_statistical_report.md` | Business-ready markdown report |
| | `results/figures/hypothesis_test_summary.png` | P-value visualization |
| `run_task4.py` | `results/task4/task4_results.json` | All model metrics |
| | `results/reports/task4_modeling_report.md` | Model comparison report |
| | `results/task4/task4_top_features.json` | SHAP/LIME feature rankings |
| `run_pipeline.py` | `results/decision_summary.json` | Automated decision justification |

---

## Data Strategy

| Context | Data Source | Size | Notes |
|---------|------------|------|-------|
| **Production** | `data/raw/MachineLearningRating_v3.txt` | ~529 MB | DVC-tracked; requires `dvc pull` |
| **Testing** | `tests/fixtures/sample_insurance_data.csv` | 12 rows | Synthetic; always available, zero DVC dependency |

### Data Version Control (DVC)

This project uses DVC to ensure full reproducibility and auditability for financial/insurance regulatory compliance.

```bash
# Pull tracked data
dvc pull

# Check data status
dvc status

# Recover a historical data version
git checkout <commit-hash> data/raw/MachineLearningRating_v3.txt.dvc
dvc checkout data/raw/MachineLearningRating_v3.txt.dvc
```

- **Remote storage:** `dvc-storage/` (local directory)
- **Configuration:** `.dvc/config`
- All data files are tracked via `.dvc` metadata committed to Git, while actual data resides in the remote store.

For detailed DVC documentation, see [docs/task2/README.md](docs/task2/README.md).

---

## Test Results and Evidence

**31 unit tests** pass in under 11 seconds using only synthetic data (executed inside Python venv):

```
tests/test_data.py::TestLoadInsuranceData::test_load_fixture_csv           PASSED
tests/test_data.py::TestLoadInsuranceData::test_load_missing_file_raises   PASSED
tests/test_data.py::TestPreprocessing::test_handle_missing_values          PASSED
tests/test_data.py::TestPreprocessing::test_engineer_features_adds_columns PASSED
tests/test_data.py::TestPreprocessing::test_encode_categoricals            PASSED
tests/test_data.py::TestPreprocessing::test_run_preprocessing_pipeline     PASSED
tests/test_model_selector.py::TestModelTraining::test_regression_models    PASSED
tests/test_model_selector.py::TestModelTraining::test_classification_models PASSED
tests/test_model_selector.py::TestModelSelector::test_select_best_regression PASSED
tests/test_model_selector.py::TestModelSelector::test_select_raises_on_empty PASSED
tests/test_model_selector.py::TestModelSelector::test_get_ranking_sorted   PASSED
tests/test_metrics.py::TestRegressionMetrics::test_perfect_predictions     PASSED
tests/test_metrics.py::TestRegressionMetrics::test_rmse_positive           PASSED
tests/test_metrics.py::TestClassificationMetrics::test_perfect_classification PASSED
tests/test_metrics.py::TestClassificationMetrics::test_zero_division_handled PASSED
tests/test_metrics.py::TestLossRatio::test_basic_ratio                     PASSED
tests/test_metrics.py::TestLossRatio::test_zero_premium_safe               PASSED
tests/test_justification.py::TestBuildDecisionSummary::test_required_keys  PASSED
tests/test_justification.py::TestBuildDecisionSummary::test_metric_rounded PASSED
tests/test_justification.py::TestBuildDecisionSummary::test_business_impact PASSED
tests/test_justification.py::TestSaveDecisionSummary::test_json_written    PASSED
tests/unit/test_config.py::test_load_config_success                        PASSED
tests/unit/test_config.py::test_load_config_file_not_found                 PASSED
tests/unit/test_config.py::test_get_config                                 PASSED
tests/unit/test_loaders.py::test_dataloader_init                           PASSED
tests/unit/test_loaders.py::test_load_csv_success                          PASSED
tests/unit/test_loaders.py::test_load_csv_file_not_found                   PASSED
tests/unit/test_validators.py::test_validate_schema_success                PASSED
tests/unit/test_validators.py::test_validate_schema_missing_column         PASSED
tests/unit/test_validators.py::test_check_missing_values_no_missing        PASSED
tests/unit/test_validators.py::test_check_duplicates_no_duplicates         PASSED

======================== 31 passed in 10.57s ========================
```

| Test File | Tests | What It Validates |
|-----------|-------|-------------------|
| `test_data.py` | 6 | CSV loading from fixture, FileNotFoundError, missing-value handling, feature engineering (HasClaim, LossRatio, ProfitMargin), categorical encoding, full preprocessing pipeline split |
| `test_model_selector.py` | 5 | Regression training returns valid metrics, classification training returns valid metrics, best-model selection picks highest R-squared, empty-input raises ValueError, ranking is sorted descending |
| `test_metrics.py` | 6 | Perfect regression gives RMSE=0/R-squared=1, RMSE is non-negative, perfect classification gives all metrics=1, zero-division is handled safely, loss ratio basic computation, zero-premium returns 0 |
| `test_justification.py` | 4 | Decision JSON contains all required keys, metric score is rounded to 6 decimals, business impact is non-empty string, JSON is written to disk and parseable |
| `unit/test_config.py` | 3 | YAML config loading, FileNotFoundError for missing config, dot-notation config access |
| `unit/test_loaders.py` | 3 | DataLoader class initialisation, CSV load success, FileNotFoundError for missing CSV |
| `unit/test_validators.py` | 4 | Schema validation success, missing column detection, missing value check, duplicate row check |

**Test isolation guarantee:** No test imports from `data/raw/`, references DVC, or requires network access. All data is either a 12-row synthetic CSV or an in-memory DataFrame created at test time.

---

## CI/CD Pipeline

The GitHub Actions workflow (`.github/workflows/ci.yml`) runs on every push to `task-dev` and on pull requests to `main`:

- **Matrix testing:** Python 3.9, 3.10, 3.11
- **Strict failure mode:** No `continue-on-error` -- any test failure blocks the pipeline
- **Dependency caching:** pip cache for faster re-runs
- **Scope:** Runs all 31 tests across `tests/` (pipeline tests + legacy unit tests)

---

## Development Workflow

### Branch Discipline

| Branch | Purpose |
|--------|---------|
| `main` | Protected; stable, reviewed releases only |
| `task-dev` | Active development; CI runs on every push |

### Commit Convention

This project follows [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>: <description>
```

| Type | Usage |
|------|-------|
| `feat` | New feature or capability |
| `fix` | Bug fix |
| `refactor` | Code restructuring without behavior change |
| `test` | Adding or updating tests |
| `ci` | CI/CD configuration changes |
| `docs` | Documentation updates |

### Commit History (task-dev)

```
c341201 docs: add CI badge and interim updates
43b6431 ci: add github actions pipeline
f5a7d68 test: add unit tests for core modules
3b737ff feat: add automated decision justification summary
48e84c8 refactor: clean modular architecture and type hints
```

### Code Quality Tools

| Tool | Purpose | Configuration |
|------|---------|---------------|
| `black` | Code formatting (line length 88) | `pyproject.toml` |
| `flake8` | Linting | `pyproject.toml` |
| `mypy` | Static type checking | `pyproject.toml` |
| `isort` | Import sorting (black-compatible) | `pyproject.toml` |
| `pytest` | Testing framework | `pyproject.toml` |
| `pre-commit` | Git hook automation | `.pre-commit-config.yaml` |

---

## Configuration

All parameters are centralized in `config/config.yaml`:

```yaml
data:
  raw_path: "data/raw"

analysis:
  task3:
    alpha: 0.05
    min_samples_province: 1000
  task4:
    random_state: 42
    test_size: 0.3
    n_estimators: 100
    max_depth: 10
    learning_rate: 0.1

output:
  results_path: "results"
```

---

## Detailed Task Documentation

- **Task 3 (Hypothesis Testing):** [docs/task3/README.md](docs/task3/README.md)
- **Task 4 (Predictive Modeling):** [docs/task4/README.md](docs/task4/README.md)

---

## License

See [LICENSE](LICENSE) file for details.

## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) before submitting pull requests.
