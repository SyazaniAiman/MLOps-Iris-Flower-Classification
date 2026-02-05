Copy-Item -Force "nginx\conf.d\green.conf.template" "nginx\conf.d\default.conf"
docker exec iris-nginx nginx -s reload
Write-Output "Switched traffic to GREEN"
