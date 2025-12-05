# Project Structure Overview

## Complete Repository Structure

```
predictive-insurance-risk-analysis/
│
├── .github/                          # GitHub configuration
│   ├── workflows/                    # CI/CD workflows
│   │   ├── ci.yml                   # Continuous Integration
│   │   ├── code-quality.yml         # Code quality checks
│   │   └── release.yml              # Release automation
│   ├── ISSUE_TEMPLATE/              # Issue templates
│   │   ├── bug_report.md
│   │   └── feature_request.md
│   └── PULL_REQUEST_TEMPLATE.md     # PR template
│
├── .gitignore                        # Git ignore rules
├── .pre-commit-config.yaml          # Pre-commit hooks configuration
│
├── CHANGELOG.md                      # Version history
├── CONTRIBUTING.md                   # Contribution guidelines
├── LICENSE                           # MIT License
├── PROJECT_STRUCTURE.md             # This file
├── README.md                         # Main project documentation
├── pyproject.toml                    # Python project configuration
│
├── config/                           # Configuration files
│   └── config.yaml                  # Main configuration
│
├── data/                             # Data directory (gitignored)
│   ├── raw/                         # Raw data files
│   │   └── .gitkeep
│   ├── processed/                   # Processed data files
│   │   └── .gitkeep
│   └── external/                    # External data sources
│       └── .gitkeep
│
├── docs/                             # Documentation
│   ├── architecture/                # Architecture documentation
│   │   └── README.md
│   ├── api/                         # API documentation
│   │   └── README.md
│   ├── guides/                      # User guides
│   │   ├── README.md
│   │   ├── development.md
│   │   └── installation.md
│   ├── task1/                       # Task 1 specific docs
│   │   └── README.md
│   ├── EXECUTION_PLAN.md            # Execution plan
│   └── IMPLEMENTATION_GUIDE.md      # Comprehensive implementation guide
│
├── logs/                             # Log files (gitignored)
│   └── .gitkeep
│
├── notebooks/                        # Jupyter notebooks
│   └── exploratory/                 # Exploratory analysis
│       └── README.md
│
├── requirements/                     # Python dependencies
│   ├── base.txt                     # Core dependencies
│   ├── dev.txt                      # Development dependencies
│   └── prod.txt                     # Production dependencies
│
├── results/                          # Analysis results (gitignored)
│   ├── figures/                     # Generated figures
│   │   └── .gitkeep
│   ├── reports/                     # Generated reports
│   │   └── .gitkeep
│   └── .gitkeep
│
├── scripts/                          # Utility scripts
│   ├── run_analysis.py              # Main analysis script
│   └── setup.py                     # Setup script
│
├── src/                              # Source code
│   ├── analysis/                    # Analysis modules
│   │   ├── __init__.py
│   │   └── task1/                   # Task 1 analysis (to be implemented)
│   ├── data/                        # Data handling modules
│   │   ├── __init__.py
│   │   ├── loaders.py               # Data loading
│   │   └── validators.py            # Data validation
│   ├── utils/                       # Utility modules
│   │   ├── __init__.py
│   │   ├── config.py                # Configuration management
│   │   └── logger.py                # Logging utility
│   └── __init__.py
│
└── tests/                            # Test suite
    ├── fixtures/                    # Test fixtures
    │   └── __init__.py
    ├── integration/                 # Integration tests
    │   └── __init__.py
    ├── unit/                        # Unit tests
    │   ├── __init__.py
    │   ├── test_config.py
    │   ├── test_loaders.py
    │   └── test_validators.py
    ├── conftest.py                  # Pytest configuration
    └── __init__.py
```

## Directory Descriptions

### Root Level Files

- **README.md**: Main project documentation and quick start guide
- **CONTRIBUTING.md**: Guidelines for contributors
- **CHANGELOG.md**: Version history and changes
- **LICENSE**: MIT License
- **PROJECT_STRUCTURE.md**: This document - overview of project structure
- **pyproject.toml**: Python project configuration (dependencies, tools, etc.)
- **.gitignore**: Files and directories to exclude from Git
- **.pre-commit-config.yaml**: Pre-commit hooks configuration

### Key Directories

#### `.github/`
GitHub-specific configurations:
- **workflows/**: GitHub Actions CI/CD pipelines
- **ISSUE_TEMPLATE/**: Templates for bug reports and feature requests
- **PULL_REQUEST_TEMPLATE.md**: Template for pull requests

#### `config/`
Configuration files in YAML format:
- **config.yaml**: Main application configuration

#### `data/`
Data storage directories (typically gitignored):
- **raw/**: Original, unprocessed data
- **processed/**: Cleaned and processed data
- **external/**: External data sources

#### `docs/`
Comprehensive documentation:
- **architecture/**: System architecture documentation
- **api/**: API reference documentation
- **guides/**: User and developer guides
- **task1/**: Task 1 specific documentation

#### `src/`
Main source code organized by functionality:
- **data/**: Data loading and validation modules
- **analysis/**: Analysis and modeling modules
- **utils/**: Utility functions (logging, config, etc.)

#### `tests/`
Test suite mirroring source structure:
- **unit/**: Unit tests for individual components
- **integration/**: Integration tests for component interactions
- **fixtures/**: Test data and fixtures

#### `scripts/`
Standalone utility scripts:
- **run_analysis.py**: Main analysis execution script
- **setup.py**: Project setup and initialization script

#### `requirements/`
Python dependency management:
- **base.txt**: Core runtime dependencies
- **dev.txt**: Development dependencies (testing, linting, etc.)
- **prod.txt**: Production-specific dependencies

## File Organization Principles

1. **Modularity**: Clear separation of concerns
2. **Scalability**: Structure supports future growth
3. **Maintainability**: Easy to navigate and understand
4. **Standards**: Follows Python and data science best practices

## Naming Conventions

- **Directories**: lowercase with underscores (`data/`, `src/utils/`)
- **Python files**: lowercase with underscores (`data_loaders.py`)
- **Classes**: PascalCase (`DataLoader`)
- **Functions**: lowercase with underscores (`load_csv`)
- **Constants**: UPPERCASE with underscores (`MAX_SIZE`)

## Getting Started

1. Review [README.md](README.md) for project overview
2. Check [docs/IMPLEMENTATION_GUIDE.md](docs/IMPLEMENTATION_GUIDE.md) for detailed implementation instructions
3. See [docs/EXECUTION_PLAN.md](docs/EXECUTION_PLAN.md) for project timeline
4. Read [CONTRIBUTING.md](CONTRIBUTING.md) for development guidelines

