from __future__ import annotations

import unittest

from kairo_houdini.hom import houdini_pattern_to_core, inspect_selected_cache


class HomAdapterTests(unittest.TestCase):
    def test_frame_tokens_convert_to_shared_patterns(self) -> None:
        self.assertEqual(
            houdini_pattern_to_core("$JOB/cache/smoke.$F4.bgeo.sc"),
            "$JOB/cache/smoke.####.bgeo.sc",
        )
        self.assertEqual(
            houdini_pattern_to_core("cache/smoke.${F}.vdb"),
            "cache/smoke.#.vdb",
        )

    def test_missing_or_multiple_tokens_are_rejected(self) -> None:
        for value in ("cache/smoke.bgeo.sc", "cache/$F4/smoke.$F4.bgeo.sc"):
            with self.subTest(value=value), self.assertRaises(ValueError):
                houdini_pattern_to_core(value)

    def test_host_operation_fails_explicitly_without_houdini(self) -> None:
        with self.assertRaisesRegex(RuntimeError, "hou module"):
            inspect_selected_cache()


if __name__ == "__main__":
    unittest.main()
