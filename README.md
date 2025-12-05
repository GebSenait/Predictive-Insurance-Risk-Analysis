# Predictive Insurance Risk Analysis - Task 1

## Project Overview

This repository contains the implementation for Task 1 of the Predictive Insurance Risk Analysis project. The project focuses on building a robust, production-ready data analysis pipeline following industry best practices.

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
│   └── task1/
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

### Running the Analysis

```bash
python scripts/run_analysis.py
```

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

