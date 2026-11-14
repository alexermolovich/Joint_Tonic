# Batch Variable-Length Episodes with Masks

## Intuition

A neural policy often expects one rectangular batch, while recordings end at different times. Padding supplies shape; a mask preserves meaning. A zero action can be a real command, so searching for nonzero values cannot recover episode length.

## Keep one row per episode

For B episodes with lengths $T_b$ and common width D, set $L=\max_b T_b$. The padded tensor $X\in\mathbb R^{B\times L\times D}$ and validity $M\in\{0,1\}^{B\times L}$ obey

$$
X_{b,t,d}=\begin{cases}E_{b,t,d},&t<T_b,\\0,&t\ge T_b,\end{cases}
\qquad M_{b,t}=\mathbf1[t<T_b].
$$

$E_b$ is the supplied episode array. Indices b,t,d mean episode, timestep and channel. Numeric units and frames follow each upstream channel unchanged; the function neither aligns clocks nor converts units. Lengths are counts of samples, not seconds.

## Visual: data and validity are separate

| Episode | t0 values | t1 values | Validity | Length |
|---|---|---|---|---:|
| 0 | [1,2] | [3,4] | [true,true] | 2 |
| 1 | [5,6] | [0,0] | [true,false] | 1 |

The second row's padded pair never becomes a demonstration target. The table is a static tensor trace and text alternative.

## Mask before reducing

A later loss must exclude padded timesteps from both its numerator and denominator. Counting all BL positions makes short episodes artificially easy. This component only constructs the mask; it does not choose a loss or promise that downstream code uses the mask correctly.

## Why this matters on a robot

A recurrent policy must also reset at episode boundaries. Concatenating recordings can invent a transition from the end of one manipulation to the beginning of another. Padding does not authorize such a transition, even when two adjacent observations look similar.

## Questions

1. Why is an all-zero observation not enough to identify padding?
2. Why bound BLD instead of the sum of observed episode sizes?

## Sources and prerequisites

robomimic motivates careful offline data handling and comparing supervised objectives with closed-loop evaluation. The exact bounded interface and deterministic policy here are original teaching choices, not the complete robomimic data loader or evaluation system. [Primary source](https://arxiv.org/abs/2108.03298), Offline demonstration evaluation and stopping criteria. Prerequisites: the component conventions defined in the statement; no Python or mathematics tutorial is assumed.

