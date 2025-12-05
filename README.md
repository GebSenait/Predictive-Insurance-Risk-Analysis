# Predictive Insurance Risk Analysis

## Project Overview

This repository contains the implementation for the Predictive Insurance Risk Analysis project. The project focuses on building a robust, production-ready data analysis pipeline following industry best practices with full reproducibility and auditability for financial/insurance regulatory compliance.

**Current Status:**
- ✅ **Task 1**: Repository infrastructure and code quality setup (Complete)
- ✅ **Task 2**: Reproducible & Auditable Data Pipeline with DVC (Complete)

## Repository Structure

```
predictive-insurance-risk-analysis/
├── .github/
│   ├── workflows/
│   │   ├── ci.yml
│   │   ├── code-quality.yml
│   │   └── release.yml
│   ├── ISSUE_TEMPLATE/
│   │   ├── bug_report.md
│   │   └── feature_request.md
│   └── PULL_REQUEST_TEMPLATE.md
├── .gitignore
├── .pre-commit-config.yaml
├── CHANGELOG.md
├── CONTRIBUTING.md
├── LICENSE
├── README.md
├── docs/
│   ├── architecture/
│   ├── api/
│   ├── guides/
│   ├── task1/
│   └── task2/
├── src/
│   ├── data/
│   │   ├── __init__.py
│   │   ├── loaders.py
│   │   └── validators.py
│   ├── analysis/
│   │   ├── __init__.py
│   │   └── task1/
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── logger.py
│   │   └── config.py
│   └── __init__.py
├── tests/
│   ├── unit/
│   ├── integration/
│   └── fixtures/
├── notebooks/
│   └── exploratory/
├── scripts/
│   ├── setup.py
│   └── run_analysis.py
├── config/
│   └── config.yaml
├── requirements/
│   ├── base.txt
│   ├── dev.txt
│   └── prod.txt
└── pyproject.toml
```

## Getting Started

### Prerequisites

- Python 3.9+
- Git
- pip or conda

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd predictive-insurance-risk-analysis
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements/base.txt
pip install -r requirements/dev.txt
```

4. Install pre-commit hooks:
```bash
pre-commit install
```

5. Set up DVC (Data Version Control):
```bash
# On Windows (PowerShell)
.\scripts\setup_dvc.ps1

# On Unix/Linux/Mac
chmod +x scripts/setup_dvc.sh
./scripts/setup_dvc.sh
```

6. Pull data from DVC remote:
```bash
dvc pull
```

### Running the Analysis

```bash
python scripts/run_analysis.py
```

## Data Version Control (DVC)

This project uses **DVC (Data Version Control)** to ensure full reproducibility and auditability of data pipelines, meeting financial/insurance regulatory requirements.

### Quick Start with DVC

1. **Pull tracked data:**
   ```bash
   dvc pull
   ```

2. **Check data status:**
   ```bash
   dvc status
   ```

3. **View tracked files:**
   ```bash
   dvc list data/raw
   ```

### Reproducing the Pipeline

To reproduce any analysis at a specific point in time:

1. **Checkout the desired Git commit:**
   ```bash
   git checkout <commit-hash>
   ```

2. **Pull the corresponding data version:**
   ```bash
   dvc pull
   ```

3. **Run the analysis:**
   ```bash
   python scripts/run_analysis.py
   ```

### DVC Remote Storage

- **Location**: `dvc-storage/` (local directory)
- **Remote Name**: `local-storage`
- **Configuration**: `.dvc/config`

The remote storage is configured to use a local directory for versioned data. All data files are tracked via `.dvc` metadata files committed to Git, while actual data is stored in the remote storage.

### Historical Data Versions

To access historical versions of data:

```bash
# List all versions
git log --oneline data/raw/MachineLearningRating_v3.txt.dvc

# Checkout a specific version
git checkout <commit-hash> data/raw/MachineLearningRating_v3.txt.dvc
dvc checkout data/raw/MachineLearningRating_v3.txt.dvc
```

For detailed DVC documentation, see [docs/task2/README.md](docs/task2/README.md).

## Development Workflow

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed development guidelines.

### Branch Naming Convention

- `feature/description` - New features
- `bugfix/description` - Bug fixes
- `hotfix/description` - Critical production fixes
- `docs/description` - Documentation updates
- `refactor/description` - Code refactoring

### Commit Message Format

Follow [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>(<scope>): <subject>

<body>

<footer>
```

Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

## Testing

```bash
pytest tests/
```

## Code Quality

This project uses:
- `black` for code formatting
- `flake8` for linting
- `mypy` for type checking
- `pytest` for testing

## Documentation

Full documentation is available in the `docs/` directory.

## License

See [LICENSE](LICENSE) file for details.

## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) before submitting pull requests.

