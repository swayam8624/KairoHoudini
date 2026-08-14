from __future__ import annotations

import unittest

import kairo_houdini


class PackageTests(unittest.TestCase):
    def test_public_version(self) -> None:
        self.assertEqual(kairo_houdini.__version__, "0.1.0")


if __name__ == "__main__":
    unittest.main()
