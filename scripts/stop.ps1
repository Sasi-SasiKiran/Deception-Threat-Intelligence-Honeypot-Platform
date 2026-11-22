<#
.SYNOPSIS
    Stops running platform containers.
#>

Write-Host "=== Stopping Platform Services ===" -ForegroundColor Cyan
docker compose down

Write-Host "[OK] All honeypot platform services stopped." -ForegroundColor Green
