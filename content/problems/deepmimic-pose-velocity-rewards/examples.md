## Example 1

Identical identity rotations and angular velocities yield pose reward [1], velocity reward [1] and angle_error [[0]] for one state and joint.

## Example 2

One joint with a 180-degree mismatch yields angle error pi and pose reward exp(-2*pi**2). A velocity difference [1, 0, 0] rad/s yields exp(-0.1). Negating a quaternion alone causes zero orientation error.
