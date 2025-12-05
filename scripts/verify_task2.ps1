# Task 2 Implementation Verification Script
# This script verifies all Task 2 deliverables are in place and working

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Task 2 Implementation Verification" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$errors = 0
$warnings = 0

# 1. Check Git Branch
Write-Host "1. Checking Git Branch..." -ForegroundColor Yellow
$currentBranch = git branch --show-current
if ($currentBranch -eq "Develop-2") {
    Write-Host "   ✅ On Develop-2 branch" -ForegroundColor Green
} else {
    Write-Host "   ⚠️  Current branch: $currentBranch (Expected: Develop-2)" -ForegroundColor Yellow
    $warnings++
}
Write-Host ""

# 2. Check DVC Installation
Write-Host "2. Checking DVC Installation..." -ForegroundColor Yellow
try {
    $dvcVersion = dvc --version
    Write-Host "   ✅ DVC installed: $dvcVersion" -ForegroundColor Green
} catch {
    Write-Host "   ❌ DVC not found" -ForegroundColor Red
    $errors++
}
Write-Host ""

# 3. Check DVC Initialization
Write-Host "3. Checking DVC Initialization..." -ForegroundColor Yellow
if (Test-Path ".dvc/config") {
    Write-Host "   ✅ DVC initialized (.dvc/config exists)" -ForegroundColor Green
} else {
    Write-Host "   ❌ DVC not initialized" -ForegroundColor Red
    $errors++
}
Write-Host ""

# 4. Check DVC Remote Configuration
Write-Host "4. Checking DVC Remote Configuration..." -ForegroundColor Yellow
try {
    $remoteList = dvc remote list
    if ($remoteList -match "local-storage") {
        Write-Host "   ✅ Remote 'local-storage' configured" -ForegroundColor Green
        Write-Host "   $remoteList" -ForegroundColor Gray
    } else {
        Write-Host "   ❌ Remote 'local-storage' not found" -ForegroundColor Red
        $errors++
    }
} catch {
    Write-Host "   ❌ Error checking remote configuration" -ForegroundColor Red
    $errors++
}
Write-Host ""

# 5. Check Remote Storage Directory
Write-Host "5. Checking Remote Storage Directory..." -ForegroundColor Yellow
if (Test-Path "dvc-storage") {
    Write-Host "   ✅ Remote storage directory exists" -ForegroundColor Green
} else {
    Write-Host "   ⚠️  Remote storage directory not found (will be created on first push)" -ForegroundColor Yellow
    $warnings++
}
Write-Host ""

# 6. Check DVC Ignore Files
Write-Host "6. Checking DVC Configuration Files..." -ForegroundColor Yellow
$filesToCheck = @(
    ".dvcignore",
    ".dvc/config",
    ".dvc/.gitignore"
)
foreach ($file in $filesToCheck) {
    if (Test-Path $file) {
        Write-Host "   ✅ $file exists" -ForegroundColor Green
    } else {
        Write-Host "   ❌ $file missing" -ForegroundColor Red
        $errors++
    }
}
Write-Host ""

# 7. Check Tracked Dataset
Write-Host "7. Checking Tracked Dataset..." -ForegroundColor Yellow
if (Test-Path "data/raw/MachineLearningRating_v3.txt.dvc") {
    Write-Host "   ✅ Dataset DVC file exists" -ForegroundColor Green
    $dvcContent = Get-Content "data/raw/MachineLearningRating_v3.txt.dvc" -Raw
    if ($dvcContent -match "md5:") {
        Write-Host "   ✅ Dataset has valid MD5 hash" -ForegroundColor Green
    }
} else {
    Write-Host "   ❌ Dataset DVC file missing" -ForegroundColor Red
    $errors++
}
Write-Host ""

