# Data contracts include physics

## Intuition

A model can train successfully on corrupted data. A missing camera, a degree/radian mismatch or duplicate timestamps may not crash the tensor library. A schema turns these assumptions into explicit checks before examples enter the training pipeline.

## Structural and physical invariants

An episode has T timestamps and every supplied signal has T rows. A row's shape is independent of the leading time axis. For joint positions, shape [7] means seven joint channels at every timestamp. Metadata distinguishes radians from meters and robot-frame from camera-frame measurements.

Timestamp order is a simple invariant:

$$
t_{i+1}>t_i,\qquad t_i\in\mathbb R,\quad |t_i|<\infty.
$$

This exercise checks adjacent valid timestamp pairs. It reports nonfinite timestamps separately; it does not bridge over them to invent a longer-range comparison.

Let m be the number of None rows in a signal with T>0:

$$
r_{\text{missing}}=\frac{m}{T}.
$$

Report an anomaly only when r_missing exceeds its configured maximum. A limit of 0 rejects any missing row; a limit of 0.25 permits one missing row in four.

## Visual lesson

The schema visual lays modalities on parallel timeline lanes. Red markers identify repeated timestamps, missing rows and invalid ranges; selecting one highlights its precise schema path. A metadata panel shows the expected and supplied unit/frame strings. A sortable issue table exposes all the same evidence without requiring color or pointer interaction.

## Worked example

For timestamps [0,0.1,0.2,0.3] and values [[0,1],None,[2,1],[0,0]], one of four rows is missing. At a 0.25 threshold, no missing-fraction issue is emitted. A threshold of 0.2 emits one signal-level issue. The validator does not manufacture a replacement sample or alter the training data.

## Why this matters on a robot

Training and deployment must agree on sensor schemas. A well-shaped observation in degrees can be numerically plausible where radians are expected. An exact metadata check catches the contract mismatch but cannot infer the true unit from numbers alone.

Version schemas alongside dataset shards, preprocessing code and checkpoints. A pipeline should block critical anomalies and retain issue paths so the collector can trace them back to an episode.

## Failure modes and scope

Reporting every derived error from one malformed row creates noisy diagnostics. This validator uses a hierarchy: shape before dtype, then finiteness before range. Stable output order makes reports reproducible and easy to compare.

The exercise takes inspiration from [Data Validation for ML](https://research.google/pubs/data-validation-for-machine-learning/) and heterogeneous robot data in [Open X-Embodiment](https://arxiv.org/abs/2310.08864). Its schema and fixtures are original and deliberately small.
