param(
  [Parameter(Mandatory=$true)]
  [ValidateSet("blue","green")]
  [string]$Color
)

$repoRoot = Resolve-Path (Join-Path $PSScriptRoot "..")
$confDir  = Join-Path $repoRoot "nginx\conf.d"

$template = Join-Path $confDir "$Color.conf.template"
$default  = Join-Path $confDir "default.conf"

Copy-Item -Force $template $default

docker exec iris-nginx nginx -t
if ($LASTEXITCODE -ne 0) { throw "Nginx config test failed" }

docker exec iris-nginx nginx -s reload
Write-Output "Switched traffic to $Color"

