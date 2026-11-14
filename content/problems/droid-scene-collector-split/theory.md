# Split Demonstrations by Scene and Collector

## Intuition

A held-out room can leak through a collector who also recorded another room. Treat shared scene and collector identities as connectivity, then hold out complete connected components.

## Formal model

Build an undirected episode relation $i\sim j$ when scene IDs match or collector IDs match. Let $C(i)$ be its transitive connected component and $H$ the declared held-out scene set.
$$i\in D_{\rm test}\iff\exists j\in C(i):\operatorname{scene}(j)\in H.$$
Each component receives its smallest episode ID as a deterministic label. Scene and collector namespaces remain distinct even when their strings coincide. This prevents these declared groups from crossing splits; it does not detect unrecorded overlap.

## Worked state and shape trace

```text
a--samecollector--b--samescene--c | d; holdscene(a) -> entire a, b, c component in test.
```

The ordered text trace is also the visual alternative; no animation is required.

## Why this matters on a robot

A large robotics corpus can contain repeated rooms and operator styles. Frame-level random splits can overstate generalization; connected holdout may also leave too little training data, which should be reported rather than silently weakened.

## Source and scope

Original bounded component inspired by [2024-droid](https://arxiv.org/abs/2403.12945). It does not reproduce the full paper or establish hardware safety or data-use authorization.
