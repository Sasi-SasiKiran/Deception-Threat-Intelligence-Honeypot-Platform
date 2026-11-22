<#
.SYNOPSIS
    Prerequisite check and initial directory setup for Deception Honeypot Platform.
#>

Write-Host "=== Setting up Deception & Threat Intelligence Platform ===" -ForegroundColor Cyan

# 1. Check Docker
if (Get-Command docker -ErrorAction SilentlyContinue) {
    Write-Host "[OK] Docker is installed." -ForegroundColor Green
} else {
    Write-Warning "[!] Docker is not installed or not in PATH. Please install Docker Desktop."
}

# 2. Check Docker Compose
$composeCmd = docker compose version 2>$null
if ($composeCmd) {
    Write-Host "[OK] Docker Compose is available." -ForegroundColor Green
} else {
    Write-Warning "[!] Docker Compose v2 is required."
}

# 3. Create .env if missing
if (-not (Test-Path ".env")) {
    if (Test-Path ".env.example") {
        Copy-Item ".env.example" ".env"
        Write-Host "[OK] Created .env from .env.example." -ForegroundColor Green
    } else {
        Write-Warning "[!] .env.example not found."
    }
} else {
    Write-Host "[OK] .env exists." -ForegroundColor Green
}

# 4. Ensure data folder exists
if (-not (Test-Path "data")) {
    New-Item -ItemType Directory -Path "data" | Out-Null
}

Write-Host "`nSetup verification complete. Run .\scripts\start.ps1 to start the platform." -ForegroundColor Cyan
