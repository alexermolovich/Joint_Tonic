import numpy as np

# Inclusive FR3 model limits, in radians, ordered fr3_joint1..fr3_joint7.
LOWER = np.array([-2.9007, -1.8361, -2.9007, -3.0770, -2.8763, 0.4398, -3.0508])
UPPER = np.array([2.9007, 1.8361, 2.9007, -0.1169, 2.8763, 4.6216, 3.0508])


def interpolate_fr3_joints(q_start, q_goal, num_steps):
    """Return independent float64 waypoints (num_steps, 7), including both endpoints.

    Inputs are seven joint angles in radians. Raise ValueError for invalid inputs.
    """
    # Validate inputs, then interpolate each joint using the same path fraction.
    pass