# 8. Check DVC Status
Write-Host "8. Checking DVC Status..." -ForegroundColor Yellow
try {
    $dvcStatus = dvc status 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "   ✅ DVC status check passed" -ForegroundColor Green
        Write-Host "   $dvcStatus" -ForegroundColor Gray
    } else {
        Write-Host "   ⚠️  DVC status check returned warnings" -ForegroundColor Yellow
        Write-Host "   $dvcStatus" -ForegroundColor Gray
        $warnings++
    }
} catch {
    Write-Host "   ❌ Error checking DVC status" -ForegroundColor Red
    $errors++
}
Write-Host ""

# 9. Check Documentation
Write-Host "9. Checking Documentation..." -ForegroundColor Yellow
$docFiles = @(
    "docs/task2/README.md",
    "docs/task2/REPRODUCIBILITY_GUIDE.md",
    "TASK2_DELIVERABLES_SUMMARY.md"
)
foreach ($doc in $docFiles) {
    if (Test-Path $doc) {
        Write-Host "   ✅ $doc exists" -ForegroundColor Green
    } else {
        Write-Host "   ❌ $doc missing" -ForegroundColor Red
        $errors++
    }
}
Write-Host ""

# 10. Check Setup Scripts
Write-Host "10. Checking Setup Scripts..." -ForegroundColor Yellow
$scripts = @(
    "scripts/setup_dvc.ps1",
    "scripts/setup_dvc.sh"
)
foreach ($script in $scripts) {
    if (Test-Path $script) {
        Write-Host "   ✅ $script exists" -ForegroundColor Green
    } else {
        Write-Host "   ⚠️  $script missing (optional)" -ForegroundColor Yellow
        $warnings++
    }
}
Write-Host ""

# 11. Check Configuration Updates
Write-Host "11. Checking Configuration Updates..." -ForegroundColor Yellow
if (Test-Path "config/config.yaml") {
    $configContent = Get-Content "config/config.yaml" -Raw
    if ($configContent -match "dvc:") {
        Write-Host "   ✅ DVC configuration added to config.yaml" -ForegroundColor Green
    } else {
        Write-Host "   ⚠️  DVC configuration not found in config.yaml" -ForegroundColor Yellow
        $warnings++
    }
} else {
    Write-Host "   ⚠️  config.yaml not found" -ForegroundColor Yellow
    $warnings++
}
Write-Host ""

# 12. Check Requirements
Write-Host "12. Checking Requirements..." -ForegroundColor Yellow
if (Test-Path "requirements/base.txt") {
    $reqContent = Get-Content "requirements/base.txt" -Raw
    if ($reqContent -match "dvc>=") {
        Write-Host "   ✅ DVC added to requirements/base.txt" -ForegroundColor Green
    } else {
        Write-Host "   ⚠️  DVC not found in requirements" -ForegroundColor Yellow
        $warnings++
    }
} else {
    Write-Host "   ⚠️  requirements/base.txt not found" -ForegroundColor Yellow
    $warnings++
}
Write-Host ""

# 13. Check Git Commits
Write-Host "13. Checking Git Commits..." -ForegroundColor Yellow
$commits = git log --oneline -5
$dvcCommits = $commits | Select-String -Pattern "dvc|DVC|task2|Task2"
if ($dvcCommits) {
    Write-Host "   ✅ Task 2 commits found:" -ForegroundColor Green
    $dvcCommits | ForEach-Object { Write-Host "      $_" -ForegroundColor Gray }
} else {
    Write-Host "   ⚠️  No Task 2 commits found in recent history" -ForegroundColor Yellow
    $warnings++
}
Write-Host ""

# Summary
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Verification Summary" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

if ($errors -eq 0 -and $warnings -eq 0) {
    Write-Host "✅ All checks passed! Task 2 implementation is complete." -ForegroundColor Green
    exit 0
} elseif ($errors -eq 0) {
    Write-Host "✅ All critical checks passed!" -ForegroundColor Green
    Write-Host "⚠️  $warnings warning(s) found (non-critical)" -ForegroundColor Yellow
    exit 0
} else {
    Write-Host "❌ Verification failed!" -ForegroundColor Red
    Write-Host "   Errors: $errors" -ForegroundColor Red
    Write-Host "   Warnings: $warnings" -ForegroundColor Yellow
    exit 1
}

