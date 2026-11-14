# Author and independent review

Status: reviewed; approved for implementation by `perception_implementation`.

## Proof of success

Check both worked arrays and masks, all-empty shapes, valid zero semantics, noncontiguous storage independence and maximum padded budget.

## Author evidence

Read the paired card and manifest; verified the mechanism or motivation against the primary source. Inputs/examples/diagram are original. Shared structural validator passed all six packages and35 LaTeX expressions. Author independently recomputed all12 worked examples with NumPy/rational arithmetic: padding/masks, exact rate rankings, pooled/macro task rates, rational threshold eligibility, unit conversions and integer remainder allocation. No evaluator or publication claim is made.

## Question answer key

1. Zero is a legitimate value. Only declared length establishes sample existence.

2. Padding can create many additional cells when one long episode determines the common horizon.

## Review risks

Do not conflate this full-episode batching operation with ACT sliding windows, or claim that masking alone prevents hidden-state leakage.


## Independent contract review

Reviewer: `perception_implementation`. Verified both shape/mask examples, real zeros versus padding, all-empty batches, the padded BLD budget and independent storage. Common units/frame/control semantics are explicitly upstream rather than inferred.

No blocking contract findings remain. Reference implementation, independent code review, isolated public/hidden grading and starter negative controls remain publication requirements.
