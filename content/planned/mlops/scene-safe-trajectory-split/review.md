# Author and independent review

Status: reviewed; approved for implementation by `perception_implementation`.

## Proof of success

Independently recompute the three SHA-256 buckets; compare a grouped fixture, strict threshold boundary, empty inputs and10000 boundary; verify every episode appears once and each scene belongs to only one partition.

## Author evidence

Read the paired card and manifest; verified the mechanism or motivation against the primary source. Inputs/examples/diagram are original. Shared structural validator passed all six packages and29 LaTeX expressions. Author independently recomputed all12 worked outputs, including NumPy extrema, category-frequency differences, anomaly priorities, integer timestamp boundaries, coverage decisions and exact SHA-256 bucket values. No evaluator or publication claim is made.

## Question answer key

1. The split function depends only on scene, seed and threshold, so their shared bucket2001 yields the same decision.

2. No; finite scene counts and unequal episodes per scene prevent an exact episode ratio.

## Review risks

Do not claim that the paper defines this exact hash protocol. Do not mistake reproducible grouping for complete leakage prevention or safety validation.


## Independent contract review

Reviewer: `perception_implementation`. Independently computed SHA-256 buckets with Node crypto: seed 7 yields kitchen 9538, office 2001 and warehouse 925. The strict 2001 threshold example, NUL separator, unsigned big-endian prefix, stable ordering and scene grouping all match. No exact partition-size claim is made.

Read the corresponding paper cards and checked the primary Data Validation for Machine Learning paper / robomimic source as applicable. The original robotics teaching scope is distinct from a full system reproduction. No blocking contract findings remain. Implementation, independent code review, and actual isolated Run/Submit are still required before publication.
