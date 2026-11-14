import numpy as np

def calibration_sensitivity(baseline, plus, minus, delta, scales):
    arrays=[baseline,plus,minus,delta,scales]
    if any(not isinstance(x,np.ndarray) or x.dtype!=np.float64 or not np.isfinite(x).all() or (np.abs(x)>1e6).any() for x in arrays):raise ValueError('numeric arrays')
    if baseline.ndim!=1 or not 1<=len(baseline)<=64 or plus.ndim!=2 or not 1<=len(plus)<=64 or plus.shape[1]!=len(baseline) or minus.shape!=plus.shape or delta.shape!=(len(plus),) or scales.shape!=delta.shape or (delta<1e-6).any() or (scales<1e-6).any():raise ValueError('perturbation shape/scale')
    slope=(plus-minus)/(2*delta[:,None]);curvature=(plus-2*baseline[None,:]+minus)/(delta[:,None]**2);scaled=np.abs(slope)*scales[:,None]
    ranking=np.lexsort((np.arange(len(plus)),-scaled.max(axis=1))).astype(np.int64)
    return dict(slope=slope,curvature=curvature,scaled_sensitivity=scaled,ranking=ranking)
