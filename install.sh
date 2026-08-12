#!/bin/bash

GREEN='\033[0;32m'
NC='\033[0m'

echo -e "${GREEN}=== Instalando o shifTool ===${NC}"

URL="https://github.com/igmunizw/ShiftTool-v1.0/releases/latest/download/shiftool"

echo "Baixando a ferramenta..."
sudo curl -L -o /usr/local/bin/shiftool "$URL"
sudo chmod +x /usr/local/bin/shiftool

echo -e "${GREEN}✓ Instalação concluída com sucesso!${NC}"
echo "Agora basta abrir qualquer terminal e digitar: shiftool"