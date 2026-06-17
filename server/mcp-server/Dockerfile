FROM python:3.11-slim

WORKDIR /app

COPY pyproject.toml .
RUN pip install --no-cache-dir -e .

COPY src/ src/

# Necesita acceso al socket de Docker del host
# Montar: -v /var/run/docker.sock:/var/run/docker.sock

CMD ["nortiqa-mcp"]
