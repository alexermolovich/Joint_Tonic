# Detect Feedback Loops in an ML Pipeline

## Intuition

A deployed policy can change which episodes get collected. Those episodes change the next policy. A normal topological scheduler rejects this cycle, but an operational review needs to describe it. Grouping mutual influence reveals which components must be investigated together.

## Reachability in both directions

Let $G=(V,E)$ be the directed graph, where $V$ is the set of component IDs and $E$ contains producer-to-consumer edges. Write $u\leadsto v$ when a path of zero or more edges connects u to v. The relation

$$
u\sim v \iff (u\leadsto v)\land(v\leadsto u)
$$

partitions V into strongly connected components. A component C is returned exactly when

$$
|C|>1 \quad\text{or}\quad \exists u\in C:(u,u)\in E.
$$

Zero-length reachability makes every isolated vertex related to itself; the second rule prevents incorrectly calling every singleton a loop. Sorting is presentation policy, not part of reachability.

## Visual: cycle versus consumer

| Edge path | Can return to dataset? | Returned group |
|---|---|---|
| dataset → train → policy → logger → dataset | Yes | All four nodes |
| logger → dashboard | No | Dashboard excluded |

The arrows are logical influence, possibly across days of operation. The table is also a text alternative; no animation is required. In example1 the first row forms a four-node group even though a downstream node is reachable.

An iterative two-pass graph traversal can find these groups: finish a traversal of the original graph, then traverse reversed edges in descending finish order. Explicit stacks avoid failure on deep graphs. A simple cycle detector returning only true/false loses the grouping required here.

## Why this matters on a robot

A grasp policy that selects easy objects may produce training data dominated by its own preferences. Strongly connected metadata can identify a potential route; understanding whether the data is biased still needs a causal and statistical review. Missing collection-policy edges give false reassurance. Conversely, a declared control or logging cycle is not automatically a defect.

## Check your understanding

1. Why is dashboard excluded even though policy can affect it?
2. Why must a singleton have an explicit self-loop?

## Sources and prerequisites

The paper motivates inspecting direct and indirect feedback. Strongly connected components are an original finite-graph teaching tool; declared graph cycles do not prove a harmful statistical feedback effect, and absent edges can hide real loops. [Primary source](https://proceedings.neurips.cc/paper/2015/hash/86df7dcfd896fcaf2674f757a2463eba-Abstract.html), Section4: Feedback Loops. Prerequisites: [dependency-graph-blast-radius](/problems/dependency-graph-blast-radius); no Python or mathematics tutorial is assumed.
