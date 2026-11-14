import numpy as np


def render_rays(weights,colors,depths,background,background_rgb):
    for x in (weights,colors,depths,background,background_rgb):
        if not isinstance(x,np.ndarray):raise TypeError("Expected NumPy arrays")
        if x.dtype!=np.float64 or not np.isfinite(x).all():raise ValueError("Expected finite float64 data")
    if weights.ndim!=2 or not all(1<=v<=1024 for v in weights.shape):raise ValueError("Invalid ray dimensions")
    r,s=weights.shape
    if colors.shape!=(r,s,3) or depths.shape!=(r,s) or background.shape!=(r,) or background_rgb.shape!=(3,) or colors.size>1_000_000:
        raise ValueError("Mismatched ray arrays")
    for x in (weights,colors,background,background_rgb):
        if np.any(x<0) or np.any(x>1):raise ValueError("Values outside [0,1]")
    if np.any(depths<0) or np.any(depths>1e6) or np.any(np.diff(depths,axis=1)<0):raise ValueError("Invalid metric depths")
    mass=weights.sum(axis=1)
    if not np.allclose(mass+background,1,atol=1e-6,rtol=0):raise ValueError("Compositing mass must sum to one")
    rgb=(weights[:,:,None]*colors).sum(axis=1)+background[:,None]*background_rgb
    valid=mass>1e-8
    depth=np.full(r,np.nan,dtype=np.float64)
    depth[valid]=(weights[valid]*depths[valid]).sum(axis=1)/mass[valid]
    return rgb,depth,valid
