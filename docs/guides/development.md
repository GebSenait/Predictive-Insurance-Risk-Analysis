# Development Setup Guide

## Development Environment

### Required Tools

- Python 3.9+
- Git
- IDE (VS Code, PyCharm, etc.)
- Terminal/Command Prompt

### Recommended VS Code Extensions

- Python
- Pylance
- Black Formatter
- GitLens
- Pytest

## Development Workflow

### 1. Fork and Clone

```bash
git clone <your-fork-url>
cd predictive-insurance-risk-analysis
```

### 2. Create Development Branch

```bash
git checkout -b develop
```

### 3. Create Feature Branch

```bash
git checkout -b feature/your-feature-name
```

### 4. Development Cycle

1. Make changes
2. Run tests: `pytest`
3. Format code: `black .`
4. Check linting: `flake8 src tests scripts`
5. Commit: `git commit -m "feat(scope): description"`
6. Push: `git push origin feature/your-feature-name`
7. Create Pull Request

## Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test file
pytest tests/unit/test_loaders.py

# Run with verbose output
pytest -v
```

## Code Formatting

```bash
# Format code
black .

# Check formatting without changes
black --check .

# Sort imports
isort .
```

## Type Checking

```bash
mypy src --ignore-missing-imports
```

## Pre-commit Hooks

Pre-commit hooks automatically run before each commit:

```bash
# Install hooks
pre-commit install

# Run manually
pre-commit run --all-files
```

## Debugging

### Using VS Code

1. Set breakpoints in code
2. Press F5 to start debugging
3. Select "Python: Current File" configuration

### Using pdb

```python
import pdb; pdb.set_trace()
```

## Next Steps

- Read [Contributing Guidelines](../../CONTRIBUTING.md)
- Review [Code Style Guide](code-style.md)

