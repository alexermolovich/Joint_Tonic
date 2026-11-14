# Theory: follow a change through the robot ML system

## Intuition

A component's direct users are only the first layer of its impact. Updating camera calibration changes geometric features; a policy consumes those features, and a monitor summarizes the policy. The monitor may need review despite never opening the calibration file.

Follow declared dependencies rather than predicting whether values actually change. This gives a conservative review set relative to the supplied graph before retraining begins.

## Reachability with a clear direction

Let $G=(V,E)$ be a directed graph of component IDs. An edge $(u,v)\in E$ means consumer $v$ depends on producer $u$. IDs and edges are dimensionless metadata. Let $C\subseteq V$ contain unique changed IDs. Grow a set:

$$
S_0=C,\qquad
S_{k+1}=S_k\cup\{v:\exists u\in S_k,\ (u,v)\in E\}.
$$

The finite set never shrinks; it stabilizes after at most $|V|$ strict growth steps. At that fixed point $S_\star$, return

$$
B=\operatorname{sort}(S_\star\setminus C).
$$

A visited set avoids endlessly revisiting cycles. The subtraction ensures that a changed policy remains a root even if a feedback path reaches it again. Sorting is an output convention, not a schedule.

## Visual and worked propagation

~~~mermaid
flowchart LR
  C["calib: changed"] --> F["features: affected"]
  I["images: unchanged"] --> F
  F --> P["policy: affected"]
  P --> M["monitor: affected"]
~~~

**Text alternative:** calib feeds features, features feed policy, and policy feeds monitor. Images are another upstream input to features, so an outgoing traversal from calib never reaches images. This visual is static and requires no animation.

| Expansion | Newly reached |
|---|---|
| Start | calib |
| 1 | features |
| 2 | policy |
| 3 | monitor |

The three consumer IDs sort to ["features", "monitor", "policy"]. Traversing incoming edges would answer a different question: which dependencies the changed component requires.

## Why this matters on a robot

A calibration artifact can be as consequential as model weights. Its impact set helps select replay tests and owners before promoting a bundle. A missing dependency, however, makes the result incomplete even when traversal is flawless. Structural reachability cannot discover undocumented consumers or prove operational safety.

The paper motivates visibility into consumers and data dependencies; the graph algorithm above is an original operational decomposition. [Hidden Technical Debt in Machine Learning Systems](https://proceedings.neurips.cc/paper/2015/hash/86df7dcfd896fcaf2674f757a2463eba-Abstract.html).

## Questions

1. If both policy and data change in example 2, which IDs remain?
2. Why can correct traversal underestimate field impact?

Prerequisite: recognize a robot data → feature → policy pipeline. No Python or mathematics tutorial is assumed.
