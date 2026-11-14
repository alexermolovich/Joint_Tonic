# Solution

Integrate one closed-form arc per command. O(T) time and O(T) output storage.

```python
import numpy as np

def _real(value):
    try:
        a = np.asarray(value)
        if a.dtype.kind not in "iuf": raise ValueError("Expected real numeric data")
        a = a.astype(np.float64)
    except (TypeError, OverflowError) as exc:
        raise ValueError("Expected real numeric data") from exc
    if not np.isfinite(a).all() or np.any(np.abs(a)>1e9):
        raise ValueError("Values must be finite with magnitude <=1e9")
    return a

def differential_drive_rollout(initial_pose, wheel_rates, dt, radius, track):
    pose,rates,dt,r,b=map(_real,(initial_pose,wheel_rates,dt,radius,track))
    if pose.shape!=(3,) or rates.ndim!=2 or rates.shape[1]!=2 or any(a.ndim!=0 or a<1e-9 for a in (dt,r,b)): raise ValueError("Invalid drive contract")
    pose=pose.copy(); pose[2]=(pose[2]+np.pi)%(2*np.pi)-np.pi; out=np.empty((len(rates)+1,3)); out[0]=pose
    for i,(left,right) in enumerate(rates):
        v=r*(left+right)/2; omega=r*(right-left)/b; half=omega*dt/2
        distance=v*dt*np.sinc(half/np.pi); angle=pose[2]+half
        pose=pose+np.array([distance*np.cos(angle),distance*np.sin(angle),2*half])
        pose[2]=(pose[2]+np.pi)%(2*np.pi)-np.pi; out[i+1]=pose
    return out
```
