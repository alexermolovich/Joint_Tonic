# Track Immutable Artifact References

## Intuition

A reference names immutable content, while replica locations can change. Losing every replica must not erase the object identity that recovery depends on.

## Formal model

For artifact $i$ with byte size $b_i$ and replica-node set $L_i$, physical storage is
$$B=\sum_i b_i|L_i|.$$
Put performs $L_i\leftarrow L_i\cup\{n\}$ and eviction performs $L_i\leftarrow L_i\setminus\{n\}$. Set updates explain retry idempotence; the identity pair(hash, size) never changes.

## Worked state and shape trace

```text
a identity(hash, size=4), locations{} -> putn1:{n1} -> duplicateput:{n1} -> putn2:{n1, n2} ->8bytes.
```

The ordered text trace is also the visual alternative; no animation is required.

## Why this matters on a robot

Object locality affects distributed robot-data processing. Treating replica retry as another physical copy inflates budgets; deleting lost identities prevents reproducible recovery.

## Source and scope

Original bounded component inspired by [2017-ray](https://arxiv.org/abs/1712.05889). It does not reproduce the full paper or establish hardware safety or data-use authorization.
