# Kairo Houdini CacheGuard

**Study the implementation:** [linked file-reading order](docs/SOURCE_READING_ORDER.md) · [Houdini temporal cache preflight and publication](https://github.com/swayam8624/KairoPipelineCore/blob/docs/teaching-walkthrough-20261121/docs/CROSS_DCC_PUBLICATION_WALKTHROUGH.md).

CacheGuard is an artist-facing Houdini package for validating simulation cache
nodes, detecting incomplete or stale frame sequences, estimating storage cost,
and publishing immutable cache versions through `KairoPipelineCore`.

## Installation layout

The repository follows Houdini's package conventions. Link or copy
`packages/kairo_houdini.json` into `$HOUDINI_USER_PREF_DIR/packages`, keeping
the repository layout intact. The package uses `$HOUDINI_PACKAGE_PATH` to add
its parent repository to `HOUDINI_PATH`; Python modules live under
`scripts/python`.

## Development smoke

```bash
PYTHONPATH=../KairoPipelineCore/src:scripts/python \
  python3 -m unittest discover -s tests -v
```

Host-neutral tests run without Houdini. Native `hou` and `hython` verification
is a separate release gate and is never inferred from mocks.

## What artists get

- one-click inspection from a Kairo shelf;
- exact missing-frame ranges for resumable simulation work;
- stale-upstream, path, free-space, and cache-budget diagnostics;
- immutable cache publication with per-frame SHA-256 fingerprints;
- manifests that downstream Nuke and engine tools can validate.

See [the artist workflow](docs/artist-workflow.md) for the production path and
native release checklist.


## Source learning pathway

Follow [the linked reading order](docs/SOURCE_READING_ORDER.md) to trace module ownership, public interfaces, implementation, tests and cross-repository interaction. This path is designed for learners who want to understand both the algorithms and the API boundaries rather than just execute a sample.

## Open-source learning and extension

Original contributions may be learned from, modified and further developed under the applicable [LICENSE](LICENSE). Preserve required notices; external libraries, application-host SDKs, source adaptations, datasets and media retain their own terms. Check [STATUS.md](STATUS.md) and native-host evidence before treating a feature as verified.
