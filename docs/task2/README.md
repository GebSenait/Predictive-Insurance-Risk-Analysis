# Task 2: Reproducible & Auditable Data Pipeline with DVC

## Overview

This document describes the implementation of Task 2: Reproducible & Auditable Data Pipeline using Data Version Control (DVC). This implementation ensures full reproducibility and auditability for financial/insurance regulatory compliance.

## Objectives

- ✅ Implement DVC for data versioning
- ✅ Create reproducible data pipelines
- ✅ Establish audit trail for all data versions
- ✅ Enable historical data retrieval
- ✅ Meet regulatory compliance requirements

## DVC Setup

### Initialization

DVC has been initialized in this project with the following configuration:

- **DVC Version**: 3.64.1+
- **Remote Storage**: Local directory (`dvc-storage/`)
- **Remote Name**: `local-storage`
- **Configuration File**: `.dvc/config`

### Remote Storage Structure

```
dvc-storage/
├── [hashed data files]
└── [versioned data artifacts]
```

The remote storage uses content-addressable storage, where files are stored by their hash. This ensures:
- **Deduplication**: Same file content stored only once
- **Integrity**: File integrity verification via checksums
- **Efficiency**: Minimal storage overhead

## Tracked Datasets

### Current Datasets

1. **MachineLearningRating_v3.txt**
   - **Location**: `data/raw/MachineLearningRating_v3.txt`
   - **DVC File**: `data/raw/MachineLearningRating_v3.txt.dvc`
   - **Size**: ~529 MB
   - **Hash**: MD5 (f6b7009b68ae21372b7deca9307fbb23)

## Usage Guide

### Pulling Data

When cloning the repository or switching branches, pull the tracked data:

```bash
# Pull all tracked data files
dvc pull

# Pull specific file
dvc pull data/raw/MachineLearningRating_v3.txt.dvc
```

### Checking Data Status

```bash
# Check if data files are up to date
dvc status

# List all tracked files
dvc list data/raw
```

### Adding New Data Files

To add a new dataset to DVC tracking:

```bash
# Add file to DVC
dvc add data/raw/new_dataset.csv

# Stage the .dvc file for Git
git add data/raw/new_dataset.csv.dvc .gitignore

# Commit to Git
git commit -m "feat(data): add new dataset to DVC tracking"

# Push data to remote
dvc push
```

### Updating Existing Data

When updating a tracked file:

```bash
# Modify the data file
# ... make changes to data/raw/MachineLearningRating_v3.txt ...

# Update DVC tracking
dvc add data/raw/MachineLearningRating_v3.txt

# Commit changes
git add data/raw/MachineLearningRating_v3.txt.dvc
git commit -m "feat(data): update dataset version"

# Push to remote
dvc push
```

## Reproducibility

### Reproducing Analysis at a Specific Point

To reproduce an analysis from a specific Git commit:

1. **Checkout the commit:**
   ```bash
   git checkout <commit-hash>
   ```

2. **Pull the corresponding data version:**
   ```bash
   dvc pull
   ```

3. **Verify data integrity:**
   ```bash
   dvc status
   ```

4. **Run the analysis:**
   ```bash
   python scripts/run_pipeline.py
   ```

### Viewing Data History

```bash
# View commit history for a data file
git log --oneline data/raw/MachineLearningRating_v3.txt.dvc

# View detailed history
git log -p data/raw/MachineLearningRating_v3.txt.dvc

# View all data versions
dvc list --rev <commit-hash> data/raw
```

### Data Version Comparison

```bash
# Compare data versions between commits
git diff <commit1> <commit2> data/raw/MachineLearningRating_v3.txt.dvc

# Check what changed in data
dvc diff <commit1> <commit2>
```

## Remote Storage Management

### Remote Configuration

The DVC remote is configured in `.dvc/config`:

```ini
[core]
    remote = local-storage
['remote "local-storage"']
    url = dvc-storage
```

### Changing Remote Storage

To change the remote storage location:

```bash
# Modify remote URL
dvc remote modify local-storage url /path/to/new/storage

# Or use absolute path
dvc remote modify local-storage url "D:\Path\To\Storage"
```

