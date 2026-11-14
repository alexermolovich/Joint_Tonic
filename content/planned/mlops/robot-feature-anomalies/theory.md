# Detect Missing, Range, Domain, and Shape Anomalies

## Intuition

A malformed feature should produce a useful location and reason. Treating every exception as a failed record hides whether the sensor was missing, the tensor width changed, or a value exceeded its declared range. A fixed priority also prevents many derivative errors from one underlying shape problem.

## Separate schema errors from data anomalies

For record i and feature f, define predicates for presence, array type, shape, dtype, finiteness and value validity. A valid numeric value x must satisfy

$$
\operatorname{shape}(x)=S_f,\qquad
\operatorname{dtype}(x)=\mathrm{float64},\qquad
\forall j:\ x_j\text{ finite and }\ell_f\le x_j\le u_f.
$$

$S_f$ is the per-observation shape; $\ell_f,u_f$ have the feature's physical unit. Categorical values instead satisfy $x_j\in\mathcal D_f$, where $\mathcal D_f$ is the supplied allowed-label set. These two kinds use different validation rules.

The issue is the first violated applicable rule in the documented order. This is a reporting policy, not a statistical score. A bad schema is rejected because no well-defined comparison exists; a bad measurement is usually retained as an anomaly location.

## Visual: priority avoids misleading cascades

| Observed terrain | Expected scalar? | Next meaningful test | Issue |
|---|---|---|---|
| scalar snow | Yes | Membership in dry/wet | domain |
| vector [snow] | No | Stop at shape | shape |
| absent optional field | Not applicable | No requirement | None |

This table is the static validation pipeline and text alternative. In the numeric example, [0,2] has the correct shape and dtype, but2 lies outside [-1,1]. The empty record instead produces missing, not range.

## Why this matters on a robot

A camera-mode change can alter feature dimensions, and a logging fallback can produce a string where a numeric sensor value was expected. Detailed issue locations help trace those events to a collection or transform version. A value can still pass every schema check while using the wrong physical frame; that semantic contract must be enforced upstream.

## Check your understanding

1. Why not emit domain as well as shape for [snow]?
2. Does a range pass prove the sensor reading is physically correct?

## Sources and prerequisites

The source motivates schema validation and located anomalies. This small numeric/categorical schema is original and complements the existing full episode validator; it does not infer a schema, convert physical units or implement every production validation rule. [Primary source](https://research.google/pubs/data-validation-for-machine-learning/), Section3: schema-based validation and actionable anomalies. Prerequisites: the component conventions defined in the statement; no Python or mathematics tutorial is assumed.
