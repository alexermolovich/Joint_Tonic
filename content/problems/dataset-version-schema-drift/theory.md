# Detect Dataset-Version and Schema Drift

## Intuition

A dataset can keep the same tensor shape while changing units, frames or channel interpretation. Version identity and schema identity are related but separate evidence. Compare both directly rather than assuming a version label guarantees compatibility.

## Compare explicit contracts

For each feature f, define descriptor $D_f=(d_f,s_f,u_f,c_f)$: dtype d, per-sample shape s, unit u and coordinate-frame label c. The changed-field set is

$$
\Delta_f=\{k\in\{\mathrm{dtype},\mathrm{shape},\mathrm{unit},\mathrm{frame}\}:D_f^{\mathrm{expected}}[k]\ne D_f^{\mathrm{observed}}[k]\}.
$$

These are symbolic metadata comparisons, not numeric transformations. Shape dimensions are sample-axis counts; no sample timestamps or episode lengths are compared. Dataset version IDs are opaque strings.

## Visual: equal shape is insufficient

| Field | Expected pose | Observed pose | Report |
|---|---|---|---|
| dtype | float64 | float64 | none |
| shape | (3,) | (3,) | none |
| unit | m | cm | unit |
| frame | base | tool | frame |
| dataset version | v1 | v2 | version |

The original static table is the visual and text alternative. A consumer must decide how each change affects its contract; this detector does not convert it.

## Stable issue granularity

An entirely missing dataset gets one dataset-level issue. Inside a shared dataset, missing fields get feature-level issues, while shared fields get all changed descriptor fields. This prevents a large absent dataset from flooding the output with redundant feature messages.

## Why this matters on a robot

A silent metre-to-centimetre change can scale a target by100 without changing its array shape. A frame change can rotate its meaning while preserving units. A pipeline that keys compatibility only on dimensions can accept both mistakes.

## Questions

1. Should a schema change be ignored when the version string stayed the same?
2. Does a version change alone prove that a consumer must reject the data?

## Sources and prerequisites

Open X-Embodiment motivates preserving heterogeneous data meaning and reporting cross-embodiment results. This bounded deterministic interface is an original teaching decomposition, not the full RT-X model, dataset tooling or experimental protocol. [Primary source](https://arxiv.org/abs/2310.08864), SectionIV data consolidation and SectionV cross-embodiment evaluation. Prerequisites: the component conventions defined in the statement; no Python or mathematics tutorial is assumed.

