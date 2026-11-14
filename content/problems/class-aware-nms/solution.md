# Solution: greedily filter one remaining index array

Validate all shapes/ranges before sorting. Convert box coordinates and scores to float64 and class IDs to an integer array after checking that their values are integral. Use `np.argsort(-scores, kind='stable')`; since the original order is input index order, this gives the required tie rule.

While candidates remain, append the first original index. Compute its intersection and union with the rest, using masked division so empty boxes have zero IoU. Retain candidates whose class differs or whose IoU is at most the cutoff. Because suppressed candidates are removed from this list immediately, they can never suppress a later detection.

Worst-case work is O(N²): when no boxes overlap, each selection compares against almost every remaining box. Additional working storage is O(N). The task uses bounded N and vectorized comparisons, so no compiled extension is necessary. Large production workloads may use a dedicated kernel, but must preserve the same coordinate and threshold semantics for reproducible outputs.
