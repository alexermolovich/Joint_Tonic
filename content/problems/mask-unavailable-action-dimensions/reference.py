import numpy as np

def mask_action_dimensions(actions, available):
    if not isinstance(actions,np.ndarray) or not isinstance(available,np.ndarray):
        raise ValueError("arrays required")
    if actions.dtype!=np.float64 or actions.ndim!=2 or available.dtype!=np.bool_ or available.shape!=actions.shape:
        raise ValueError("float64 actions and matching Boolean availability required")
    if not 0<=actions.shape[0]<=1024 or not 1<=actions.shape[1]<=128:
        raise ValueError("shape bounds")
    selected=actions[available]
    if not np.isfinite(selected).all() or (np.abs(selected)>1e6).any():
        raise ValueError("invalid available action")
    return np.where(available,actions,0.)
