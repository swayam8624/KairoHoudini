# Kairo Houdini CacheGuard

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

