# Reproducibility Guide

## Overview

This guide provides step-by-step instructions for reproducing any analysis or model training at any point in the project's history. This is critical for regulatory compliance and audit requirements.

## Prerequisites

- Git installed and configured
- DVC installed (`pip install dvc`)
- Python 3.9+ with project dependencies installed
- Access to DVC remote storage

## Step-by-Step Reproduction Process

### 1. Identify the Target Version

First, identify the Git commit or tag you want to reproduce:

```bash
# List all commits
git log --oneline

# List tags
git tag -l

# View commit details
git show <commit-hash>
```

### 2. Checkout the Code Version

```bash
# Checkout specific commit
git checkout <commit-hash>

# Or checkout a tag
git checkout <tag-name>

# Create a new branch for reproduction (recommended)
git checkout -b reproduce-<commit-hash> <commit-hash>
```

### 3. Restore Data Version

After checking out the code, restore the corresponding data:

```bash
# Pull all data files for this version
dvc pull

# Verify data integrity
dvc status
```

### 4. Verify Environment

Ensure your Python environment matches the requirements:

```bash
# Install/update dependencies
pip install -r requirements/base.txt

# Verify Python version
python --version  # Should be 3.9+

# Check DVC version
dvc --version
```

### 5. Run the Analysis

```bash
# Run the main analysis script
python scripts/run_pipeline.py

# Or run specific analysis modules
python -m src.analysis.<module>
```

### 6. Verify Results

Compare results with expected outputs:

```bash
# Check output files
ls -la results/

# Compare checksums if available
md5sum results/reports/*.html
```

## Advanced Reproduction Scenarios

### Reproducing with Different Data Versions

To test how analysis changes with different data versions:

```bash
# Checkout specific data version
git checkout <commit-hash> data/raw/MachineLearningRating_v3.txt.dvc
dvc checkout data/raw/MachineLearningRating_v3.txt.dvc

# Run analysis
python scripts/run_pipeline.py

# Compare results
```

### Reproducing Pipeline Stages

If using DVC pipelines:

```bash
# Reproduce specific stage
dvc repro <stage-name>

# Reproduce entire pipeline
dvc repro

# Force reproduction
dvc repro --force
```

### Reproducing in Isolated Environment

For complete isolation:

```bash
# Create new virtual environment
python -m venv venv-reproduce
source venv-reproduce/bin/activate  # On Windows: venv-reproduce\Scripts\activate

# Install exact dependencies
pip install -r requirements/base.txt

# Checkout code and data
git checkout <commit-hash>
dvc pull

# Run analysis
python scripts/run_pipeline.py
```

## Troubleshooting Reproduction Issues

### Issue: Data file not found

**Symptoms:**
```
ERROR: failed to pull data from the cloud
```

**Solutions:**
1. Check remote storage access:
   ```bash
   dvc remote list
   ls dvc-storage/
   ```

2. Verify .dvc file exists:
   ```bash
   ls data/raw/*.dvc
   ```

3. Force pull:
   ```bash
   dvc pull --force
   ```

### Issue: Dependency version mismatch

**Symptoms:**
```
ImportError: cannot import name 'X'
```

**Solutions:**
1. Check requirements file for that commit:
   ```bash
   git show <commit-hash>:requirements/base.txt
   ```

2. Install exact versions:
   ```bash
   pip install -r requirements/base.txt --force-reinstall
   ```

### Issue: Configuration file differences

**Symptoms:**
```
KeyError: 'missing_config_key'
```

**Solutions:**
1. Check config file for that commit:
   ```bash
   git show <commit-hash>:config/config.yaml
   ```

2. Restore config file:
   ```bash
   git checkout <commit-hash> config/config.yaml
   ```

## Audit Trail Documentation

### Documenting Reproduction

When reproducing for audit purposes, document:

1. **Reproduction Date**: When the reproduction was performed
2. **Git Commit**: Exact commit hash used
3. **Data Versions**: DVC file hashes for all data files
4. **Environment**: Python version, OS, dependency versions
5. **Results**: Output files and checksums
6. **Differences**: Any differences from original results

### Example Audit Report Template

```markdown
# Reproduction Audit Report

**Date**: 2024-01-15
**Reproduced By**: [Name]
**Original Analysis Date**: [Date]
**Original Commit**: abc123def456

## Environment
- Python: 3.10.8
- OS: Windows 10
- DVC: 3.64.1

## Data Versions
- MachineLearningRating_v3.txt: md5:f6b7009b68ae21372b7deca9307fbb23

## Results
- Output files: [list]
- Checksums: [list]
- Status: ✅ Reproduced successfully / ❌ Differences found

## Notes
[Any observations or differences]
```

## Automation Scripts

### Automated Reproduction Script

Create `scripts/reproduce.sh`:

```bash
#!/bin/bash
set -e

COMMIT_HASH=$1
if [ -z "$COMMIT_HASH" ]; then
    echo "Usage: ./scripts/reproduce.sh <commit-hash>"
    exit 1
fi

echo "Reproducing analysis for commit: $COMMIT_HASH"

# Checkout code
git checkout $COMMIT_HASH

# Pull data
dvc pull

# Verify
dvc status

# Run analysis
python scripts/run_pipeline.py

echo "Reproduction complete!"
```

### Windows PowerShell Version

Create `scripts/reproduce.ps1`:

```powershell
param(
    [Parameter(Mandatory=$true)]
    [string]$CommitHash
)

Write-Host "Reproducing analysis for commit: $CommitHash"

# Checkout code
git checkout $CommitHash

# Pull data
dvc pull

# Verify
dvc status

# Run analysis
python scripts/run_pipeline.py

Write-Host "Reproduction complete!"
```

## Best Practices

1. **Always document**: Keep records of all reproductions
2. **Test regularly**: Periodically test reproduction of key analyses
3. **Version pinning**: Pin dependency versions for critical analyses
4. **Isolation**: Use isolated environments for reproduction
5. **Verification**: Always verify data integrity before analysis
6. **Comparison**: Compare results with original when possible

## Compliance Checklist

When reproducing for regulatory compliance:

- [ ] Exact Git commit identified and documented
- [ ] All data versions verified and documented
- [ ] Environment matches original (or differences documented)
- [ ] All dependencies installed at correct versions
- [ ] Analysis runs without errors
- [ ] Results match original (or differences explained)
- [ ] Complete audit trail maintained
- [ ] Reproduction report generated

---

**Last Updated**: Task 2 Implementation
**Status**: ✅ Production Ready

