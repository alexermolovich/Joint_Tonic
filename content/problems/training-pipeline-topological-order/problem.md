# Topologically Schedule a Training Pipeline DAG

**Local Python exercise · content version 1.0.0.**

A training stage may run only after every stage supplying its artifacts. Produce one deterministic serial order; do not execute jobs.

## Function contract

~~~python
def schedule_pipeline(nodes: list[str],
                      edges: list[tuple[str, str]]) -> list[str]:
    ...
~~~

Each (producer, consumer) edge requires producer to appear before consumer. IDs match [a-z][a-z0-9_-]{0,63}; nodes are unique, case-sensitive ASCII strings. Every endpoint must be declared. Duplicate edges are treated once.

At each step choose the lexicographically smallest **currently ready** remaining node: one whose predecessors have all appeared. Return a fresh list containing every node exactly once. This defines the lexicographically smallest topological order. Inputs are not modified.

Limits: at most 10,000 nodes and 50,000 edges. A graph is one versioned pipeline snapshot. IDs and precedence edges have no physical units or coordinate frame. There are no durations, timestamp comparisons, retries, resource capacities, or concurrent execution in this contract. CPU Python objects only.

## Errors and empty inputs

Raise ValueError for non-list outer containers, invalid/duplicate node IDs, edges other than two-item tuples of declared IDs, exceeded limits, or **any directed cycle**. A self-loop is a cycle. Reject a cyclic disconnected component even when other stages could run; never return a partial schedule. Empty nodes and edges return [].

## Worked example 1 — newly ready work

~~~python
nodes = ["z-audit", "decode", "train"]
edges = [("decode", "train")]
# Output: ["decode", "train", "z-audit"]
~~~

Initially decode and z-audit are ready. After decode, train becomes ready and sorts before z-audit. Returning entire precomputed ready layers would violate this tie-break.

## Worked example 2 — merging inputs

~~~python
nodes = ["report", "labels", "fit", "images"]
edges = [("images", "fit"), ("labels", "fit"), ("fit", "report")]
# Output: ["images", "labels", "fit", "report"]
~~~

Fit must wait for both inputs; alphabetical position alone cannot move fit before them.

## Runtime budget

CPython 3.12.3 on the isolated local CPU worker. Limits: 10 CPU seconds, 18 wall seconds, 4 GiB address space per process, and 64 KiB output. The function uses Python standard-library data structures; no simulator is required.
