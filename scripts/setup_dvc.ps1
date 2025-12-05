# PowerShell script to set up DVC for the project
# This script initializes DVC and configures local remote storage

Write-Host "Setting up DVC for Predictive Insurance Risk Analysis..." -ForegroundColor Green

# Check if DVC is installed
Write-Host "`nChecking DVC installation..." -ForegroundColor Yellow
try {
    $dvcVersion = dvc --version
    Write-Host "DVC is installed: $dvcVersion" -ForegroundColor Green
} catch {
    Write-Host "DVC is not installed. Installing..." -ForegroundColor Yellow
    pip install dvc
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Failed to install DVC. Please install manually: pip install dvc" -ForegroundColor Red
        exit 1
    }
}

# Initialize DVC if not already initialized
if (-not (Test-Path ".dvc")) {
    Write-Host "`nInitializing DVC..." -ForegroundColor Yellow
    dvc init
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Failed to initialize DVC" -ForegroundColor Red
        exit 1
    }
    Write-Host "DVC initialized successfully" -ForegroundColor Green
} else {
    Write-Host "DVC is already initialized" -ForegroundColor Green
}

# Create local remote storage directory
$storagePath = "dvc-storage"
if (-not (Test-Path $storagePath)) {
    Write-Host "`nCreating local DVC remote storage directory..." -ForegroundColor Yellow
    New-Item -ItemType Directory -Path $storagePath -Force | Out-Null
    Write-Host "Created directory: $storagePath" -ForegroundColor Green
} else {
    Write-Host "Storage directory already exists: $storagePath" -ForegroundColor Green
}

# Configure local remote
Write-Host "`nConfiguring DVC remote storage..." -ForegroundColor Yellow
$absolutePath = (Resolve-Path $storagePath).Path
dvc remote add -d local-storage $absolutePath
if ($LASTEXITCODE -ne 0) {
    # Try to modify if it already exists
    dvc remote modify local-storage url $absolutePath
    dvc remote default local-storage
    Write-Host "Updated existing remote configuration" -ForegroundColor Yellow
} else {
    Write-Host "Remote 'local-storage' configured successfully" -ForegroundColor Green
}

# Display configuration
Write-Host "`nDVC Configuration:" -ForegroundColor Cyan
dvc remote list

Write-Host "`nSetup complete! Next steps:" -ForegroundColor Green
Write-Host "1. Add data files: dvc add data/raw/MachineLearningRating_v3.txt" -ForegroundColor White
Write-Host "2. Commit .dvc files: git add *.dvc .dvcignore" -ForegroundColor White
Write-Host "3. Push data to remote: dvc push" -ForegroundColor White

