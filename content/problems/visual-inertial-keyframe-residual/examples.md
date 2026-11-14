# Worked examples

1. Identity orientations, zero positions/velocities, gravity `[0.,0.,-10.]`, T=0.1 s, delta_velocity `[0.,0.,1.]`, delta_position `[0.,0.,0.05]` and identity delta_rotation give zero IMU residual: gravity and stationary specific-force increments cancel.
2. Gravity zero, identity rotations, zero velocities/increments, positions i=`[0.,0.,0.]`, j=`[1.,0.,0.]`, T=1 s, all standard deviations 1 and visual residual `[[3.,4.]]` give rp=`[1.,0.,0.]` and cost `(1+9+16)/2=13`.
