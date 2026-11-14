import numpy as np


def warp_previous_bev(previous,previous_from_current,resolution,origin):
    if any(not isinstance(x,np.ndarray) for x in (previous,previous_from_current,origin)):
        raise TypeError("feature grid transform and origin must be arrays")
    if previous.dtype!=np.float64 or previous.ndim!=3:
        raise ValueError("float64 HWC feature grid required")
    height,width,channels=previous.shape
    if not 1<=height<=256 or not 1<=width<=256 or not 1<=channels<=64 or previous.size>1000000:
        raise ValueError("grid bounds")
    if previous_from_current.dtype!=np.float64 or previous_from_current.shape!=(3,3) or origin.dtype!=np.float64 or origin.shape!=(2,):
        raise ValueError("transform or origin shape/dtype")
    for values in (previous,previous_from_current,origin):
        if not np.isfinite(values).all() or (np.abs(values)>1e6).any():
            raise ValueError("finite bounded input required")
    if type(resolution) not in (int,float) or not 1e-3<=resolution<=1e3:
        raise ValueError("metric resolution")
    rotation=previous_from_current[:2,:2]
    if not np.allclose(previous_from_current[2],[0,0,1],rtol=0,atol=1e-7) or not np.allclose(rotation.T@rotation,np.eye(2),rtol=0,atol=1e-7) or not np.isclose(np.linalg.det(rotation),1.,rtol=0,atol=1e-7):
        raise ValueError("proper planar rigid transform required")
    row,column=np.indices((height,width),dtype=np.float64)
    cell_centers=np.stack((column+.5,row+.5),axis=-1)
    # Algebraic cancellation avoids subtracting large origins after metric lookup.
    shift=((rotation-np.eye(2))@origin+previous_from_current[:2,2])/resolution
    coordinates=cell_centers@rotation.T+shift-.5
    u,v=coordinates[...,0],coordinates[...,1]
    left=np.floor(u).astype(np.int64);top=np.floor(v).astype(np.int64)
    a=u-left;b=v-top
    result=np.zeros_like(previous)
    for dx,dy,weight in ((0,0,(1-a)*(1-b)),(1,0,a*(1-b)),(0,1,(1-a)*b),(1,1,a*b)):
        x=left+dx;y=top+dy
        valid=(x>=0)&(x<width)&(y>=0)&(y<height)
        result[valid]+=previous[y[valid],x[valid]]*weight[valid,None]
    return result

