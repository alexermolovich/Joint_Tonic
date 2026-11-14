# Build Padding and Validity Masks for Robot Sequences

## Intuition

Padding is storage, not evidence. A mask needs to protect both the query and key sides: a padded query must not attend to real history, even if a causal triangle would allow it.

## Mathematics and physical meaning

For batch row $b$, length $\ell_b$, query time $i$ and key time $j$ (all frame indices), define
$$V_{bi}=\mathbf1[i<\ell_b],\qquad A_{bij}=V_{bi}\land V_{bj}\land\mathbf1[j\le i].$$
$V$ has shape $(B,T)$ and $A$ has shape $(B,T,T)$. The diagonal is allowed for valid tokens; every row and column belonging to padding is false. This produces boolean attention permissions, not additive logits.

## Visual trace

| Query i / key j, length=2, T=3 | j=0 | j=1 | j=2 |
|---|---|---|---|
| i=0 | true | false | false |
| i=1 | true | true | false |
| i=2 | false | false | false |

This static table is also the text alternative; no animation is required.

## Worked examples

1. `lengths=[2,0], max_steps=3` → valid `[[True,True,False],[False,False,False]]`; the first attention matrix is the table above, the second is all false.
2. `lengths=[1], max_steps=1` → valid `[[True]]`, attention `[[[True]]]`.

## Why this matters on a robot

A padded action token attending to real observations can introduce loss on nonexistent actions. Conversely, reversing the triangle leaks future sensor measurements into a policy that must operate causally.

## Sources and prerequisites

Original pedagogical robotics component; no external data or paper reproduction claim.
