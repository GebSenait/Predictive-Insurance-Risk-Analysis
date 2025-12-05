# PowerShell script to connect local repository to GitHub remote
# Usage: .\scripts\setup_remote.ps1 -GitHubUsername "YOUR_GITHUB_USERNAME"

param(
    [Parameter(Mandatory=$true)]
    [string]$GitHubUsername,
    
    [Parameter(Mandatory=$false)]
    [string]$RepoName = "Predictive-Insurance-Risk-Analysis"
)

Write-Host "Setting up remote repository connection..." -ForegroundColor Green
Write-Host "GitHub Username: $GitHubUsername"
Write-Host "Repository Name: $RepoName"
Write-Host ""

# Check if remote already exists
$remoteExists = git remote get-url origin 2>$null
if ($remoteExists) {
    Write-Host "Remote 'origin' already exists:" -ForegroundColor Yellow
    git remote -v
    $response = Read-Host "Do you want to update it? (y/n)"
    if ($response -eq "y" -or $response -eq "Y") {
        git remote remove origin
    } else {
        Write-Host "Aborted." -ForegroundColor Red
        exit 1
    }
}

# Add remote
Write-Host "Adding remote repository..." -ForegroundColor Green
$remoteUrl = "https://github.com/$GitHubUsername/$RepoName.git"
git remote add origin $remoteUrl

# Verify
Write-Host ""
Write-Host "Remote added successfully!" -ForegroundColor Green
Write-Host "Verifying connection..." -ForegroundColor Green
git remote -v

Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "1. Push main branch: git push -u origin main"
Write-Host "2. Push develop branch: git checkout develop; git push -u origin develop"

