import numpy as np

def broadcast_sensor_features(sensor, context, present):
    for a in [sensor,context]:
        if not isinstance(a,np.ndarray) or a.dtype!=np.float64 or not np.isfinite(a).all() or (np.abs(a)>1e6).any():raise ValueError('normalized features')
    if sensor.ndim!=3 or context.ndim!=2 or not isinstance(present,np.ndarray) or present.dtype!=np.bool_:raise ValueError('feature ranks/mask')
    b,t,f=sensor.shape
    if not 1<=b<=32 or not 0<=t<=256 or not 1<=f<=64 or context.shape[0]!=b or not 1<=context.shape[1]<=64 or present.shape!=(b,t) or b*t*(f+context.shape[1])>1000000:raise ValueError('episode alignment')
    joined=np.concatenate((sensor,np.broadcast_to(context[:,None,:],(b,t,context.shape[1]))),axis=2)
    return np.where(present[:,:,None],joined,0.)
