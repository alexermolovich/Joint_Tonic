# Evaluation and failure analysis

Run checks the two worked examples; Submit also checks independent stage oracles, invalid contracts, boundary conditions, storage preservation, and realistic tensor sizes in the isolated CPU worker.

## Diagnose a failed release

1. Locate the first stage whose evidence violates its contract.
2. Change one input factor and predict which report fields must change.
3. Separate insufficient evidence from measured regression.
4. Record the observed verdict and numerical evidence in workspace Notes.

### Example 1: fit then evaluate

Use observations `[[[1.],[1.]]]`, targets `[[[0.5],[0.5]]]`, validity `[[True,True]]`, training mask `[[True,False]]`, embodiment/task `[0]`, bounds `[[-1.]]` to `[[1.]]`, base `[[0.]]`, projection `[[1.]]`, adapter `[[0.]]`, learning rate `0.5`, latency `[[100.,5.]]`, max MSE `0.01`, and budget `10`. The updated adapter is `[[0.5]]`; tokens are `[[[12],[12]]]`, actions `[[[0.5625],[0.5625]]]` radians, represented slice MSE is `0.00390625`, other task slices are NaN, held-out p95 is 5 ms, and decision is `promote`. The slow training-slot duration is excluded.

### Example 2: held-out latency failure

Change held-out latency to 20 ms. The adapter, action tokens, and errors stay identical, but p95 becomes 20 ms and decision becomes `hold`. Training success cannot override serving evidence.

Passing these synthetic checks does not establish real-world accuracy or safety. A real release requires licensed held-out data, target-hardware measurements, and independent robot validation.
