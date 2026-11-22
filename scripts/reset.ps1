<#
.SYNOPSIS
    Resets platform data, dropping database volumes and restarting clean state.
#>

$confirm = Read-Host "Are you sure you want to completely reset and wipe all collected honeypot data? (y/N)"
if ($confirm -eq 'y' -or $confirm -eq 'Y') {
    Write-Host "Resetting platform..." -ForegroundColor Yellow
    docker compose down -v --remove-orphans
    Write-Host "[OK] Cleaned all containers and storage volumes." -ForegroundColor Green
} else {
    Write-Host "Reset operation canceled." -ForegroundColor Cyan
}
