# Running and Testing Locally

## Overview

This guide explains how to run and test the Task 1 solution locally before committing and pushing to the repository.

## Prerequisites

1. Python 3.9+ installed
2. Virtual environment created and activated
3. Dependencies installed

## Setup Steps

### 1. Initialize Project Directories

```bash
python scripts/setup.py
```

This creates all necessary directories (data, results, logs, etc.)

### 2. Install Dependencies

```bash
# Install base dependencies
pip install -r requirements/base.txt

# Install development dependencies (includes testing tools)
pip install -r requirements/dev.txt
```

### 3. Install Pre-commit Hooks (Optional but Recommended)

```bash
pre-commit install
```

## Running the Solution

### Run Main Analysis Script

```bash
python scripts/run_analysis.py
```

This will:
- Load configuration from `config/config.yaml`
- Set up logging
- Execute Task 1 analysis (once implemented)

### Run with Custom Configuration

You can modify `config/config.yaml` to customize:
- Data paths
- Logging levels
- Analysis parameters

## Testing Locally

### Run All Tests

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run with coverage report
pytest --cov=src --cov-report=html
```

### Run Specific Tests

```bash
# Run only unit tests
pytest tests/unit/

# Run specific test file
pytest tests/unit/test_loaders.py

# Run specific test function
pytest tests/unit/test_loaders.py::test_load_csv_success
```

### Check Code Quality

```bash
# Format code
black .

# Check formatting (without changes)
black --check .

# Run linter
flake8 src tests scripts

# Type checking
mypy src --ignore-missing-imports
```

## Development Workflow

### Recommended Local Workflow

1. **Make Changes**
   ```bash
   # You're on develop branch
   git status  # Check current status
   ```

2. **Test Your Changes**
   ```bash
   # Run tests
   pytest
   
   # Run the main script
   python scripts/run_analysis.py
   
   # Check code quality
   black --check .
   flake8 src tests scripts
   ```

3. **Stage Changes**
   ```bash
   git add .
   # Or add specific files
   git add src/analysis/task1/
   ```

4. **Commit Changes**
   ```bash
   git commit -m "feat(task1): implement analysis module"
   ```

5. **Push to Remote** (when ready)
   ```bash
   git push origin develop
   ```

## Testing Before Commit

### Pre-commit Checks

If you installed pre-commit hooks, they will automatically run when you commit:

```bash
git commit -m "your message"
# Pre-commit hooks run automatically
```

### Manual Pre-commit Checks

You can also run pre-commit checks manually:

```bash
pre-commit run --all-files
```

## Common Issues

### Import Errors

If you get import errors:
```bash
# Make sure you're in the project root
cd "d:\Senait Doc\KAIM 8 Doc\Predictive Insurance Risk Analysis"

# Verify Python path
python -c "import sys; print(sys.path)"
```

### Module Not Found

If modules aren't found:
```bash
# Install in development mode (if using setuptools)
pip install -e .

# Or ensure project root is in PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```

### Configuration File Not Found

If config.yaml is not found:
```bash
# Verify config file exists
ls config/config.yaml

# Or create it from template
cp config/config.yaml.example config/config.yaml
```

## Running Jupyter Notebooks

If you're using notebooks for exploration:

```bash
# Start Jupyter Lab
jupyter lab

# Or Jupyter Notebook
jupyter notebook
```

Navigate to `notebooks/exploratory/` to create your analysis notebooks.

## Debugging

### Using Python Debugger

Add breakpoints in your code:
```python
import pdb; pdb.set_trace()
```

### Using VS Code Debugger

1. Set breakpoints in your code
2. Press F5
3. Select "Python: Current File"

### Verbose Logging

Modify `config/config.yaml`:
```yaml
logging:
  level: "DEBUG"  # Change from INFO to DEBUG
```

## Best Practices

1. **Test Before Committing**: Always run tests locally before committing
2. **Check Code Quality**: Run linting and formatting checks
3. **Small Commits**: Make small, focused commits
4. **Descriptive Messages**: Use conventional commit format
5. **Test Coverage**: Aim for 80%+ test coverage

## Next Steps

- Implement Task 1 specific analysis in `src/analysis/task1/`
- Create visualizations and save to `results/figures/`
- Generate reports and save to `results/reports/`
- Write tests for your implementation
- Document your findings

---

**Remember**: You can develop, test, and run everything locally before committing and pushing. This is the recommended workflow!

