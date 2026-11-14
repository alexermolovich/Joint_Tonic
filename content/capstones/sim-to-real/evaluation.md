# Evaluation and failure analysis

Run checks the two worked examples; Submit also checks independent stage oracles, invalid contracts, boundary conditions, storage preservation, and realistic tensor sizes in the isolated CPU worker.

## Diagnose a failed release

1. Locate the first stage whose evidence violates its contract.
2. Change one input factor and predict which report fields must change.
3. Separate insufficient evidence from measured regression.
4. Record the observed verdict and numerical evidence in workspace Notes.

### Example 1: complete synthetic evidence

Use eight rows, all successes and observed, every latency 5 ms, seed 7, minimum rate 0.5, maximum gap 0.2, and budget 10 ms. Strata are `[0,1,2,3,0,1,2,3]`, counts are all 2, rates/means/worst rates are all 1, p95 is 5 ms, gaps are zero. Wilson intervals are approximately `[0.675592,1]` for each domain; decision is `promote`. The first factor pair is approximately `(0.650038,0.948607)`.

### Example 2: a hidden transfer failure

Set real-domain success False at rows 0 and 4. Real overall rate is 0.75, but bucket-zero real rate is 0 and its sim-real gap is 1. Decision is `hold`, even though the other three buckets all succeed. This failure must appear in the evidence report.

Passing these synthetic checks does not establish real-world accuracy or safety. A real release requires licensed held-out data, target-hardware measurements, and independent robot validation.
