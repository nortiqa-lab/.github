#!/usr/bin/env python3
"""Content contract for the NORTIQA home polish package (DEV)."""

from __future__ import annotations

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "index.html"


class HomeContentTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.html = INDEX.read_text(encoding="utf-8")
        cls.text = re.sub(r"<script[\s\S]*?</script>", " ", cls.html)
        cls.text = re.sub(r"<style[\s\S]*?</style>", " ", cls.text)
        cls.text = re.sub(r"<[^>]+>", " ", cls.text)
        cls.text = re.sub(r"\s+", " ", cls.text)

    def test_01_index_exists(self) -> None:
        self.assertTrue(INDEX.is_file(), "index.html must exist")

    def test_02_brand_signature_nortiqa(self) -> None:
        self.assertIn("NORTIQA", self.html)

    def test_03_contenido_demostrativo_contract(self) -> None:
        # Contract kept so validation does not break when demoting "demo" noise.
        self.assertIn("contenido demostrativo", self.text.lower())

    def test_04_en_preparacion_language(self) -> None:
        self.assertIn("en preparación", self.text.lower())

    def test_05_no_demo_status_badge(self) -> None:
        statuses = re.findall(r'class="status[^"]*"[^>]*>([^<]+)', self.html)
        joined = " | ".join(statuses).upper()
        self.assertNotIn("DEMO", joined)
        self.assertNotRegex(joined, r"\bMVP\b")
        self.assertNotIn("PROTOTIPO", joined)

    def test_06_public_internal_layer_separation(self) -> None:
        self.assertIn('data-layer="public"', self.html)
        self.assertIn('data-layer="internal"', self.html)
        lowered = self.html.lower()
        self.assertIn("capa interna", lowered)
        self.assertIn("capa pública", lowered)

    def test_07_required_sections(self) -> None:
        for section_id in (
            "inicio",
            "enfoque",
            "productos",
            "metodo",
            "arquitectura",
            "roadmap",
            "contacto",
        ):
            self.assertIn(f'id="{section_id}"', self.html)

    def test_08_no_secret_patterns(self) -> None:
        lowered = self.html.lower()
        for needle in ("api_key", "secret_key", "password=", "begin private key"):
            self.assertNotIn(needle, lowered)

    def test_09_institutional_not_prototype_shouting(self) -> None:
        self.assertIn("Sistemas de Inteligencia Organizacional", self.html)
        self.assertNotRegex(self.text, r"(?i)sitio\s+demo")
        self.assertNotRegex(self.text, r"(?i)esto\s+es\s+un\s+prototipo")


if __name__ == "__main__":
    unittest.main()
