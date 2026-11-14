# Worked examples

1. With every Jacobian zero, any supported small bias deltas leave the original rotation, velocity and position unchanged, but return new arrays.
2. Start with identity rotation and zero velocity/position. Let J_R_bg=I, J_v_ba=2I, J_p_ba=0.5I and all other Jacobians zero. Gyro delta `[0.,0.,0.01]` and accel delta `[0.01,0.,0.]` give a local z rotation of `0.01` rad, velocity `[0.02,0.,0.]` m/s and position `[0.005,0.,0.]` meters.
