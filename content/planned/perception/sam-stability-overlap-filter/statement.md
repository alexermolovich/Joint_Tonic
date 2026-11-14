# Filter Automatic Masks by Stability and Overlap

Draft contract — no published evaluator yet.

Implement filter_stable_masks(logits, quality, threshold, offset, stability_threshold, overlap_threshold).

logits is a finite NumPy float64 array (N,H,W), 0<=N<=128, 1<=H,W<=512, at most 1,000,000 entries, with absolute values <=1e6. quality is finite float64 (N,) with absolute values <=1e6; it is a ranking score and need not lie in [0,1]. Arrays may be noncontiguous.

The four scalar parameters are built-in int/float excluding bool. threshold is in [-1000,1000], offset in (0,1000], and stability_threshold and overlap_threshold in [0,1]. All are finite.

For candidate i, form three masks with strict > comparisons: base = logits[i]>threshold, high = logits[i]>threshold+offset, and low = logits[i]>threshold-offset. Stability is count(high)/count(low), or 0 when low is empty. Retain candidates only if the base mask is nonempty and stability>=stability_threshold.

Process eligible candidates in descending quality, breaking equal quality by smaller original candidate index. Greedily keep a candidate unless its binary base-mask intersection-over-union with ANY already kept mask is strictly greater than overlap_threshold. At equality it is kept. Return a new one-dimensional NumPy int64 array of original indices in processing order. Empty input or no eligible masks returns shape (0,).

All candidate masks refer to the same preprocessed image pixel grid; mask areas count pixels, and all scores are dimensionless. Preserve inputs. Non-array logits/quality raises TypeError; all other contract violations raise ValueError. No prompting, quality-head model, coordinate resizing, GPU, or gradient API is included.

This teaching variant suppresses by binary-mask IoU. The original SAM automatic generator uses box-based NMS stages; this exercise does not claim identical automatic-mask-generator output.

## Example 1: stability before suppression

~~~python
logits = np.array([[[2.,2.,-2.]], [[2.,2.,-2.]], [[0.2,2.,-2.]]])
quality = np.array([0.6,0.9,1.0])
filter_stable_masks(logits,quality,0.,1.,0.75,0.5)
# array([1], dtype=int64)
~~~

Stabilities are 1, 1, and 1/2. Candidate 2 fails before ranking; candidate 1 wins the identical-mask pair despite its larger original index.

## Example 2: overlap equality and an empty mask

~~~python
logits = np.array([[[2.,-2.]], [[2.,2.]], [[-2.,-2.]]])
quality = np.array([1.,1.,4.])
filter_stable_masks(logits,quality,0.,1.,0.,0.5)
# array([0,1], dtype=int64)
~~~

The empty candidate 2 is removed even when the stability threshold is zero. Equal quality visits 0 before 1; their mask IoU is exactly 1/2, so the strict suppression rule keeps both.

