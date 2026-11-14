import numpy as np


def fourier_encode(positions,levels):
    if not isinstance(positions,np.ndarray):raise TypeError("Expected position array")
    if positions.dtype!=np.float64 or positions.ndim!=2 or positions.shape[1]!=3 or positions.shape[0]>10000 or not np.isfinite(positions).all() or np.any(np.abs(positions)>1e4):
        raise ValueError("Invalid normalized positions")
    if type(levels) is not int or not 0<=levels<=10:raise ValueError("Invalid frequency count")
    frequencies=(2.**np.arange(levels))*np.pi
    phase=positions[:,None,:]*frequencies[None,:,None]
    return np.concatenate((np.sin(phase),np.cos(phase)),axis=2).reshape(positions.shape[0],6*levels)
