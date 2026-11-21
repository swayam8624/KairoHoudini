# Teaching source map — KairoHoudini

Houdini simulation/cache publication tooling.

Read these source links in order, identify the caller and callee for each public API, then check the error/ownership contract and its tests.

## Reading order

1. [`README.md`](README.md)
2. [`pyproject.toml`](pyproject.toml)
3. [`packages`](packages)
4. [`toolbar`](toolbar)
5. [`scripts`](scripts)
6. [`tests`](tests)
7. [`docs`](docs)

## Repository integration and API contracts

Houdini hosts Python tools that inspect cache ranges and provenance; KairoPipelineCore supplies shared publication validation. No Houdini license/runtime is bundled by a Python test.

## Teaching standards

- Comments explain invariants, decision reasons, lifetime, prerequisites and cross-file effects; they do not narrate obvious statements.
- Follow upstream interfaces before implementation details; distinguish implemented, host-verified and planned features.
- Run available tests at a pinned commit and consult [STATUS.md](STATUS.md) / [STATUS.yaml](STATUS.yaml) before declaring completion.
- Reuse original contributions under [LICENSE](LICENSE), subject to third-party code and asset terms.
