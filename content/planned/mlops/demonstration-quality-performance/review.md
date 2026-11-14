# Author and independent review

Status: reviewed; approved for implementation by `perception_implementation`.

## Proof of success

Recompute the0.9 pooled versus0.5 macro example and the two-condition example; verify empty output, repeated-trial counting, sorted labels, exact output types and bounds.

## Author evidence

Read the paired card and manifest; verified the mechanism or motivation against the primary source. Inputs/examples/diagram are original. Shared structural validator passed all six packages and35 LaTeX expressions. Author independently recomputed all12 worked examples with NumPy/rational arithmetic: padding/masks, exact rate rankings, pooled/macro task rates, rational threshold eligibility, unit conversions and integer remainder allocation. No evaluator or publication claim is made.

## Question answer key

1. They may represent distinct evaluation episodes with the same labels/outcome; the input contract says each row is one trial.

2. An absent task has no denominator or measured rate. Zero successes with positive trials is measured evidence.

## Review risks

Do not infer quality labels or claim macro averages remove task-coverage confounding; missing task evidence remains missing.


## Independent contract review

Reviewer: `perception_implementation`. Recomputed pooled 0.9 versus macro 0.5 and the separate quality slices. Duplicate tuples count as trials, absent tasks are not invented, and comparisons across unmatched coverage are explicitly limited.

No blocking contract findings remain. Reference implementation, independent code review, isolated public/hidden grading and starter negative controls remain publication requirements.
