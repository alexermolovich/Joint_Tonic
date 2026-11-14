import numpy as np
import math

def check_calibration_gradient(design, parameters, target, analytic, step, tolerance):
    if any(not isinstance(a,np.ndarray) or a.dtype!=np.float64 or not np.isfinite(a).all() or (np.abs(a)>100).any() for a in [design,parameters,target,analytic]):raise ValueError('calibration arrays')
    if design.ndim!=2 or not 1<=design.shape[0]<=64 or not 1<=design.shape[1]<=32 or parameters.shape!=(design.shape[1],) or analytic.shape!=parameters.shape or target.shape!=(design.shape[0],):raise ValueError('design shape')
    if type(step) not in (int,float) or not 1e-6<=step<=1e-2 or not math.isfinite(step) or type(tolerance) not in (int,float) or not 0<=tolerance<=1 or not math.isfinite(tolerance):raise ValueError('step/tolerance')
    def loss(x):return .5*np.sum((design@x-target)**2)
    numeric=np.empty_like(parameters)
    for j in range(len(parameters)):
        plus=parameters.copy();minus=parameters.copy();plus[j]+=step;minus[j]-=step;numeric[j]=(loss(plus)-loss(minus))/(2*step)
    error=np.abs(numeric-analytic)/np.maximum(1,np.maximum(np.abs(numeric),np.abs(analytic)))
    return dict(numeric=numeric,relative_error=error,passed=bool(np.all(error<=tolerance)))
