# Solution

Subtract the fixed bias, form each interval rotation vector, and right-multiply its exponential onto the previous orientation. Preserve every intermediate matrix so downstream preintegration can use interval-start rotations. O(N) time and memory.

```python
import numpy as np

def _array(x, ndim, kind="f"):
    if not isinstance(x, np.ndarray) or x.ndim != ndim or x.dtype != {"f":np.dtype("float64"),"i":np.dtype("int64"),"b":np.dtype("bool")}[kind]:
        raise ValueError("Invalid array type, dtype or rank")
    if kind == "f" and (not np.isfinite(x).all() or np.any(np.abs(x)>1e6)):
        raise ValueError("Array values must be finite and bounded")
    return x

def _scalar(x, low, high):
    if type(x) not in (int,float) or not low<=x<=high or not np.isfinite(x):raise ValueError("scalar contract")
    return float(x)

def _skew(v):
    x,y,z=v
    return np.array([[0.,-z,y],[z,0.,-x],[-y,x,0.]])

def _so3(phi):
    theta=float(np.linalg.norm(phi));s=theta*theta;k=_skew(phi)
    if theta<1e-4:a=1-s/6+s*s/120;b=.5-s/24+s*s/720
    else:a=np.sin(theta)/theta;b=(1-np.cos(theta))/s
    return np.eye(3)+a*k+b*(k@k)

def _left_jacobian(phi):
    theta=float(np.linalg.norm(phi));s=theta*theta;k=_skew(phi)
    if theta<1e-4:b=.5-s/24+s*s/720;c=1/6-s/120+s*s/5040
    else:b=(1-np.cos(theta))/s;c=(theta-np.sin(theta))/(s*theta)
    return np.eye(3)+b*k+c*(k@k)

def integrate_imu_rotation(angular_velocity,gyro_bias,durations):
    w=_array(angular_velocity,2);b=_array(gyro_bias,1);dt=_array(durations,1);n=len(w)
    if w.shape[1]!=3 or n>4096 or b.shape!=(3,) or dt.shape!=(n,) or np.any(np.abs(w)>100) or np.any(np.abs(b)>100) or np.any((dt<1e-6)|(dt>1)) or dt.sum()>100:raise ValueError("rotation integration contract")
    rotations=np.empty((n+1,3,3));rotations[0]=np.eye(3)
    for k in range(n):rotations[k+1]=rotations[k]@_so3((w[k]-b)*dt[k])
    return dict(rotations=rotations,elapsed=np.r_[0.,np.cumsum(dt)])
```