### Remote Storage Best Practices

1. **Backup**: Regularly backup the `dvc-storage/` directory
2. **Location**: Use a shared network drive for team collaboration
3. **Permissions**: Ensure proper read/write permissions
4. **Monitoring**: Monitor storage usage and clean up old versions if needed

## Audit Trail & Compliance

### Regulatory Compliance Features

DVC provides the following compliance features:

1. **Immutable History**: All data versions are permanently tracked
2. **Checksum Verification**: Data integrity verified via MD5 hashes
3. **Reproducibility**: Any analysis can be reproduced exactly
4. **Traceability**: Full audit trail via Git commits and DVC metadata

### Audit Log

To generate an audit log:

```bash
# Export commit history with data versions
git log --oneline --all --graph > audit_log.txt

# Include DVC file changes
git log --oneline --all -- data/raw/*.dvc >> audit_log.txt
```

### Data Lineage

Track data lineage through the pipeline:

```bash
# View data dependencies
dvc dag

# Export pipeline graph
dvc dag --dot > pipeline.dot
```

## Troubleshooting

### Common Issues

#### Issue: `dvc pull` fails

**Solution:**
```bash
# Check remote configuration
dvc remote list

# Verify remote storage exists
ls dvc-storage/

# Re-pull with verbose output
dvc pull -v
```

#### Issue: Data file not found after `dvc pull`

**Solution:**
```bash
# Check DVC status
dvc status

# Force checkout
dvc checkout --force

# Verify .dvc file exists
ls data/raw/*.dvc
```

#### Issue: Remote storage path issues

**Solution:**
```bash
# Use absolute path in config
dvc remote modify local-storage url "$(pwd)/dvc-storage"

# Or on Windows
dvc remote modify local-storage url "D:\Full\Path\To\dvc-storage"
```

## Best Practices

### For Data Engineers

1. **Always commit .dvc files**: Never commit actual data files to Git
2. **Use descriptive commit messages**: Include data version info
3. **Push data after commits**: `dvc push` after `git commit`
4. **Verify before pushing**: Use `dvc status` to check state
5. **Document data changes**: Update data documentation with changes

### For Analysts

1. **Pull before analysis**: Always run `dvc pull` after `git pull`
2. **Check data status**: Verify data is up to date with `dvc status`
3. **Report data version**: Include data version in analysis reports
4. **Don't modify tracked files directly**: Use DVC commands to update

### For Auditors

1. **Review Git history**: Check `.dvc` file commits for data changes
2. **Verify checksums**: DVC automatically verifies data integrity
3. **Check reproducibility**: Test reproducing analyses from history
4. **Review remote storage**: Ensure proper backup and access controls

## Configuration Files

### Key Files

- **`.dvc/config`**: DVC configuration and remote settings
- **`.dvcignore`**: Files to ignore in DVC operations
- **`data/raw/*.dvc`**: Metadata files for tracked data
- **`.gitignore`**: Git ignore rules (includes DVC cache)

### Configuration Management

DVC configuration is version-controlled in Git. Changes to `.dvc/config` should be:
1. Reviewed by the team
2. Documented in commit messages
3. Tested before merging to main

## Integration with CI/CD

### Automated Data Validation

Add to CI/CD pipeline:

```yaml
# Example GitHub Actions step
- name: Verify DVC data
  run: |
    dvc pull
    dvc status
    # Add data validation checks
```

### Data Version Checks

```yaml
- name: Check data versions
  run: |
    dvc list data/raw
    # Verify expected files exist
```

## Additional Resources

- [DVC Documentation](https://dvc.org/doc)
- [DVC Best Practices](https://dvc.org/doc/user-guide/best-practices)
- [Data Versioning Guide](https://dvc.org/doc/use-cases/versioning-data-and-model-files)
- [Reproducibility Guide](https://dvc.org/doc/use-cases/reproducible-pipeline)

## Support

For issues or questions:
1. Check this documentation
2. Review DVC official documentation
3. Check project issues on GitHub
4. Contact the data engineering team

---

**Last Updated**: Task 2 Implementation
**DVC Version**: 3.64.1+
**Status**: ✅ Production Ready

