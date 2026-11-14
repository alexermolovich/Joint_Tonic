# Report Metrics by Source and Embodiment

## Intuition

A high average success rate can hide a weak source or robot embodiment. Keep a source-by-embodiment table, distinguish missing evidence from failure, and compute latency percentiles inside each cell.

## Mathematical mechanism

For source s and target embodiment e, cell $I_{se}=\{i:S_i=s,E_i=e\}$ has count $n_{se}$. $$r_{se}=\frac{\sum_{i\in I_{se}}y_i}{n_{se}},\qquad r_{all}=\frac{\sum_i y_i}{N}.$$ A cell with no trials is unknown, not zero success. The worst observed rate uses only populated cells; it cannot certify unobserved embodiments. Latency percentiles are computed after slicing, not averaged across cells.

## Visual computation trace

| Source, embodiment | successes | count | rate |
|---|---|---|---|
| real,0 | 1 | 2 | 0.5 |
| synthetic,1 | 1 | 1 | 1.0 |
| video,0 | none | 0 | NaN |

The table is the static visual and its text alternative; each row describes a transformation or decision.

## Worked calculation

sources=[0,0,2],embodiments=[0,0,1],success=[True,False,True],latency=[2,4,3],E2 gives count[[2,0],[0,0],[0,1]], populated rates .5 and1, populated p95 4 and3,overall2/3,worst.5.

## Why this matters on a robot

Aggregating incompatible robot channels or source types can hide a failing embodiment. Keep provenance, masks and per-slice results visible throughout training and evaluation.

## Physical contract and limits

Latency milliseconds; source/embodiment labels are fixed evaluation schema indices; success is binary closed-loop trial outcome. Observations are synchronized by the caller; flow time is dimensionless and differs from physical sampling time. Original bounded interface/diagnostic inspired by GR00T N1, not a full model reproduction or real-hardware safety certification.

Source: [primary paper](https://arxiv.org/abs/2503.14734). Prerequisite: understand the observation/action schema supplied in the contract; no additional lesson is required.
