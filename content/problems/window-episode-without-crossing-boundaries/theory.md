# Window an Episode Without Crossing Boundaries

## Intuition

A training window must describe one robot episode. Sliding over the concatenated dataset without checking boundaries creates impossible transitions between unrelated scenes.

## Mathematics and physical meaning

For one run occupying half-open rows $[a,b)$, length $L=b-a$, use start indices $s_k=a+kh$ where $h$ is stride in frames. Keep only $s_k+w\le b$, where $w$ is window length. Each output row is
$$[s_k,s_k+1,\ldots,s_k+w-1].$$
The number of windows in this run is $\max(0,1+\lfloor(L-w)/h\rfloor)$. All indices are global dataset row indices, not episode-local offsets.

## Visual trace

| Run | Rows | Width 2, stride 1 windows |
|---|---|---|
| episode 4 | 0,1,2 | [0,1], [1,2] |
| episode 8 | 3,4 | [3,4] |
| forbidden | 2,3 | crosses episode boundary |

This static table is also the text alternative; no animation is required.

## Worked examples

1. `episode_ids=[4,4,4,8,8], window=2, stride=1` → `[[0,1],[1,2],[3,4]]`.
2. `episode_ids=[1,1,1,1,2], window=3, stride=2` → `[[0,1,2]]`; no partial window is returned.

## Why this matters on a robot

A synthetic transition from the end of one task to the start of another corrupts action targets and reward labels. Episode-level splitting and this boundary-preserving window operation solve different leakage risks.

## Sources and prerequisites

Original pedagogical robotics component; no external data or paper reproduction claim.
