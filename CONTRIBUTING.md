# Contributing

Use a feature branch and keep changes focused on CacheGuard. Run the complete
host-neutral verification before opening a pull request:

```bash
PYTHONPATH=../KairoPipelineCore/src:scripts/python \
  python3 -m unittest discover -s tests -v
python3 -m compileall -q scripts/python tests
python3 -m json.tool packages/kairo_houdini.json >/dev/null
xmllint --noout toolbar/KairoCacheGuard.shelf
```

Changes touching `hom.py`, shelf tools, or Houdini packaging also require a
native Houdini smoke test. State the Houdini version and license tier used.
