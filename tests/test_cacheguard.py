from __future__ import annotations

from pathlib import Path
import tempfile
import unittest

from kairo_houdini.cacheguard import (
    CacheProfile,
    inspect_cache,
    missing_frames,
    validate_cache,
)
from kairo_pipeline.fingerprint import fingerprint_bytes


class CacheGuardTests(unittest.TestCase):
    def test_incomplete_cache_reports_resume_frames(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            cache = root / "cache"
            cache.mkdir()
            for frame in (1, 3):
                (cache / f"smoke.{frame:04d}.bgeo.sc").write_bytes(b"x" * frame)

            snapshot = inspect_cache(
                root,
                node_path="/obj/smoke/filecache1",
                source_scene="shots/smoke.hipnc",
                output_pattern="cache/smoke.####.bgeo.sc",
                first=1,
                last=3,
            )
            diagnostics = validate_cache(snapshot)

            self.assertEqual(missing_frames(snapshot), (2,))
            self.assertIn(
                "CACHE_FRAMES_MISSING",
                {item.code for item in diagnostics},
            )
            self.assertTrue(diagnostics.blocks_publish)

    def test_complete_current_cache_passes(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            cache = root / "cache"
            cache.mkdir()
            for frame in range(1, 4):
                (cache / f"smoke.{frame:04d}.bgeo.sc").write_bytes(b"frame")
            upstream = fingerprint_bytes(b"upstream")
            snapshot = inspect_cache(
                root,
                node_path="/obj/smoke/filecache1",
                source_scene="shots/smoke.hipnc",
                output_pattern="cache/smoke.####.bgeo.sc",
                first=1,
                last=3,
                current_upstream=upstream,
                published_upstream=upstream,
            )
            self.assertEqual(tuple(validate_cache(snapshot)), ())

    def test_stale_upstream_and_budget_are_reported(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            cache = root / "cache"
            cache.mkdir()
            (cache / "smoke.0001.bgeo.sc").write_bytes(b"12345678")
            snapshot = inspect_cache(
                root,
                node_path="/obj/smoke/filecache1",
                source_scene="shots/smoke.hipnc",
                output_pattern="cache/smoke.####.bgeo.sc",
                first=1,
                last=1,
                current_upstream=fingerprint_bytes(b"new"),
                published_upstream=fingerprint_bytes(b"old"),
            )
            codes = {
                item.code
                for item in validate_cache(
                    snapshot,
                    CacheProfile(storage_budget_bytes=4),
                )
            }
            self.assertIn("CACHE_UPSTREAM_STALE", codes)
            self.assertIn("CACHE_STORAGE_BUDGET", codes)

    def test_relative_node_path_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaisesRegex(ValueError, "absolute"):
                inspect_cache(
                    Path(directory),
                    node_path="obj/cache1",
                    source_scene="shot.hip",
                    output_pattern="cache/sim.####.bgeo.sc",
                    first=1,
                    last=2,
                )


if __name__ == "__main__":
    unittest.main()
