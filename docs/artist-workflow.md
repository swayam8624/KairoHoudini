# Artist workflow

1. Select a file-cache node whose output contains one Houdini frame token.
2. Run **Kairo > Inspect Selected Cache** from the Kairo shelf.
3. Resolve blocking diagnostics: invalid paths, missing frames, stale upstream
   inputs, insufficient free space, or a cache over the configured budget.
4. Resume only the reported missing frames instead of recooking the sequence.
5. Publish the completed cache. CacheGuard fingerprints every frame and writes
   a `kairo.publish.v1` manifest into an immutable version directory.

The tool reads project files but never deletes cache frames. Publication first
plans and validates the complete bundle, stages it in a temporary directory,
then atomically makes the version visible.

## Native release gate

Host-neutral rules and publication logic are tested in CI. A release that
changes the HOM adapter or shelf must additionally be exercised inside Houdini:

- package loads with no startup error;
- shelf tool inspects a selected file-cache node;
- `$F`, `${F}`, and padded `$F4` paths resolve correctly;
- a deliberately missing frame is reported;
- a complete sequence publishes and its manifest reloads.
