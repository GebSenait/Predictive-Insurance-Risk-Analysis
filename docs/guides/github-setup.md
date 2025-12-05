# GitHub Repository Setup Guide

## Creating the Remote Repository

### Step 1: Create Repository on GitHub

1. **Go to GitHub**: Navigate to [https://github.com](https://github.com)
2. **Sign in** to your account
3. **Click the "+" icon** in the top right corner
4. **Select "New repository"**

### Step 2: Repository Settings

Fill in the repository details:

- **Repository name**: `Predictive Insurance Risk Analysis`
  - Or use: `predictive-insurance-risk-analysis` (lowercase with hyphens - recommended)
  
- **Description**: `Predictive Insurance Risk Analysis - Task 1 Implementation`

- **Visibility**: 
  - Choose **Public** (if you want it visible to others)
  - Or **Private** (if you want it private)

- **DO NOT** initialize with:
  - ❌ README
  - ❌ .gitignore
  - ❌ license
  
  (We already have these files locally)

5. **Click "Create repository"**

### Step 3: Connect Local Repository to Remote

After creating the repository, GitHub will show you commands. Use these:

```bash
# Add remote repository (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/Predictive-Insurance-Risk-Analysis.git

# Or if you used lowercase with hyphens:
git remote add origin https://github.com/YOUR_USERNAME/predictive-insurance-risk-analysis.git

# Verify remote was added
git remote -v
```

### Step 4: Push to Remote

```bash
# Push main branch first
git checkout main
git push -u origin main

# Push develop branch
git checkout develop
git push -u origin develop
```

## Alternative: Using GitHub CLI

If you have GitHub CLI installed:

```bash
# Create repository and connect in one step
gh repo create "Predictive-Insurance-Risk-Analysis" --public --source=. --remote=origin --push
```

## Repository Name Considerations

### Option 1: Exact Match (with spaces)
- Repository name: `Predictive Insurance Risk Analysis`
- URL: `https://github.com/YOUR_USERNAME/Predictive-Insurance-Risk-Analysis`
- Note: GitHub will convert spaces to hyphens in the URL

### Option 2: Lowercase with Hyphens (Recommended)
- Repository name: `predictive-insurance-risk-analysis`
- URL: `https://github.com/YOUR_USERNAME/predictive-insurance-risk-analysis`
- Better for URLs and command-line usage

## After Repository Creation

### Set Up Branch Protection (Optional but Recommended)

1. Go to repository Settings
2. Click "Branches" in left sidebar
3. Add rule for `main` branch:
   - ✅ Require pull request reviews
   - ✅ Require status checks to pass
   - ✅ Require branches to be up to date

### Verify Everything Works

```bash
# Check remote connection
git remote -v

# Fetch from remote
git fetch origin

# Check branches
git branch -a
```

## Troubleshooting

### If repository name has spaces

GitHub will automatically convert spaces to hyphens in the URL. Use the URL GitHub provides after creation.

### If you need to change remote URL

```bash
# Remove existing remote
git remote remove origin

# Add new remote
git remote add origin https://github.com/YOUR_USERNAME/repo-name.git
```

### If you get authentication errors

You may need to set up authentication:
- Use Personal Access Token (PAT)
- Or use SSH keys
- Or use GitHub CLI

## Next Steps

After setting up the remote repository:

1. ✅ Repository created on GitHub
2. ✅ Local repository connected to remote
3. ✅ Main branch pushed
4. ✅ Develop branch pushed
5. Ready to work on Task 1!

---

**Note**: If you need help with any step, let me know and I can provide more detailed instructions.

