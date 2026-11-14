# Worked examples

1. Identity extrinsic, IMU world poses at x=0 and x=2, measured lidar relative translation x=1, and all standard deviations 1 give translation residual [1,0,0], zero rotation residual, and cost 0.5.
2. The IMU rotates 90 degrees about z at a fixed origin. A lidar mounted one meter along IMU x has relative rotation Rz90 and relative translation [-1,1,0]. Supplying exactly that measurement gives zero cost.
