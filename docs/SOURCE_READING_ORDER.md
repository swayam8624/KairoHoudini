# KairoHoudini — teaching source reading order

Start with the [README](../README.md), then follow this **workflow-oriented** path. These repositories integrate with [KairoPipelineCore](https://github.com/swayam8624/KairoPipelineCore), the host-neutral Python contracts. The order below describes how a user action reaches validated, publishable data—not the import/build order.

1. [scripts/python/kairo_houdini/__init__.py](../scripts/python/kairo_houdini/__init__.py) — read API inputs, output contracts, errors and downstream caller.
2. [scripts/python/kairo_houdini/hom.py](../scripts/python/kairo_houdini/hom.py) — read API inputs, output contracts, errors and downstream caller.
3. [scripts/python/kairo_houdini/cacheguard.py](../scripts/python/kairo_houdini/cacheguard.py) — read API inputs, output contracts, errors and downstream caller.
4. [scripts/python/kairo_houdini/publisher.py](../scripts/python/kairo_houdini/publisher.py) — read API inputs, output contracts, errors and downstream caller.
5. [packages/kairo_houdini.json](../packages/kairo_houdini.json) — read API inputs, output contracts, errors and downstream caller.
6. [toolbar/KairoCacheGuard.shelf](../toolbar/KairoCacheGuard.shelf) — read API inputs, output contracts, errors and downstream caller.
7. [tests/test_cacheguard.py](../tests/test_cacheguard.py) — read API inputs, output contracts, errors and downstream caller.
8. [tests/test_hom_adapter.py](../tests/test_hom_adapter.py) — read API inputs, output contracts, errors and downstream caller.
9. [tests/test_publisher.py](../tests/test_publisher.py) — read API inputs, output contracts, errors and downstream caller.
10. [tests/test_package.py](../tests/test_package.py) — read API inputs, output contracts, errors and downstream caller.

## Data flow

Houdini shelf selection → hou/HOM adapter reads a cache node, upstream parameters and $F frame token → normalized #### pattern → KairoPipelineCore SequenceScan → CacheSnapshot and CacheProfile checks (staleness, missing frames, budget, free space) → publisher checks SHA-256 per frame → validated atomic cache publish manifest. The shared core does not import hou.

## Boundary of the tests

Frame-sequence validation under standard Python does not certify that live houdini nodes, $F expansions, hython, or package shelf installation work without a native host test.

## Teaching exercises

1. Trace one host action or command into a pure validation function and its structured diagnostic.
2. Identify where filesystem paths are normalized and hashed before publishing.
3. Feed malformed/missing files to the host-neutral path and locate the specific failure/diagnostic.
4. Run the portable tests; then read the native verification checklist before claiming host support.
5. Explain why a dry-run plan, a completed atomic publish, and a native host import are three different events.

## Licensing

Preserve the repository's existing [LICENSE](../LICENSE). The original source and documentation permit learning and development according to that file; external DCC SDKs, plugins, images and example assets retain their own terms.
