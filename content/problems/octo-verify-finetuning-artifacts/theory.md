# Verify Trainable Parameters and Fine-Tuning Artifacts

## Intuition

A fine-tuning artifact should contain exactly the learned parameter subset and identify the frozen model it extends. Counting trainable entries, checking namespace boundaries and matching base hashes catch different ways a seemingly valid checkpoint can be incomplete.

## Mathematical mechanism

Parameter p with shape $s_p$ contributes $n_p=\prod_k s_{pk}$ scalars. $$N_{train}=\sum_p n_p\mathbf1[p\text{ trainable}],\qquad N_{frozen}=N_{total}-N_{train}.$$ Artifact readiness requires an exact trainable parameter set, authorized namespace boundaries, shape agreement and pinned base identity. Counting trainable weights alone cannot prove a useful adaptation.

## Visual computation trace

| Check | Example | Outcome |
|---|---|---|
| namespace | adapter.up under adapter | allowed |
| namespace | adapterevil.up under adapter | rejected |
| frozen weight in adapter artifact | backbone.weight | report |

The table is the static visual and its text alternative; each row describes a transformation or decision.

## Worked calculation

parameters=[{name:"adapter.up",shape:[2,3],trainable:True}], artifacts=[], allowed_prefixes=["adapter"], base="0"*64 returns total/trainable6, frozen0, missing_artifacts=["adapter.up"], readyFalse.

## Why this matters on a robot

An incorrect interface silently changes which sensor or actuator a feature describes. Preserve masks and schema versions when transferring to another robot.

## Physical contract and limits

Token features and normalized actions are dimensionless; no world-frame transform or physical actuation is performed. Each batch row is a synchronized caller-supplied policy context; group order is explicit. Original deterministic artifact audit motivated by Octo adaptation and reproducibility; no weights are loaded, trained or serialized by this function.

Source: [primary paper](https://arxiv.org/abs/2405.12213). Prerequisite: understand the observation/action schema supplied in the contract; no additional lesson is required.
