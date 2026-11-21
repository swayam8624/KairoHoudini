# Teaching source map — KairoHoudini

Houdini simulation/cache publication tooling.

Read these source links in order, identify the caller and callee for each public API, then check the error/ownership contract and its tests.

## Reading order

1. [`README.md`](../README.md)
2. [`pyproject.toml`](../pyproject.toml)
3. [`packages`](../packages)
4. [`toolbar`](../toolbar)
5. [`scripts`](../scripts)
6. [`tests`](../tests)
7. [`docs`](../docs)

## Repository integration and API contracts

Houdini hosts Python tools that inspect cache ranges and provenance; KairoPipelineCore supplies shared publication validation. No Houdini license/runtime is bundled by a Python test.

## Teaching standards

- Comments explain invariants, decision reasons, lifetime, prerequisites and cross-file effects; they do not narrate obvious statements.
- Follow upstream interfaces before implementation details; distinguish implemented, host-verified and planned features.
- Run available tests at a pinned commit and consult [STATUS.md](../STATUS.md) / [STATUS.yaml](../STATUS.yaml) before declaring completion.
- Reuse original contributions under [LICENSE](../LICENSE), subject to third-party code and asset terms.


## Complete source-file inventory

After the curated teaching path, follow this deterministic inventory of first-party source, scripts, shaders, and tests. Grouping is a suggested learning order, not an indication that every function is already annotated. Vendored dependencies, ROMs, binaries, data, media, and generated evidence are excluded.

### Automation and tooling (4)

1. [`scripts/python/kairo_houdini/__init__.py`](../scripts/python/kairo_houdini/__init__.py)
2. [`scripts/python/kairo_houdini/cacheguard.py`](../scripts/python/kairo_houdini/cacheguard.py)
3. [`scripts/python/kairo_houdini/hom.py`](../scripts/python/kairo_houdini/hom.py)
4. [`scripts/python/kairo_houdini/publisher.py`](../scripts/python/kairo_houdini/publisher.py)

### Verification and tests (4)

1. [`tests/test_cacheguard.py`](../tests/test_cacheguard.py)
2. [`tests/test_hom_adapter.py`](../tests/test_hom_adapter.py)
3. [`tests/test_package.py`](../tests/test_package.py)
4. [`tests/test_publisher.py`](../tests/test_publisher.py)

Snapshot totals: 8 first-party source/build/test files, 22 tracked files overall. Re-audit when files are renamed or added.
