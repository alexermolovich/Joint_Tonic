# Invalidate Cached Artifacts After an Upstream Change

**Local Python exercise · content version 1.0.0.**

The dataset version changed. A feature artifact is currently uncached, but an old model and its report remain cached. Identify stale cache entries without deleting anything.

## Function contract

~~~python
def invalidated_artifacts(
    dependencies: dict[str, list[str]],
    changed: list[str],
    cached: list[str],
) -> list[str]:
    ...
~~~

Every dictionary key declares one artifact. Its list contains that artifact's **direct parents**, not consumers. All IDs match [a-z][a-z0-9_-]{0,63}; every parent, changed ID, and cached ID must be a declared key. Parent lists, changed, and cached may repeat IDs; repeats count once.

The graph must be a DAG. An empty parent list means an input artifact. Start with changed artifacts, follow all consumers transitively, and return only reached IDs that are cached, in ascending Python string order. Include a changed root itself if it is cached. Continue traversal through uncached intermediates. Return a new list and do not mutate inputs or perform filesystem operations.

At most 10,000 artifacts, 50,000 parent-list entries total, and 10,000 entries in each of changed and cached. One snapshot is supplied. IDs and edges are dimensionless; no coordinate frame or event timestamps apply. An upstream caller has already determined changed versions; this function does not compare files, hashes, or modification times. CPU Python data only.

## Errors and empty inputs

Raise ValueError for a non-dict dependencies argument, non-list parent/changed/cached collections, invalid or undeclared IDs, exceeded limits, or any cycle including a self-loop. Validate the complete graph even when cached or changed is empty. Error wording is not graded. Empty inputs return []; no changes or no cached artifacts returns [] on a valid graph.

## Worked example 1 — missing intermediate cache entry

~~~python
dependencies = {"raw": [], "features": ["raw"], "model": ["features"],
                "report": ["model"], "lookup": []}
changed = ["raw"]
cached = ["model", "report", "lookup"]
# Output: ["model", "report"]
~~~

Features are uncached, but still transmit the dependency from raw to model. Lookup is independent.

## Worked example 2 — the changed artifact is cached

~~~python
dependencies = {"raw": [], "model": ["raw"], "report": ["model"]}
changed = ["model"]
cached = ["raw", "model", "report"]
# Output: ["model", "report"]
~~~

The changed model invalidates itself and its report. Raw is upstream, so it remains reusable.

## Runtime budget

CPython 3.12.3 on the isolated local CPU worker. Limits: 10 CPU seconds, 18 wall seconds, 4 GiB address space per process, and 64 KiB output. No simulator or network access is required.
