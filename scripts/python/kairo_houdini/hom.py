"""Houdini Object Model adapter for CacheGuard."""

from __future__ import annotations

import json
import os
from pathlib import Path
import re
from typing import Any

from kairo_pipeline.fingerprint import fingerprint_bytes

from .cacheguard import CacheProfile, inspect_cache, validate_cache


try:
    import hou  # type: ignore
except ImportError:  # Host-neutral unit tests intentionally run without Houdini.
    hou = None


_FRAME_TOKEN = re.compile(r"\$F([1-9]|1[0-2])?|\$\{F([1-9]|1[0-2])?\}")
_OUTPUT_PARMS = ("file", "sopoutput", "output", "filepath")


def houdini_pattern_to_core(value: str) -> str:
    """Convert exactly one Houdini `$F` token to the shared hash syntax."""

    if not isinstance(value, str) or not value:
        raise ValueError("Houdini cache path must not be empty")
    matches = list(_FRAME_TOKEN.finditer(value))
    if len(matches) != 1:
        raise ValueError("Houdini cache path must contain exactly one $F frame token")
    match = matches[0]
    padding_text = match.group(1) or match.group(2)
    padding = int(padding_text) if padding_text else 1
    return f"{value[:match.start()]}{'#' * padding}{value[match.end():]}"


def inspect_selected_cache(profile: CacheProfile | None = None) -> tuple[Any, Any]:
    """Inspect the selected Houdini cache node and return snapshot/diagnostics."""

    host = _require_hou()
    selected = host.selectedNodes()
    if len(selected) != 1:
        raise ValueError("select exactly one Houdini cache node")
    node = selected[0]
    output_parm = next((node.parm(name) for name in _OUTPUT_PARMS if node.parm(name)), None)
    if output_parm is None:
        raise ValueError(f"selected node has no supported output path parameter: {node.path()}")

    project_root_text = os.environ.get("KAIRO_PROJECT_ROOT") or host.getenv("JOB")
    if not project_root_text:
        raise ValueError("set KAIRO_PROJECT_ROOT or Houdini JOB before using CacheGuard")
    project_root = Path(project_root_text).expanduser().resolve(strict=False)
    output_pattern = _expand_pattern(host, output_parm.unexpandedString())
    output_path = Path(output_pattern).expanduser().resolve(strict=False)
    try:
        relative_pattern = output_path.relative_to(project_root).as_posix()
    except ValueError as error:
        raise ValueError("cache output must remain inside the project root") from error

    first, last = _frame_range(host, node)
    current_upstream = fingerprint_bytes(_upstream_payload(node))
    snapshot = inspect_cache(
        project_root,
        node_path=node.path(),
        source_scene=_source_scene(project_root, host.hipFile.path()),
        output_pattern=relative_pattern,
        first=first,
        last=last,
        current_upstream=current_upstream,
    )
    return snapshot, validate_cache(snapshot, profile or CacheProfile())


def show_selected_cacheguard() -> None:
    """Run CacheGuard and display an artist-readable Houdini message."""

    host = _require_hou()
    try:
        snapshot, diagnostics = inspect_selected_cache()
        if diagnostics:
            lines = [
                f"[{item.severity.value.upper()}] {item.code}: {item.message}"
                for item in diagnostics
            ]
        else:
            lines = ["Cache is complete, current, and within configured budgets."]
        lines.append(
            f"Frames: {snapshot.scan.first}-{snapshot.scan.last}; "
            f"missing: {len(snapshot.scan.missing)}; "
            f"estimated bytes: {snapshot.estimated_total_bytes}"
        )
        host.ui.displayMessage(
            "\n".join(lines),
            title="Kairo CacheGuard",
            severity=(
                host.severityType.Error
                if diagnostics.blocks_publish
                else host.severityType.Message
            ),
        )
    except (OSError, TypeError, ValueError, RuntimeError) as error:
        host.ui.displayMessage(
            str(error),
            title="Kairo CacheGuard",
            severity=host.severityType.Error,
        )


def _expand_pattern(host: Any, value: str) -> str:
    shared = houdini_pattern_to_core(value)
    marker = "__KAIRO_FRAME_TOKEN__"
    token_match = re.search(r"#{1,12}", shared)
    assert token_match is not None
    protected = f"{shared[:token_match.start()]}{marker}{shared[token_match.end():]}"
    expanded = host.text.expandString(protected)
    return expanded.replace(marker, token_match.group(0))


def _frame_range(host: Any, node: Any) -> tuple[int, int]:
    first_parm = node.parm("f1")
    last_parm = node.parm("f2")
    if first_parm is not None and last_parm is not None:
        first = int(first_parm.eval())
        last = int(last_parm.eval())
    else:
        playback = host.playbar.playbackRange()
        first, last = int(playback[0]), int(playback[1])
    if first > last:
        raise ValueError("cache start frame must not exceed end frame")
    return first, last


def _upstream_payload(node: Any) -> bytes:
    pending = list(node.inputs())
    visited: set[str] = set()
    records: list[dict[str, object]] = []
    while pending:
        current = pending.pop()
        if current is None or current.path() in visited:
            continue
        if len(visited) >= 10_000:
            raise ValueError("upstream graph exceeds 10000 nodes")
        visited.add(current.path())
        parameters: dict[str, str] = {}
        for parm in current.parms():
            try:
                parameters[parm.name()] = parm.unexpandedString()
            except Exception:
                parameters[parm.name()] = repr(parm.eval())
        records.append(
            {
                "path": current.path(),
                "type": current.type().nameWithCategory(),
                "parameters": parameters,
            }
        )
        pending.extend(current.inputs())
    return json.dumps(
        sorted(records, key=lambda record: str(record["path"])),
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")


def _source_scene(project_root: Path, value: str) -> str:
    source = Path(value).expanduser().resolve(strict=False)
    try:
        return source.relative_to(project_root).as_posix()
    except ValueError:
        return f"external/{source.name or 'untitled.hip'}"


def _require_hou() -> Any:
    if hou is None:
        raise RuntimeError("Houdini's hou module is not available")
    return hou

