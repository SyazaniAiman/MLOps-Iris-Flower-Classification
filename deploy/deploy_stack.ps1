# deploy/deploy_stack.ps1
param(
  [string]$ComposeFile = "docker-compose.yml"
)

$ErrorActionPreference = "Stop"

Write-Output "Bringing stack down..."
docker compose -f $ComposeFile down

Write-Output "Building images..."
docker compose -f $ComposeFile build

Write-Output "Bringing stack up..."
docker compose -f $ComposeFile up -d --force-recreate

Write-Output "Stack is up."
docker compose -f $ComposeFile ps
