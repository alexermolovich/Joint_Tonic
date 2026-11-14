import numpy as np

def select_safe_ik_candidate(lengths, candidates, joint_limits, obstacles, target, margin):
    """Reject planar IK candidates violating joint limits or link-obstacle clearance, then rank the survivors."""
    raise NotImplementedError
