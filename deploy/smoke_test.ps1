# deploy/smoke_test.ps1
param(
  [string]$BaseUrl = "http://127.0.0.1:8081"
)

$ErrorActionPreference = "Stop"

Write-Output "Smoke test: $BaseUrl/health"
curl.exe -s "$BaseUrl/health" | Out-String | Write-Output

Write-Output "Smoke test: $BaseUrl/predict"
curl.exe -s -X POST "$BaseUrl/predict" `
  -H "Content-Type: application/json" `
  -d '{\"features\":[5.1,3.5,1.4,0.2]}' | Out-String | Write-Output
