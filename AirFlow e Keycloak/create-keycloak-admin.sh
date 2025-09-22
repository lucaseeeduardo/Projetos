#!/bin/bash
echo "Parando Keycloak..."
docker-compose stop keycloak

echo "Removendo dados antigos..."
docker volume ls | grep keycloak | awk '{print $2}' | xargs -r docker volume rm

echo "Iniciando Keycloak com admin..."
docker-compose up -d keycloak

echo "Aguardando Keycloak inicializar..."
for i in {1..60}; do
  if curl -s http://localhost:9090/health/ready > /dev/null; then
    echo "Keycloak pronto!"
    break
  fi
  echo "Tentativa $i/60..."
  sleep 5
done

echo "Testando login admin..."
curl -X POST http://localhost:9090/realms/master/protocol/openid-connect/token \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin&password=admin&grant_type=password&client_id=admin-cli"
