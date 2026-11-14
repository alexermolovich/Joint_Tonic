# Worked examples

1. One sample has zero rotation and force, duration 1 second, gyro variances [1,1,1] and accelerometer variances [4,4,4]. Final orientation-error variances are 1, velocity variances 4, position variances 1, and matching velocity/position cross-covariances 2.
2. Empty sample arrays return covariance shape (1,9,9) containing zeros and final rotation equal to identity.
