# KairoHoudini: linked source-reading order

Read cacheguard and sequence/publish contracts before native HOM integration: pure filesystem diagnostics can run outside Houdini, but actual Houdini object-model work requires Houdini's Python host. Track missing simulation cache frames, stale upstream input and disk budgets.

## APIs and boundaries

cacheguard inspects cache sequences; publisher prepares provenance manifests using KairoPipelineCore; hom.py uses Houdini's host APIs. Avoid modifying artist scenes and simulation caches during a dry-run. Verification must separate mock/pure tests from a native Houdini session.

## Read these files (8)

1. [`scripts/python/kairo_houdini/cacheguard.py`](scripts/python/kairo_houdini/cacheguard.py) — inspect the host API dependencies, validation, returned evidence and failure handling; compare its callers to corresponding tests.
2. [`scripts/python/kairo_houdini/publisher.py`](scripts/python/kairo_houdini/publisher.py) — inspect the host API dependencies, validation, returned evidence and failure handling; compare its callers to corresponding tests.
3. [`scripts/python/kairo_houdini/hom.py`](scripts/python/kairo_houdini/hom.py) — inspect the host API dependencies, validation, returned evidence and failure handling; compare its callers to corresponding tests.
4. [`tests/test_cacheguard.py`](tests/test_cacheguard.py) — inspect the host API dependencies, validation, returned evidence and failure handling; compare its callers to corresponding tests.
5. [`tests/test_hom_adapter.py`](tests/test_hom_adapter.py) — inspect the host API dependencies, validation, returned evidence and failure handling; compare its callers to corresponding tests.
6. [`tests/test_publisher.py`](tests/test_publisher.py) — inspect the host API dependencies, validation, returned evidence and failure handling; compare its callers to corresponding tests.
7. [`scripts/python/kairo_houdini/__init__.py`](scripts/python/kairo_houdini/__init__.py) — inspect the host API dependencies, validation, returned evidence and failure handling; compare its callers to corresponding tests.
8. [`tests/test_package.py`](tests/test_package.py) — inspect the host API dependencies, validation, returned evidence and failure handling; compare its callers to corresponding tests.

## License and verification

This repository preserves its existing [LICENSE](LICENSE) for original work; external artist tools, SDKs, output media and third-party assets keep their own terms. Educational reuse and further development are encouraged within those licenses. Use [README](README.md) for actual host configuration. A source guide or passing pure-Python unit tests do not imply a successful native-host integration run.
