<#
.SYNOPSIS
    Starts all platform services using Docker Compose.
#>

Write-Host "=== Starting Deception & Threat Intelligence Platform ===" -ForegroundColor Cyan
docker compose up -d --build

if ($LASTEXITCODE -eq 0) {
    Write-Host "`n[SUCCESS] Platform services launched successfully!" -ForegroundColor Green
    Write-Host "  Honeypot Decoy (Public Facing):  http://localhost:80/wp-login.php" -ForegroundColor Yellow
    Write-Host "  SOC Visibility Dashboard:        http://localhost:3000" -ForegroundColor Yellow
    Write-Host "  Dashboard REST API:              http://localhost:8002/docs" -ForegroundColor Yellow
} else {
    Write-Error "Failed to launch platform services. Check docker compose logs."
}
