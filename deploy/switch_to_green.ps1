# deploy/switch_to_green.ps1
$ErrorActionPreference = "Stop"

Write-Output "Switching traffic to GREEN..."

Copy-Item -Force "nginx\conf.d\green.conf.template" "nginx\conf.d\default.conf"

# Reload nginx inside the running nginx container
docker exec iris-nginx nginx -s reload

Write-Output "Switched traffic to GREEN."
