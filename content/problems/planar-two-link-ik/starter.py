import numpy as np


def planar_ik(L1, L2, target) -> dict:
    """Return reachable, angles [q1,q2] or None, and singular.

    Length/target units: meters. Angles: radians about +z.
    Choose q2 in [0,pi], normalize q1 to [-pi,pi).
    """
    # Validate, check the reachable annulus, then solve the declared branch.
    pass
