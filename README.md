# Predictive Insurance Risk Analysis

[![CI](https://github.com/GebSenait/Predictive-Insurance-Risk-Analysis/actions/workflows/ci.yml/badge.svg?branch=task-dev)](https://github.com/GebSenait/Predictive-Insurance-Risk-Analysis/actions/workflows/ci.yml)

## Business Problem

Insurance pricing decisions rely on predictive models, but stakeholders struggle to interpret and trust technical outputs. Mis-priced policies lead to adverse selection, under-reserving, and regulatory risk. There is a need for a **transparent, justifiable, automated decision system** that connects model outputs directly to pricing actions.

## Solution

This project delivers a **production-ready ML pipeline** that:

1. **Trains** multiple regression and classification models on insurance data
2. **Selects** the best-performing model automatically
3. **Generates** a structured JSON decision summary explaining *which* model was chosen, *why*, and *what it means* for pricing
4. **Passes** a comprehensive test suite via CI on every push

The pipeline uses DVC-tracked data in production and synthetic fixtures in tests, ensuring full reproducibility without exposing sensitive data.

## Success Metrics

| Metric | Target | Status |
|--------|--------|--------|
| Unit tests | >= 5 passing | 21 passing |
| CI pipeline | Green on task-dev | Active |
| Decision JSON | Auto-generated | `results/decision_summary.json` |
| Modular architecture | Clean separation | `src/{data,models,evaluation,decision}` |
| Test isolation | Synthetic only | No DVC dependency in tests |

## Repository Structure

```
predictive-insurance-risk-analysis/
├── .github/workflows/
│   └── ci.yml                    # CI pipeline (pytest, fail on failure)
├── src/
│   ├── data/
│   │   ├── loaders.py            # Data loading with file_path param
│   │   └── preprocessing.py      # Missing values, features, encoding, split
│   ├── models/
│   │   ├── trainer.py            # Regression + classification training
│   │   └── selector.py           # Automated best-model selection
│   ├── evaluation/
│   │   └── metrics.py            # RMSE, R², accuracy, F1, loss ratio
│   ├── decision/
│   │   └── justification.py      # JSON decision summary builder
│   └── utils/
│       ├── config.py             # YAML config loader
│       └── logger.py             # Structured logging
├── scripts/
│   └── run_pipeline.py           # End-to-end pipeline orchestrator
├── tests/
│   ├── test_data.py              # Data loading & preprocessing tests
│   ├── test_model_selector.py    # Training & selection tests
│   ├── test_metrics.py           # Metric computation tests
│   ├── test_justification.py     # Decision JSON tests
│   └── fixtures/
│       └── sample_insurance_data.csv  # Synthetic 12-row dataset
├── results/
│   └── decision_summary.json     # Auto-generated decision artifact
├── config/
│   └── config.yaml
├── requirements/
│   ├── base.txt
│   └── dev.txt
└── pyproject.toml
```

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

### Running the Production Pipeline (requires DVC data)

```bash
dvc pull
python scripts/run_pipeline.py
```

This generates `results/decision_summary.json` with the selected model and business justification.

## Data Strategy

| Context | Data Source | Notes |
|---------|------------|-------|
| **Production** | `data/raw/MachineLearningRating_v3.txt` (DVC-tracked, ~529 MB) | Requires `dvc pull` |
| **Testing** | `tests/fixtures/sample_insurance_data.csv` (12 rows, synthetic) | Always available, no DVC needed |

## Architecture

The pipeline follows a strict modular separation of concerns:

- **`src/data/`** -- Loading and preprocessing (missing values, feature engineering, encoding)
- **`src/models/`** -- Training suite (Linear, Decision Tree, Random Forest, Gradient Boosting) + automated selection
- **`src/evaluation/`** -- Standalone metric functions (RMSE, R-squared, accuracy, precision, recall, F1, loss ratio)
- **`src/decision/`** -- Business-aligned JSON justification output
- **`scripts/run_pipeline.py`** -- Lightweight orchestration

## Decision Summary Output

The pipeline auto-generates `results/decision_summary.json`:

```json
{
  "selected_model": "RandomForestRegressor",
  "task_type": "regression",
  "metric_name": "r2",
  "metric_score": 0.8523,
  "timestamp": "2026-02-15T16:15:24.964656+00:00",
  "business_impact": "The selected regression model achieves an R-squared of 0.8523..."
}
```

## Development

### Branch Discipline

- `main` -- Protected, stable releases only
- `task-dev` -- Active development branch

### Commit Convention

```
<type>: <description>
```

Types: `feat`, `fix`, `refactor`, `test`, `ci`, `docs`

### Running Tests

```bash
pytest tests/ -v
```

All 21 tests run in under 25 seconds using only synthetic data.

## License

See [LICENSE](LICENSE) file for details.

