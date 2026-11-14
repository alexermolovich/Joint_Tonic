# Theory: artifact readiness determines execution order

## Intuition

A stage name is not enough to determine when it may run. A policy trainer might need both transformed sensor episodes and labels. One completed parent is insufficient: all required artifacts must be available.

The exercise reduces readiness to explicit edges. It does not estimate job duration, reserve GPUs, or recover a failed worker. Separating precedence from those scheduling concerns makes correctness visible.

## The remaining-parent invariant

Let $G=(V,E)$ be the deduplicated directed graph and $D\subseteq V$ the stages already emitted. For each un-emitted stage $v$, define its remaining indegree

$$
d_D(v)=|\{u\in V\setminus D:(u,v)\in E\}|.
$$

The ready set is $Q_D=\{v\in V\setminus D:d_D(v)=0\}$. All quantities are dimensionless graph metadata. If $Q_D$ is nonempty, choose

$$
v^\star=\min_{\mathrm{lex}} Q_D
$$

and append it. Decrease the remaining count of each consumer of $v^\star$. A duplicate edge must not decrement twice unless it also counted twice; deduplicating edges makes the invariant clear.

Choosing the smallest legal next element produces the required lexicographically smallest valid list. This is not the globally alphabetized list: dependencies can force a later-sorting input before an earlier-sorting consumer.

If some nodes remain but the ready set is empty, the remaining graph contains a cycle. Each remaining node has a remaining predecessor; repeatedly following predecessors in a finite set eventually revisits a node. Therefore a valid full DAG order cannot be completed.

## Visual: two artifacts unlock a trainer

~~~mermaid
flowchart LR
  I["images"] --> F["fit"]
  L["labels"] --> F
  F --> R["report"]
~~~

**Text alternative:** fit consumes both images and labels; report consumes fit. The graph is static and has no motion dependence.

| Completed before choice | Ready IDs | Chosen |
|---|---|---|
| none | images, labels | images |
| images | labels | labels |
| images, labels | fit | fit |
| images, labels, fit | report | report |

For the other worked input, decode unlocks train while z-audit is waiting. Reconsider the ready set after every emitted node, producing decode → train → z-audit.

## Why this matters on a robot

Starting training before calibration-aware transforms finish can consume absent or stale artifacts. An order that respects all declared parents prevents this particular mistake. It does not prove that artifact versions are correct; cache validity and lineage are separate checks.

A dangerous failure is returning the acyclic prefix while hiding a cycle elsewhere. The platform could falsely claim that a complete model bundle was scheduled. This contract requires a whole-graph failure instead.

TFX supplies the integrated pipeline context; this deterministic algorithm is an original teaching design. [TFX primary source](https://research.google/pubs/tfx-a-tensorflow-based-production-scale-machine-learning-platform/).

## Questions

1. Why does sorting each ready layer differ from selecting one smallest-ready stage at a time?
2. Can a valid topological order prove that a model was evaluated on the intended dataset version?

Prerequisite: [Dependency-graph blast radius](../dependency-graph-blast-radius/statement.md).
