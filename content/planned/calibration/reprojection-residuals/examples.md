# Worked inputs and expected outcomes

## Example 1: one measured landmark

`K=[[100,0,50],[0,100,40],[0,0,1]]`, point `[[0.2,0,2]]`, observation `[[62,37]]`.

Prediction: `[[60,40]]`. Expected residual: `[[2,-3]]`; valid: `[True]`; RMSE: `sqrt(13) = 3.605551275...` pixels.

## Example 2: average point error, not coordinate error

Use the same K, points `[[0,0,2],[0.2,0.2,2]]`, observations `[[51,40],[60,52]]`.

Predictions: `[[50,40],[60,50]]`. Expected residuals: `[[1,0],[0,2]]`; valid: `[True,True]`; RMSE: `sqrt((1+4)/2) = 1.581138830...` pixels.

If every point instead has nonpositive depth, residuals are NaN, all validity entries are false, and expected RMSE is `None`.
