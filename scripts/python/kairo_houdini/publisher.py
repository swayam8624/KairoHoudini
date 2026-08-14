"""Immutable Houdini cache publication through KairoPipelineCore."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from kairo_pipeline.fingerprint import fingerprint_file
from kairo_pipeline.manifest import PublishFile, PublishKind, PublishManifest
from kairo_pipeline.paths import resolve_project_path
from kairo_pipeline.publish import plan_publish, publish_bundle

from .cacheguard import CacheProfile, CacheSnapshot, validate_cache


@dataclass(frozen=True, slots=True)
class CachePublishResult:
    target: Path
    frames: int
    bytes: int
    manifest_sha256: str
    dry_run: bool


def publish_cache(
    project_root: Path,
    snapshot: CacheSnapshot,
    *,
    project_name: str,
    cache_name: str,
    version: int,
    dry_run: bool = False,
    replace: bool = False,
    profile: CacheProfile = CacheProfile(),
) -> CachePublishResult:
    """Validate and publish a complete on-disk cache sequence."""

    diagnostics = validate_cache(snapshot, profile)
    if diagnostics.blocks_publish:
        codes = ", ".join(item.code for item in diagnostics if item.blocks_publish)
        raise ValueError(f"cache publish is blocked by: {codes}")
    root = Path(project_root).resolve(strict=True)
    source_scene = resolve_project_path(root, snapshot.source_scene)
    source_fingerprint = fingerprint_file(source_scene)
    pattern = snapshot.scan.pattern
    frames = tuple(
        PublishFile(
            path=pattern.path_for_frame(frame),
            role="cache-frame",
            fingerprint=fingerprint_file(
                resolve_project_path(root, pattern.path_for_frame(frame))
            ),
            media_type=_cache_media_type(pattern.path_for_frame(frame)),
        )
        for frame in snapshot.scan.existing
    )
    metadata = {
        "node": snapshot.node_path,
        "frame_first": str(snapshot.scan.first),
        "frame_last": str(snapshot.scan.last),
        "frame_pattern": pattern.canonical(),
    }
    if snapshot.current_upstream is not None:
        metadata["upstream_sha256"] = snapshot.current_upstream.sha256
    manifest = PublishManifest(
        kind=PublishKind.CACHE,
        project=project_name,
        name=cache_name,
        version=version,
        source_host="houdini",
        source_path=snapshot.source_scene,
        source_fingerprint=source_fingerprint,
        outputs=frames,
        metadata=metadata,
    )
    library = root / "Published"
    if dry_run:
        plan = plan_publish(root, library, manifest, replace=replace)
        return CachePublishResult(
            target=plan.target,
            frames=len(plan.files),
            bytes=sum(item.fingerprint.size for item in plan.files),
            manifest_sha256=plan.manifest_fingerprint.sha256,
            dry_run=True,
        )
    published = publish_bundle(root, library, manifest, replace=replace)
    return CachePublishResult(
        target=published.target,
        frames=published.copied_files,
        bytes=published.copied_bytes,
        manifest_sha256=published.manifest_fingerprint.sha256,
        dry_run=False,
    )


def _cache_media_type(path: str) -> str:
    lower = path.casefold()
    if lower.endswith(".vdb"):
        return "application/vnd.openvdb"
    if lower.endswith(".bgeo.sc") or lower.endswith(".bgeo"):
        return "application/vnd.houdini.bgeo"
    if lower.endswith(".abc"):
        return "application/vnd.alembic"
    return "application/octet-stream"

