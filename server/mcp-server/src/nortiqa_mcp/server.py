"""
Nortiqa MCP Server — herramientas de control de infraestructura para Claude.
Expone operaciones Docker, métricas del servidor y estado de servicios.
"""
import asyncio
import os
from datetime import datetime

import docker
import psutil
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import TextContent, Tool

app = Server("nortiqa-mcp")

_docker_client: docker.DockerClient | None = None

ALLOWED_CONTAINERS = {
    "caddy", "nortiqa-api", "n8n", "ollama", "postgres", "redis", "nortiqa-mcp"
}


def _docker() -> docker.DockerClient:
    global _docker_client
    if _docker_client is None:
        _docker_client = docker.from_env()
    return _docker_client


def _assert_allowed(name: str) -> None:
    if name not in ALLOWED_CONTAINERS:
        raise ValueError(f"Contenedor '{name}' no está en la lista permitida: {ALLOWED_CONTAINERS}")


@app.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="docker_status",
            description="Estado de todos los contenedores del stack Nortiqa.",
            inputSchema={"type": "object", "properties": {}, "required": []},
        ),
        Tool(
            name="docker_logs",
            description="Últimas líneas del log de un contenedor.",
            inputSchema={
                "type": "object",
                "properties": {
                    "container": {"type": "string", "description": "Nombre del contenedor"},
                    "lines": {"type": "integer", "description": "Cantidad de líneas (default 50)", "default": 50},
                },
                "required": ["container"],
            },
        ),
        Tool(
            name="docker_restart",
            description="Reinicia un contenedor específico.",
            inputSchema={
                "type": "object",
                "properties": {
                    "container": {"type": "string", "description": "Nombre del contenedor"},
                },
                "required": ["container"],
            },
        ),
        Tool(
            name="docker_pull_and_recreate",
            description="Hace pull de la imagen más reciente y recrea el contenedor.",
            inputSchema={
                "type": "object",
                "properties": {
                    "container": {"type": "string", "description": "Nombre del contenedor"},
                },
                "required": ["container"],
            },
        ),
        Tool(
            name="server_metrics",
            description="Métricas actuales del servidor: CPU, RAM, disco, uptime.",
            inputSchema={"type": "object", "properties": {}, "required": []},
        ),
        Tool(
            name="service_health",
            description="Verifica conectividad de servicios internos (PostgreSQL, Redis, n8n, Ollama).",
            inputSchema={"type": "object", "properties": {}, "required": []},
        ),
    ]


@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    try:
        result = await _dispatch(name, arguments)
    except ValueError as e:
        result = f"ERROR: {e}"
    except Exception as e:
        result = f"ERROR inesperado: {type(e).__name__}: {e}"
    return [TextContent(type="text", text=result)]


async def _dispatch(name: str, args: dict) -> str:
    match name:
        case "docker_status":
            return await _docker_status()
        case "docker_logs":
            return await _docker_logs(args["container"], args.get("lines", 50))
        case "docker_restart":
            return await _docker_restart(args["container"])
        case "docker_pull_and_recreate":
            return await _docker_pull_and_recreate(args["container"])
        case "server_metrics":
            return await _server_metrics()
        case "service_health":
            return await _service_health()
        case _:
            raise ValueError(f"Herramienta desconocida: {name}")


async def _docker_status() -> str:
    client = _docker()
    containers = client.containers.list(all=True)
    lines = [f"{'NOMBRE':<25} {'ESTADO':<15} {'IMAGEN'}", "-" * 70]
    for c in sorted(containers, key=lambda x: x.name):
        image = c.image.tags[0] if c.image.tags else c.image.short_id
        lines.append(f"{c.name:<25} {c.status:<15} {image}")
    lines.append(f"\nTimestamp: {datetime.utcnow().isoformat()}Z")
    return "\n".join(lines)


async def _docker_logs(container: str, lines: int) -> str:
    _assert_allowed(container)
    client = _docker()
    c = client.containers.get(container)
    logs = c.logs(tail=lines, timestamps=True).decode("utf-8", errors="replace")
    return f"--- logs: {container} (últimas {lines} líneas) ---\n{logs}"


async def _docker_restart(container: str) -> str:
    _assert_allowed(container)
    client = _docker()
    c = client.containers.get(container)
    c.restart(timeout=30)
    return f"Contenedor '{container}' reiniciado. Estado: {c.reload() or c.status}"


async def _docker_pull_and_recreate(container: str) -> str:
    _assert_allowed(container)
    client = _docker()
    c = client.containers.get(container)
    image_name = c.image.tags[0] if c.image.tags else None
    if not image_name:
        return f"ERROR: no se puede determinar la imagen de '{container}'"

    loop = asyncio.get_event_loop()
    await loop.run_in_executor(None, client.images.pull, image_name)

    c.stop(timeout=30)
    c.remove()
    return f"Imagen '{image_name}' actualizada. Contenedor eliminado — usar 'docker compose up -d {container}' para recrearlo."


async def _server_metrics() -> str:
    cpu = psutil.cpu_percent(interval=1)
    mem = psutil.virtual_memory()
    disk = psutil.disk_usage("/")
    boot = datetime.fromtimestamp(psutil.boot_time())
    uptime = datetime.now() - boot

    return (
        f"=== Métricas del servidor ===\n"
        f"CPU:    {cpu:.1f}%\n"
        f"RAM:    {mem.used / 1024**3:.1f} GB / {mem.total / 1024**3:.1f} GB ({mem.percent:.1f}%)\n"
        f"Disco:  {disk.used / 1024**3:.1f} GB / {disk.total / 1024**3:.1f} GB ({disk.percent:.1f}%)\n"
        f"Uptime: {str(uptime).split('.')[0]}\n"
        f"Timestamp: {datetime.utcnow().isoformat()}Z"
    )


async def _service_health() -> str:
    import socket

    checks = {
        "PostgreSQL": ("postgres", 5432),
        "Redis":      ("redis", 6379),
        "n8n":        ("n8n", 5678),
        "Ollama":     ("ollama", 11434),
        "API":        ("nortiqa-api", 8000),
    }
    lines = [f"=== Health check — {datetime.utcnow().isoformat()}Z ==="]
    for service, (host, port) in checks.items():
        try:
            sock = socket.create_connection((host, port), timeout=2)
            sock.close()
            lines.append(f"  {service:<12} ✓ OK  ({host}:{port})")
        except Exception as e:
            lines.append(f"  {service:<12} ✗ FAIL ({e})")
    return "\n".join(lines)


def main() -> None:
    asyncio.run(stdio_server(app))


if __name__ == "__main__":
    main()
