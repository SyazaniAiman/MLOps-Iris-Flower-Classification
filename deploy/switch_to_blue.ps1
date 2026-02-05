# deploy/switch_to_blue.ps1
$ErrorActionPreference = "Stop"

Write-Output "Switching traffic to BLUE..."

Copy-Item -Force "nginx\conf.d\blue.conf.template" "nginx\conf.d\default.conf"
docker exec iris-nginx nginx -s reload

Write-Output "Switched traffic to BLUE."
