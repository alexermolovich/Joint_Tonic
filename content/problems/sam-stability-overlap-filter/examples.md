# Worked examples

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

