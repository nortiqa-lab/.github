#!/bin/bash
# Nortiqa MCP Server — instalación en servidor Hetzner
# Uso: curl -fsSL https://raw.githubusercontent.com/nortiqa-lab/.github/main/server/mcp-server/install.sh | bash
set -euo pipefail

REPO="https://github.com/nortiqa-lab/.github.git"
INSTALL_DIR="/opt/nortiqa-mcp"
BRANCH="main"

echo "=== Nortiqa MCP Server — instalación ==="

# Verificar Docker
if ! command -v docker &>/dev/null; then
    echo "Instalando Docker..."
    curl -fsSL https://get.docker.com | sh
    usermod -aG docker "$USER" || true
fi

# Clonar o actualizar repo
if [ -d "$INSTALL_DIR/.git" ]; then
    echo "Actualizando repositorio..."
    git -C "$INSTALL_DIR" pull origin "$BRANCH"
else
    echo "Clonando repositorio..."
    git clone --depth 1 --branch "$BRANCH" "$REPO" "$INSTALL_DIR"
fi

cd "$INSTALL_DIR/server/mcp-server"

# Build y levantar
echo "Construyendo imagen MCP server..."
docker compose build --no-cache

echo "Levantando contenedor..."
docker compose up -d

echo ""
echo "=== MCP server instalado ==="
docker compose ps

echo ""
echo "Para verificar: docker exec nortiqa-mcp nortiqa-mcp --help"
echo "Para conectar Claude: ver claude-mcp-config.json"
