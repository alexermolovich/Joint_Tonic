# Evaluation and failure analysis

Run checks the two worked examples; Submit also checks independent stage oracles, invalid contracts, boundary conditions, storage preservation, and realistic tensor sizes in the isolated CPU worker.

## Diagnose a failed release

1. Locate the first stage whose evidence violates its contract.
2. Change one input factor and predict which report fields must change.
3. Separate insufficient evidence from measured regression.
4. Record the observed verdict and numerical evidence in workspace Notes.

### Example 1: reuse and select

Use latency `[[4.,5.],[2.,3.]]`, quality `[0.9,0.8]`, drift `[0.1,0.1]`, sizes `[[8,4],[4,4]]`, intervals `[[0,1],[1,2]]`, model bytes `[b'a',b'b']`, preprocessing `rgb-0-1`, key `b'k'*32`, minimum quality 0.8, budget 10 ms, memory budget 8 bytes, max drift 0.2, inactive. Both models reuse buffer zero: IDs `[[0,0],[0,0]]`, allocated bytes `[8,4]`, p95 `[5.,3.]`. Higher-quality candidate 0 is selected and promoted. Its manifest records candidate 0, 8 allocated bytes, SHA256 of `b'a'`, preprocessing, and schema 1.

### Example 2: drift rollback

Change candidate 0 drift to 0.3 and active to True. Candidate 0 and its manifest/signature stay the same, but decision is `rollback`. Candidate 1 is not silently substituted after the selection; the failed release evidence is retained.

Passing these synthetic checks does not establish real-world accuracy or safety. A real release requires licensed held-out data, target-hardware measurements, and independent robot validation.
