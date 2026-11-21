# TEACHING MAP — scripts/python/kairo_houdini/__init__.py
# Houdini Python package entrypoint for cache diagnostics and publishing helpers. The
# portable pipeline contract lives in KairoPipelineCore; HOM-host integration lives in
# hom.py.
# Consult READING_ORDER.md for related host APIs, validation and tests.

"""Houdini CacheGuard validation and publication tools."""

from .cacheguard import (
    CacheProfile,
    CacheSnapshot,
    inspect_cache,
    missing_frames,
    validate_cache,
)
from .publisher import CachePublishResult, publish_cache

__version__ = "0.1.0"

__all__ = [
    "CacheProfile",
    "CacheSnapshot",
    "CachePublishResult",
    "inspect_cache",
    "missing_frames",
    "publish_cache",
    "validate_cache",
    "__version__",
]
