# TEACHING MAP — tests/test_package.py
# Validates Python package import/installation boundaries for running the Houdini tool
# extension.
# Consult READING_ORDER.md for related host APIs, validation and tests.

from __future__ import annotations

import unittest

import kairo_houdini


class PackageTests(unittest.TestCase):
    def test_public_version(self) -> None:
        self.assertEqual(kairo_houdini.__version__, "0.1.0")


if __name__ == "__main__":
    unittest.main()
