# Block a Pipeline on Critical Data Anomalies

## Intuition

A validator can report zero critical anomalies because the data was healthy—or because one source was never checked. A gate must inspect both anomaly severity and validation coverage. Keeping warnings separate allows a caller to show useful evidence without quietly promoting it to a critical condition.

## Evidence sets and the decision

Let R be the required-source set and C the checked-source set. Let B contain critical (source,code) pairs and W contain warning pairs after exact deduplication. The missing coverage set is

$$
M=R\setminus C,\qquad
\mathrm{blocked}=(|B|>0)\lor(|M|>0).
$$

All sets contain metadata identifiers, not physical quantities. W is returned for inspection but does not appear in this particular blocking rule. Other organizations may choose another policy; learners implement the one stated here.

Severity conflicts are invalid evidence rather than an invitation to pick a convenient result. If the same source/code is both warning and critical in one snapshot, the caller must resolve the provenance before asking for a deterministic gate.

## Visual: distinguish three states

| Required coverage | Critical anomalies | Warnings | blocked |
|---|---|---|---|
| Complete | None | Any | False |
| Complete | Present | Any | True |
| Incomplete | None or present | Any | True |

This decision table is also the text alternative. In example2, the empty anomaly list says nothing about camera because camera is absent from C. Deduplicating repeated requirements changes neither coverage nor the decision.

## Why this matters on a robot

Skipping a wrist-camera partition can create a seemingly clean training run. Likewise, treating a critical anomaly from an extra checked calibration source as irrelevant discards known evidence. A gate should record all contributing source/model/evaluator versions so its result can be replayed; this function only computes the deterministic decision from an already-associated snapshot.

## Check your understanding

1. Can zero anomalies still produce blocked=True?
2. Does a critical anomaly outside required_sources get ignored?

## Sources and prerequisites

The paper motivates separating validation evidence from downstream pipeline execution. Required-source coverage, severity policy and conflict rules are original teaching choices; a passing data gate is not a robot safety guarantee. [Primary source](https://research.google/pubs/data-validation-for-machine-learning/), Data validation as a pipeline boundary; schema anomaly review. Prerequisites: the component conventions defined in the statement; no Python or mathematics tutorial is assumed.
