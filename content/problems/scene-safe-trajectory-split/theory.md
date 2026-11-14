# Split Robot Trajectories Without Scene Leakage

## Intuition

Adjacent robot trajectories can share backgrounds, object layouts and calibration. Randomly splitting individual trajectories can make validation look like memorization of the training environment. Group assignment holds out whole declared scenes, which tests a different question from holding out a few recordings inside the same scene.

## A deterministic scene decision

Let $s_i$ be the supplied scene ID of episode $i$, $r$ the nonnegative integer seed and $m\in\{0,\ldots,10000\}$ the validation threshold. Let $H$ denote SHA-256 on the exact UTF-8 bytes of the decimal seed, a zero separator and the scene ID. Define

$$
b_r(s)=\operatorname{uint64}_{\mathrm{big}}\!\left(H(\operatorname{str}(r)\Vert 0\Vert s)_{0:8}\right)\bmod10000.
$$

The symbol $\Vert$ means byte concatenation; the zero is exactly one zero byte, not a digit. The uint64 expression interprets eight bytes as unsigned big-endian. Buckets and seed are dimensionless. The partition function is

$$
p_i=\begin{cases}\mathrm{validation},&b_r(s_i)<m,\\ \mathrm{train},&b_r(s_i)\ge m.\end{cases}
$$

Equal scene IDs have equal buckets, so they cannot cross the split. The algorithm does not inspect episode length, frames, timestamps or physical values.

## Visual: grouping beats recording order

| Input position | Episode | Scene | Bucket at seed7 | Partition at threshold5000 |
|---:|---|---|---:|---|
| 0 | ep_a | kitchen | 9538 | train |
| 1 | ep_b | office | 2001 | validation |
| 2 | ep_c | kitchen | 9538 | train |
| 3 | ep_d | warehouse | 925 | validation |

Read rows in input order to construct each output list. The table is the original static trace and text alternative: rows0 and2 share one scene, despite not being adjacent.

## What the fraction means

The nominal threshold fraction is $m/10000$. It is not a promised fraction of episodes: a single large scene can dominate one partition. Even the fraction of scenes is approximate for a finite collection. Group isolation is the invariant, not an exact sample count.

Changing seed or threshold can change the split. Record both and the exact scene metadata alongside evaluation results. Python's process-dependent hash is unsuitable for this cross-process protocol.

## Why this matters on a robot

A held-out recording of the same tabletop may hide failures on unfamiliar lighting and layouts. Scene grouping reduces that particular leakage only when IDs correctly encode shared environments; renaming the same room twice defeats it. It does not isolate robot identities, operators or time periods unless the upstream grouping policy includes them.

## Questions

1. Why must two office episodes move together at threshold2002?
2. Does a threshold5000 ensure half the episodes are in validation?

## Sources and prerequisites

robomimic motivates careful evaluation of offline robot demonstrations. Grouping by supplied scene identity and the exact SHA-256 bucket protocol are original teaching choices, not a split algorithm claimed by the paper. [Primary source](https://arxiv.org/abs/2108.03298), Evaluation and dataset design; scene-grouped hashing is an original teaching protocol. Prerequisites: the component conventions defined in the statement; no Python or mathematics tutorial is assumed.

