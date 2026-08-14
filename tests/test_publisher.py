from __future__ import annotations

from pathlib import Path
import tempfile
import unittest

from kairo_houdini.cacheguard import inspect_cache
from kairo_houdini.publisher import publish_cache
from kairo_pipeline.manifest import load_manifest


class CachePublisherTests(unittest.TestCase):
    def test_complete_cache_dry_run_then_publish(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "shots").mkdir()
            (root / "shots/smoke.hipnc").write_bytes(b"houdini-scene")
            (root / "cache").mkdir()
            for frame in (1, 2):
                (root / f"cache/smoke.{frame:04d}.bgeo.sc").write_bytes(
                    f"frame-{frame}".encode()
                )
            snapshot = inspect_cache(
                root,
                node_path="/obj/smoke/filecache1",
                source_scene="shots/smoke.hipnc",
                output_pattern="cache/smoke.####.bgeo.sc",
                first=1,
                last=2,
            )

            planned = publish_cache(
                root,
                snapshot,
                project_name="Portfolio",
                cache_name="SmokeCache",
                version=1,
                dry_run=True,
            )
            self.assertTrue(planned.dry_run)
            self.assertFalse((root / "Published").exists())

            result = publish_cache(
                root,
                snapshot,
                project_name="Portfolio",
                cache_name="SmokeCache",
                version=1,
            )
            self.assertEqual(result.frames, 2)
            self.assertEqual(len(result.manifest_sha256), 64)
            manifest = load_manifest(result.target / "publish.kairo.json")
            self.assertEqual(manifest.kind.value, "cache")
            self.assertEqual(len(manifest.outputs), 2)

    def test_incomplete_cache_cannot_publish(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "shots").mkdir()
            (root / "shots/smoke.hipnc").write_bytes(b"scene")
            (root / "cache").mkdir()
            (root / "cache/smoke.0001.bgeo.sc").write_bytes(b"frame")
            snapshot = inspect_cache(
                root,
                node_path="/obj/smoke/filecache1",
                source_scene="shots/smoke.hipnc",
                output_pattern="cache/smoke.####.bgeo.sc",
                first=1,
                last=2,
            )
            with self.assertRaisesRegex(ValueError, "CACHE_FRAMES_MISSING"):
                publish_cache(
                    root,
                    snapshot,
                    project_name="Portfolio",
                    cache_name="SmokeCache",
                    version=1,
                )


if __name__ == "__main__":
    unittest.main()
