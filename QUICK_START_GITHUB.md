# Quick Start: GitHub Repository Setup

## 🚀 Quick Setup Guide

### Step 1: Create Repository on GitHub

**Option A: Via Web Browser (Easiest)**
1. Go to: https://github.com/new
2. Repository name: `Predictive-Insurance-Risk-Analysis`
3. Description: `Predictive Insurance Risk Analysis - Task 1 Implementation`
4. Choose Public or Private
5. **DO NOT** check any boxes (README, .gitignore, license)
6. Click **"Create repository"**

**Option B: Via GitHub CLI** (if installed)
```bash
gh repo create "Predictive-Insurance-Risk-Analysis" --public --description "Predictive Insurance Risk Analysis - Task 1 Implementation"
```

### Step 2: Connect Local Repository

After creating the repository, run one of these:

**For Windows (PowerShell):**
```powershell
# Replace YOUR_USERNAME with your GitHub username
.\scripts\setup_remote.ps1 -GitHubUsername "YOUR_USERNAME"
```

**For Linux/Mac (Bash):**
```bash
# Replace YOUR_USERNAME with your GitHub username
chmod +x scripts/setup_remote.sh
./scripts/setup_remote.sh YOUR_USERNAME
```

**Or manually:**
```bash
# Replace YOUR_USERNAME with your GitHub username
git remote add origin https://github.com/YOUR_USERNAME/Predictive-Insurance-Risk-Analysis.git

# Verify
git remote -v
```

### Step 3: Push Your Branches

```bash
# Push main branch
git checkout main
git push -u origin main

# Push develop branch
git checkout develop
git push -u origin develop
```

## ✅ Verification

After setup, verify everything works:

```bash
# Check remote connection
git remote -v

# Check branches
git branch -a

# Test push (from develop branch)
git push origin develop
```

## 📝 Important Notes

1. **Repository Name**: GitHub will convert spaces to hyphens in URLs
   - You can use: `Predictive-Insurance-Risk-Analysis` or `predictive-insurance-risk-analysis`
   - Both work, but lowercase with hyphens is more URL-friendly

2. **Authentication**: You may need to authenticate:
   - Use Personal Access Token (PAT)
   - Or set up SSH keys
   - Or use GitHub CLI

3. **First Push**: The `-u` flag sets up tracking so future pushes are simpler

## 🆘 Troubleshooting

### Authentication Error?
```bash
# Use Personal Access Token when prompted for password
# Or set up SSH keys
ssh-keygen -t ed25519 -C "your_email@example.com"
```

### Wrong Remote URL?
```bash
# Remove and re-add
git remote remove origin
git remote add origin https://github.com/YOUR_USERNAME/Predictive-Insurance-Risk-Analysis.git
```

### Repository Already Exists?
The script will ask if you want to update it. Say "y" to proceed.

## 🎯 Next Steps

After successful setup:
1. ✅ Repository created on GitHub
2. ✅ Local repo connected to remote
3. ✅ Branches pushed
4. ✅ Ready to develop Task 1!

You can now:
- Make changes locally
- Commit your work
- Push to develop branch
- Create pull requests

---

**Need Help?** See detailed guide: `docs/guides/github-setup.md`

