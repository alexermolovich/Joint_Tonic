# Compute Per-Embodiment and Transfer Metrics

## Intuition

A single average hides whether a shared policy succeeds only on the embodiment it was trained for. Preserve the training-to-evaluation direction and keep untested combinations visibly unknown.

## Mathematical mechanism

For training embodiment i and test embodiment j, $n_{ij}=\sum_k\mathbf1[t_k=i,e_k=j]$ and $$p_{ij}=\frac{\sum_k\mathbf1[t_k=i,e_k=j]y_k}{n_{ij}}.$$ y is Boolean episode success. Transfer micro-rate divides all successful off-diagonal attempts by all off-diagonal attempts; it weights frequently evaluated pairs more heavily. Empty cells are NaN rather than zero-success evidence.

## Visual computation trace

| Train/test | 0 | 1 |
|---|---|---|
| 0 | 1/1=1 | 1/2=0.5 |
| 1 | no observations | no observations |

The table is the static visual and its text alternative; each row describes a transformation or decision.

## Worked calculation

train_ids=[0,0,0], test_ids=[0,1,1], success=[True,True,False], E=2 returns count=[[1,2],[0,0]], rates=[[1,0.5],[NaN,NaN]], same_embodiment_rate=1 and transfer_rate=0.5.

## Why this matters on a robot

Transposing train and test changes the interpretation of transfer. Treating untested cells as failures conflates missing coverage with negative evidence, while averaging cells equally answers a different question than attempt-weighted performance.

## Physical contract and limits

Rates dimensionless; IDs reference a versioned embodiment registry. Each row is one episode evaluation, not an action timestep; train/test IDs label model-training and deployment embodiment. Original cross-embodiment evaluation aggregation inspired by OXE. A matrix cell measures supplied outcomes and cannot prove transfer causality without controlled baselines.

Source: [primary paper](https://arxiv.org/abs/2310.08864). Prerequisite: understand the observation/action schema supplied in the contract; no additional lesson is required.
