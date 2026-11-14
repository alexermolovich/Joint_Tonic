## Example 1

Predictions [[1, 3], [4, 99]], targets [0, 2] and mask [[True, True], [True, False]] yield per-state losses [5, 4], total loss 4.5 and gradient [[0.5, 1.5], [2, 0]].

## Example 2

If every view is invalid, total loss is zero, every per-state loss is NaN and all gradient entries are zero.
