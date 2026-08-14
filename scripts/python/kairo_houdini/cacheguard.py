"""Host-neutral simulation cache inspection and validation rules."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import statistics

from kairo_pipeline.diagnostics import (
    Diagnostic,
    DiagnosticBag,
    DiagnosticLocation,
    Severity,
)
from kairo_pipeline.fingerprint import Fingerprint
from kairo_pipeline.paths import resolve_project_path
from kairo_pipeline.sequences import FramePattern, SequenceScan, scan_sequence


@dataclass(frozen=True, slots=True)
class CacheSnapshot:
    node_path: str
    source_scene: str
    scan: SequenceScan
    estimated_total_bytes: int
    free_bytes: int
    current_upstream: Fingerprint | None = None
    published_upstream: Fingerprint | None = None


@dataclass(frozen=True, slots=True)
class CacheProfile:
    storage_budget_bytes: int = 100 * 1024 * 1024 * 1024
    require_complete: bool = True

    def __post_init__(self) -> None:
        if self.storage_budget_bytes < 1:
            raise ValueError("cache storage budget must be positive")


def inspect_cache(
    project_root: Path,
    *,
    node_path: str,
    source_scene: str,
    output_pattern: str,
    first: int,
    last: int,
    current_upstream: Fingerprint | None = None,
    published_upstream: Fingerprint | None = None,
) -> CacheSnapshot:
    """Inspect one on-disk sequence and estimate its complete range size."""

    if not node_path or not node_path.startswith("/"):
        raise ValueError("Houdini node path must be absolute")
    pattern = FramePattern.parse(output_pattern)
    scan = scan_sequence(project_root, pattern, first, last)
    sizes = [
        resolve_project_path(project_root, pattern.path_for_frame(frame)).stat().st_size
        for frame in scan.existing
    ]
    typical_size = int(statistics.median(sizes)) if sizes else 0
    total_frames = last - first + 1
    free_bytes = _free_bytes(Path(project_root))
    return CacheSnapshot(
        node_path=node_path,
        source_scene=source_scene,
        scan=scan,
        estimated_total_bytes=typical_size * total_frames,
        free_bytes=free_bytes,
        current_upstream=current_upstream,
        published_upstream=published_upstream,
    )


def validate_cache(
    snapshot: CacheSnapshot,
    profile: CacheProfile = CacheProfile(),
) -> DiagnosticBag:
    """Return actionable cache blockers and production-risk warnings."""

    location = DiagnosticLocation(
        host="houdini",
        resource=snapshot.source_scene,
        object_path=snapshot.node_path,
        property_name="filecache",
    )
    diagnostics = DiagnosticBag()
    if not snapshot.scan.existing:
        diagnostics.add(
            Diagnostic(
                "CACHE_SEQUENCE_EMPTY",
                Severity.ERROR,
                "The cache contains no frames in the requested range.",
                location,
                "Cook the cache or correct the output pattern and frame range.",
            )
        )
    elif snapshot.scan.missing:
        preview = ", ".join(str(frame) for frame in snapshot.scan.missing[:8])
        remainder = len(snapshot.scan.missing) - 8
        if remainder > 0:
            preview += f" and {remainder} more"
        diagnostics.add(
            Diagnostic(
                "CACHE_FRAMES_MISSING",
                Severity.ERROR if profile.require_complete else Severity.WARNING,
                f"Cache is missing frame(s): {preview}.",
                location,
                "Resume only the missing frames before publishing.",
            )
        )
    if snapshot.scan.outside_range:
        diagnostics.add(
            Diagnostic(
                "CACHE_FRAMES_OUTSIDE_RANGE",
                Severity.INFO,
                f"Cache contains {len(snapshot.scan.outside_range)} frame(s) outside the requested range.",
                location,
            )
        )
    if (
        snapshot.current_upstream is not None
        and snapshot.published_upstream is not None
        and snapshot.current_upstream != snapshot.published_upstream
    ):
        diagnostics.add(
            Diagnostic(
                "CACHE_UPSTREAM_STALE",
                Severity.ERROR,
                "The cache was produced from a different upstream dependency state.",
                location,
                "Re-cook the cache or restore the recorded upstream inputs.",
            )
        )
    if snapshot.estimated_total_bytes > profile.storage_budget_bytes:
        diagnostics.add(
            Diagnostic(
                "CACHE_STORAGE_BUDGET",
                Severity.WARNING,
                f"Estimated cache size is {snapshot.estimated_total_bytes} bytes; budget is {profile.storage_budget_bytes}.",
                location,
                "Choose an approved higher budget or reduce cache resolution/channels.",
            )
        )
    missing_bytes = max(
        0,
        snapshot.estimated_total_bytes
        - _estimated_existing_bytes(snapshot),
    )
    if missing_bytes > snapshot.free_bytes:
        diagnostics.add(
            Diagnostic(
                "CACHE_DISK_SPACE",
                Severity.ERROR,
                f"Completing the cache may require {missing_bytes} bytes but only {snapshot.free_bytes} are free.",
                location,
                "Select another cache root or free sufficient storage before cooking.",
            )
        )
    return diagnostics


def missing_frames(snapshot: CacheSnapshot) -> tuple[int, ...]:
    """Return the exact deterministic resume set for a cache node."""

    return snapshot.scan.missing


def _estimated_existing_bytes(snapshot: CacheSnapshot) -> int:
    total_frames = snapshot.scan.last - snapshot.scan.first + 1
    if total_frames <= 0:
        return 0
    typical = snapshot.estimated_total_bytes // total_frames
    return typical * len(snapshot.scan.existing)


def _free_bytes(path: Path) -> int:
    import shutil

    existing = path.resolve(strict=False)
    while not existing.exists() and existing != existing.parent:
        existing = existing.parent
    return shutil.disk_usage(existing).free

