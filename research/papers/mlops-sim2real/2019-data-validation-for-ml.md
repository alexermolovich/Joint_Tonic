---
schema_version: 1
paper_id: "2019-data-validation-for-ml"
title: "Data Validation for Machine Learning"
authors:
  - "Eric Breck"
  - "Marty Zinkevich"
  - "Neoklis Polyzotis"
  - "Steven Whang"
  - "Sudip Roy"
year: 2019
venue_or_status: "SysML 2019"
primary_url: "https://research.google/pubs/data-validation-for-machine-learning/"
pdf_url: "https://mlsys.org/Conferences/2019/doc/2019/167.pdf"
local_pdf: "./2019-data-validation-for-ml.pdf"
sha256: "4c26718460681e3cd8a2be65308f85352af1be46aef84cf749903f9387381f53"
bytes: 435587
pages: 14
topics:
  - "data-quality"
  - "schema-inference"
  - "anomaly-detection"
  - "training-serving-skew"
  - "monitoring"
modalities:
  - "tabular-features"
  - "distributions"
  - "schemas"
  - "robot-episode-metadata"
track_role: "core"
open_access_status: "open-access-proceedings"
redistribution_note: "Research copy only; verify the source license before redistribution."
---

## Agent brief

Implement a small schema-driven validator for robot episodes and online observations. Favor actionable anomalies over generic drift scores.

## Contribution

The system infers and maintains feature schemas, computes scalable summary statistics, detects anomalies, and compares training with serving data. It frames data as a versioned production asset.

## Prerequisite concepts

- Descriptive statistics and quantiles
- Categorical domains and missing values
- Probability distributions and divergence measures
- Dataset versioning

## Essential theory

For a numeric or categorical feature, one symmetric drift measure for a teaching implementation is Jensen-Shannon divergence. Given smoothed histograms \(P\) and \(Q\), with \(M=(P+Q)/2\),

$$
\operatorname{JS}(P,Q)=\tfrac12\operatorname{KL}(P\Vert M)+\tfrac12\operatorname{KL}(Q\Vert M).
$$

This metric complements, rather than replaces, explicit schema checks such as type, presence, range, and domain membership.

## Method map

| Component | Input | Output | Core invariant | Good exercise boundary |
| --- | --- | --- | --- | --- |
| Statistics generator | Versioned data batch | Presence, range, quantile, and category summaries | Every statistic identifies its data version and slice | Summarize one feature family |
| Schema validator | Schema plus examples/batch summaries | Located actionable anomalies | Every anomaly cites a violated constraint | Implement type, range, or domain checks |
| Skew comparator | Reference and serving summaries | Per-feature drift metrics and alerts | Both distributions use compatible bins and units | Implement one smoothed divergence metric |

- Batch statistics generation
- Schema inference and explicit constraints
- Example and aggregate anomaly detection
- Schema evolution suggestions
- Training-serving skew and drift comparison
- Actionable diagnostics

## Data and evaluation

Create robot-episode records with images represented by metadata plus proprioception and actions. Inject missing sensors, unit changes, out-of-range joints, novel categorical values, and distribution shifts. Measure exact anomaly recovery and false alerts.

## Limitations and failure modes

Schema checks cannot determine whether behavior is semantically safe or labels are correct. Distribution thresholds can be noisy and require domain-aware slices and update policies.

## Implementation decomposition

1. Compute per-feature presence, type, range, quantiles, and category counts.
2. Infer a conservative schema from a reference split.
3. Validate examples and aggregate batches against the schema.
4. Compare training and serving summaries.
5. Generate evidence and safe schema-change suggestions.

## Problem blueprints

| Title | Type | Difficulty | Inputs | Outputs | Grading |
| --- | --- | --- | --- | --- | --- |
| Infer an Episode Schema | Data engineering | Medium | JSON-like episodes | Typed constraints and presence rates | Correct inference, deterministic domains, null handling |
| Detect Sensor Anomalies | Validation | Medium | Schema and batch | Located anomalies with reasons | Exact issue coverage and no duplicate reports |
| Training-Serving Skew | Statistics | Hard | Reference/current summaries | Per-feature skew metrics and alerts | Correct metrics, smoothing, threshold edge cases |

## Visual teaching plan

- Side-by-side feature histograms with a live JS-divergence threshold.
- Schema tree that highlights missing, novel, and out-of-range values in an incoming episode.
- Training-versus-serving matrix across robot, site, sensor, and firmware slices.
- Data-lifecycle timeline showing when a schema update is safe versus when data should be blocked.

## MLOps and deployment extensions

Validate coordinate frames, units, camera intrinsics, timestamps, control rates, joint limits, and action/observation alignment. Slice drift by robot serial number, site, lighting, payload, firmware, and teleoperator.

## Canonical sources

- [Google Research publication page](https://research.google/pubs/data-validation-for-machine-learning/)
- [Official MLSys PDF](https://mlsys.org/Conferences/2019/doc/2019/167.pdf)

