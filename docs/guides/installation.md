# Installation Guide

## Prerequisites

- Python 3.9 or higher
- pip or conda package manager
- Git

## Step-by-Step Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd predictive-insurance-risk-analysis
```

### 2. Create Virtual Environment

**Using venv:**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

**Using conda:**
```bash
conda create -n insurance-analysis python=3.9
conda activate insurance-analysis
```

### 3. Install Dependencies

```bash
pip install -r requirements/base.txt
pip install -r requirements/dev.txt  # For development
```

### 4. Install Pre-commit Hooks

```bash
pre-commit install
```

### 5. Initialize Project Directories

```bash
python scripts/setup.py
```

### 6. Verify Installation

```bash
pytest tests/ -v
```

## Troubleshooting

### Common Issues

1. **Import errors**: Ensure virtual environment is activated
2. **Permission errors**: Use `sudo` on Linux/Mac or run as administrator on Windows
3. **Package conflicts**: Create a fresh virtual environment

## Next Steps

- Read the [Development Setup Guide](development.md)
- Check out the [Running Analyses Guide](running-analyses.md)

