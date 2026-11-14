# Progressive hints

## Hint 1

Keep the residual in the measured coordinate: subtract the prediction from the sensor reading.

## Hint 2

Use variance, not standard deviation, when calculating the relative confidence. Gain has no physical unit.

## Hint 3

Compute the corrected mean and Joseph variance separately. Check the limits: a zero-variance prior stays fixed; a very noisy measurement has little influence.

