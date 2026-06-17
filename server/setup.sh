#!/bin/bash
# Setup inicial del servidor Hetzner — ejecutar como root una sola vez
set -euo pipefail

DEPLOY_USER="nortiqa"
DEPLOY_DIR="/opt/nortiqa"

echo "=== Nortiqa Lab — Setup de servidor ==="

# Actualizar sistema
apt-get update && apt-get upgrade -y

# Instalar dependencias
apt-get install -y \
    ca-certificates \
    curl \
    gnupg \
    ufw \
    fail2ban \
    git \
    htop \
    unzip

# Instalar Docker
install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg
chmod a+r /etc/apt/keyrings/docker.gpg

echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  tee /etc/apt/sources.list.d/docker.list > /dev/null

apt-get update
apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# Usuario de deploy
if ! id "$DEPLOY_USER" &>/dev/null; then
    useradd -m -s /bin/bash "$DEPLOY_USER"
    usermod -aG docker "$DEPLOY_USER"
    echo "Usuario $DEPLOY_USER creado"
fi

# Directorio de trabajo
mkdir -p "$DEPLOY_DIR"
chown "$DEPLOY_USER:$DEPLOY_USER" "$DEPLOY_DIR"

# Firewall
ufw default deny incoming
ufw default allow outgoing
ufw allow ssh
ufw allow 80/tcp
ufw allow 443/tcp
ufw --force enable
echo "Firewall configurado"

# fail2ban
systemctl enable fail2ban
systemctl start fail2ban
echo "fail2ban activo"

# Crear directorio de logs para Caddy
mkdir -p /var/log/caddy
chown "$DEPLOY_USER:$DEPLOY_USER" /var/log/caddy

echo ""
echo "=== Setup completo ==="
echo "Próximo paso: copiar archivos a $DEPLOY_DIR y ejecutar 'docker compose up -d'"
