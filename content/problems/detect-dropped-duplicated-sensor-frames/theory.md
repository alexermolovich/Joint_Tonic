# Detect Dropped and Duplicated Sensor Frames

## Intuition

Arrival counts alone cannot distinguish a repeated frame from a missed frame. Sequence counters expose both failures without assuming a constant frame rate.

## Mathematics and physical meaning

For observed IDs $s_0\le\cdots\le s_{N-1}$, define the count $c(k)=\sum_i\mathbf1[s_i=k]$. The missing set contains integers $k\in[s_0,s_{N-1}]$ with $c(k)=0$. The duplicate set contains $k$ with $c(k)>1$. A repeated ID is reported once regardless of its multiplicity. Counters are dimensionless and are not timestamps.

## Visual trace

For nonempty input, the two returned sets can be written as

$$
M=\{k\in\mathbb Z:s_0\le k\le s_{N-1},\ c(k)=0\},\qquad D=\{k:c(k)>1\}.
$$

Here $M$ contains missing IDs and $D$ duplicate IDs, each returned in ascending order. Both sets are empty when the input is empty.

| Counter | Observations | Classification |
|---|---|---|
| 3 | 1 | present |
| 4 | 2 | duplicate |
| 5 | 0 | missing |
| 6 | 1 | present |

This static table is also the text alternative; no animation is required.

## Worked examples

1. `[3,4,4,6]` → `{"missing": [5], "duplicates": [4]}`.
2. `[7,7,7]` → `{"missing": [], "duplicates": [7]}`; the repeated ID is listed once.

## Why this matters on a robot

A duplicated image can overweight a stationary observation; a dropped image can invalidate velocity estimates. A counter reset is a new stream segment, so this exercise rejects descending IDs instead of inventing losses across a reset.

## Sources and prerequisites

Original pedagogical robotics component; no external data or paper reproduction claim.
