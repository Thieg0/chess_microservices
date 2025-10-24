#!/bin/bash

echo "=== Teste 1: Health Check ==="
curl http://localhost:8000/health
echo -e "\n"

echo "=== Teste 2: Registrar usuário ==="
REGISTER_RESPONSE=$(curl -s -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"name":"TestUser","email":"test@example.com","password":"123456"}')
echo $REGISTER_RESPONSE
TOKEN=$(echo $REGISTER_RESPONSE | grep -o '"token":"[^"]*' | cut -d'"' -f4)
echo "Token: $TOKEN"
echo -e "\n"

echo "=== Teste 3: Criar jogo ==="
GAME_RESPONSE=$(curl -s -X POST http://localhost:8000/games \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"mode":"local","white_player_id":1,"black_player_id":2}')
echo $GAME_RESPONSE
GAME_ID=$(echo $GAME_RESPONSE | grep -o '"game_id":"[^"]*' | cut -d'"' -f4)
echo "Game ID: $GAME_ID"
echo -e "\n"

echo "=== Teste 4: Fazer movimento ==="
curl -X POST http://localhost:8000/games/$GAME_ID/move \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"from":"e2","to":"e4"}'
echo -e "\n"
