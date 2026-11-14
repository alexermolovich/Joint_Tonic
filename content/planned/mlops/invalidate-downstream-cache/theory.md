# Theory: cache existence is not cache validity

## Intuition

A cache answers whether an artifact is available. It does not answer whether that artifact still belongs to the current experiment. If a model was trained on old features, keeping the model file does not make it valid after those features change.

Represent dependencies independently of cache membership. A missing intermediate artifact still connects a changed dataset to a cached model.

## From parent lists to a stale set

Let $V$ be artifact IDs, $P(v)\subseteq V$ the parents stored under consumer $v$, $C\subseteq V$ the changed IDs, and $K\subseteq V$ the currently cached IDs. All are dimensionless metadata sets from one graph/version snapshot.

The producer-to-consumer edge set is

$$
E=\{(u,v):v\in V,\ u\in P(v)\}.
$$

This reverses the input lookup direction: dependencies[v] lists incoming neighbors, but a changed artifact affects outgoing consumers. Define

$$
A_0=C,\qquad A_{k+1}=A_k\cup\{v:P(v)\cap A_k\ne\varnothing\}.
$$

At the fixed point $A_\star$, return the sorted set

$$
I=K\cap A_\star.
$$

Unlike the blast-radius exercise, changed roots are retained when cached. Cache membership filters the **answer**, not the traversal. Removing uncached nodes before reachability would change the graph and can incorrectly certify stale outputs as reusable.

This policy is conservative: an upstream version change invalidates descendants even if recomputing them might coincidentally produce identical values. Content-based reuse and dependency-complete cache keys are a later extension.

## Visual: propagate through what is not cached

~~~mermaid
flowchart LR
  R["raw: changed"] --> F["features: uncached"]
  F --> M["model: cached"]
  M --> P["report: cached"]
  L["lookup: cached, unrelated"]
~~~

**Text alternative:** raw feeds features, features feed model, and model feeds report. Lookup has no connection. Features are uncached but remain part of the path. The diagram is static.

| Artifact | Reached from raw? | Cached? | Invalidate? |
|---|---|---|---|
| raw | yes | no | no cache entry |
| features | yes | no | no cache entry |
| model | yes | yes | yes |
| report | yes | yes | yes |
| lookup | no | yes | no |

Thus the first worked output is ["model", "report"]. The graph contains causal metadata, not wall-clock timestamps: a recently copied stale file is still stale.

## Why this matters on a robot

Calibration, normalization parameters, robot firmware assumptions, and evaluator versions can all be dependencies. A policy evaluated against a stale transform can appear validated while belonging to a different physical contract. This function only plans invalidation; deployment gates still need versioned evidence and a separate controlled recomputation step.

A common failure is walking parent lists directly from the changed node, which invalidates inputs instead of consumers. Another is treating an uncached node as a dead end.

TFX provides the pipeline context; the fixed-point invalidation rule is our teaching design. [TFX primary source](https://research.google/pubs/tfx-a-tensorflow-based-production-scale-machine-learning-platform/).

## Questions

1. Why should raw remain valid when only model changes?
2. Would equal output filenames prove that an old model cache entry is reusable?

Prerequisites: [blast radius](../dependency-graph-blast-radius/statement.md) and [DAG scheduling](../training-pipeline-topological-order/statement.md).
