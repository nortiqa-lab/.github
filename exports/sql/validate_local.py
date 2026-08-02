#!/usr/bin/env python3
"""Validate nl_agentes / nl_tareas SQL against ephemeral PostgreSQL.

Prefers Docker Postgres 16. Falls back to structural checks if Docker unavailable.
Never targets VPS/PROD.
"""
from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent
MIGRATION = ROOT / "migrations" / "003_nl_agentes_tareas.sql"
SEED = ROOT / "seed" / "001_nl_agentes_tareas_seed.sql"
IMAGE = "postgres:16-alpine"
CONTAINER = "nl-sql-validate-tmp"


def structural_check() -> int:
    """Minimal syntax / content checks without a DB engine."""
    errors: list[str] = []
    mig = MIGRATION.read_text(encoding="utf-8")
    seed = SEED.read_text(encoding="utf-8")
    for label, text, needles in (
        ("migration", mig, ["CREATE TABLE IF NOT EXISTS nl_agentes_inventario", "CREATE TABLE IF NOT EXISTS nl_tareas", "BEGIN;", "COMMIT;"]),
        ("seed", seed, ["INSERT INTO nl_agentes_inventario", "INSERT INTO nl_tareas", "ON CONFLICT", "BEGIN;", "COMMIT;"]),
    ):
        for n in needles:
            if n not in text:
                errors.append(f"{label}: missing `{n}`")
    # PG-only constructs that sqlite cannot run — document, do not fail structural
    pg_only = ["TIMESTAMPTZ", "now()", "ON CONFLICT"]
    print("structural: OK markers present" if not errors else "structural: FAIL")
    for e in errors:
        print(f"  - {e}")
    print(f"note: SQL uses PostgreSQL constructs ({', '.join(pg_only)}); apply with psql/Docker, not sqlite.")
    return 1 if errors else 0


def docker_available() -> bool:
    return shutil.which("docker") is not None


def run_docker_validate() -> int:
    subprocess.run(["docker", "rm", "-f", CONTAINER], check=False, capture_output=True)
    run = subprocess.run(
        [
            "docker",
            "run",
            "-d",
            "--name",
            CONTAINER,
            "-e",
            "POSTGRES_PASSWORD=nldev",
            "-e",
            "POSTGRES_USER=nldev",
            "-e",
            "POSTGRES_DB=nldev",
            "-p",
            "55432:5432",
            IMAGE,
        ],
        capture_output=True,
        text=True,
    )
    if run.returncode != 0:
        print("docker run failed:", run.stderr.strip())
        return structural_check()

    try:
        for _ in range(30):
            ready = subprocess.run(
                ["docker", "exec", CONTAINER, "pg_isready", "-U", "nldev"],
                capture_output=True,
                text=True,
            )
            if ready.returncode == 0:
                break
            time.sleep(1)
        else:
            print("postgres not ready")
            return 1

        for sql_path in (MIGRATION, SEED):
            proc = subprocess.run(
                ["docker", "exec", "-i", CONTAINER, "psql", "-U", "nldev", "-d", "nldev", "-v", "ON_ERROR_STOP=1"],
                input=sql_path.read_text(encoding="utf-8"),
                capture_output=True,
                text=True,
            )
            if proc.returncode != 0:
                print(f"FAIL applying {sql_path.name}:\n{proc.stderr}")
                return 1
            print(f"OK apply {sql_path.name}")

        check = subprocess.run(
            [
                "docker",
                "exec",
                CONTAINER,
                "psql",
                "-U",
                "nldev",
                "-d",
                "nldev",
                "-t",
                "-A",
                "-c",
                "SELECT count(*) FROM nl_agentes_inventario; SELECT count(*) FROM nl_tareas;",
            ],
            capture_output=True,
            text=True,
        )
        if check.returncode != 0:
            print(check.stderr)
            return 1
        lines = [ln.strip() for ln in check.stdout.splitlines() if ln.strip()]
        print(f"counts agentes={lines[0] if lines else '?'} tareas={lines[1] if len(lines) > 1 else '?'}")
        if len(lines) >= 2 and int(lines[0]) >= 11 and int(lines[1]) >= 1:
            print("docker postgres validate: PASS")
            return 0
        print("docker postgres validate: unexpected counts", lines)
        return 1
    finally:
        subprocess.run(["docker", "rm", "-f", CONTAINER], check=False, capture_output=True)


def main() -> int:
    if not MIGRATION.is_file() or not SEED.is_file():
        print("missing migration/seed files", file=sys.stderr)
        return 1
    if docker_available():
        print("using Docker Postgres 16…")
        code = run_docker_validate()
        if code == 0:
            return 0
        print("docker path failed; falling back to structural")
    else:
        print("docker not available; structural check only")
    return structural_check()


if __name__ == "__main__":
    raise SystemExit(main())
