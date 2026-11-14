# Validate a Robot Dataset Datasheet

## Intuition

A datasheet should make missing and explicitly unknown information visible. A complete machine-readable record is a starting point for human review, not a dataset quality score.

## Formal model

Let $F$ be required fields, $K$ supplied keys, and $U$ explicitly unknown values. The missing set is
$$M=F\setminus K.$$
Validation distinguishes absence($M$), present-but-invalid values, and documented unknowns($U$). These are original reporting categories, not a numeric score or schema standardized by the Datasheets paper.

## Worked state and shape trace

```text
Start from the complete datasheet in Example1.
Remove license; set calibration_sha256="unknown"; add extras=1.
Returned issues:
[("calibration_sha256", "unknown"), ("extras", "unexpected"), ("license", "missing")]
These distinguish a documented unknown, an extra field, and missing provenance.
```

The ordered text trace is also the visual alternative; no animation is required.

## Why this matters on a robot

Robotics data cannot be interpreted reliably when embodiment or calibration provenance is missing. A known digest does not prove the calibration was physically correct or that use is permitted.

## Source and scope

Original bounded component inspired by [2018-datasheets-for-datasets](https://arxiv.org/abs/1803.09010). It does not reproduce the full paper or establish hardware safety or data-use authorization.
