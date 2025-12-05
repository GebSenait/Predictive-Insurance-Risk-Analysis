# Contributing Guidelines

## Development Workflow

### 1. Branch Strategy

We follow a Git Flow-inspired branching strategy:

- **`main`** - Production-ready code
- **`develop`** - Integration branch for features
- **`feature/*`** - Feature development branches
- **`bugfix/*`** - Bug fix branches
- **`hotfix/*`** - Critical production fixes
- **`release/*`** - Release preparation branches

### 2. Creating a Branch

```bash
# From develop branch
git checkout develop
git pull origin develop
git checkout -b feature/your-feature-name
```

### 3. Commit Message Convention

We follow [Conventional Commits](https://www.conventionalcommits.org/):

#### Format
```
<type>(<scope>): <subject>

<body>

<footer>
```

#### Types
- **feat**: New feature
- **fix**: Bug fix
- **docs**: Documentation changes
- **style**: Code style changes (formatting, etc.)
- **refactor**: Code refactoring
- **test**: Adding or updating tests
- **chore**: Maintenance tasks

#### Examples
```
feat(analysis): add risk score calculation

Implement risk score calculation algorithm based on 
historical claims data.

Closes #123
```

```
fix(data): resolve null value handling in loaders

Fixed issue where null values in CSV files caused 
data loading to fail.

Fixes #456
```

### 4. Pull Request Process

1. **Before Creating PR:**
   - Ensure all tests pass: `pytest`
   - Run code quality checks: `black .`, `flake8`, `mypy`
   - Update documentation if needed
   - Rebase on latest develop branch

2. **PR Title Format:**
   - Follow commit message format: `<type>(<scope>): <subject>`

3. **PR Description:**
   - Use the PR template
   - Describe changes clearly
   - Reference related issues
   - Include screenshots if applicable

4. **Review Process:**
   - All PRs require at least one approval
   - Address all review comments
   - Keep PRs focused and reasonably sized

### 5. Code Style

- Follow PEP 8 style guide
- Use `black` for automatic formatting
- Maximum line length: 88 characters (black default)
- Use type hints for all function signatures

### 6. Testing Requirements

- Write tests for all new features
- Maintain minimum 80% code coverage
- Include unit tests and integration tests as appropriate

### 7. Documentation

- Update README.md for user-facing changes
- Add docstrings to all functions and classes
- Update API documentation if applicable

## Code Review Checklist

- [ ] Code follows style guidelines
- [ ] Tests are included and passing
- [ ] Documentation is updated
- [ ] No console.log or debug statements
- [ ] Error handling is appropriate
- [ ] Performance considerations addressed

