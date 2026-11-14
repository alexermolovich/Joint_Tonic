# Reference solution

Zero-pad actions, accumulate the three cross-correlation offsets, construct time/context FiLM values, apply stable SiLU and the linear output head.

Temporal conditioning helps an action sequence reflect current observations. Kernel reversal changes which neighbor influences a command; confusing diffusion level with wall-clock time changes the model input. Predicted noise is not an executable robot command and needs a separate sampler and safety checks.

```python
import numpy as np
import math

def array(x, ndim, dtype=np.float64):
    if not isinstance(x,np.ndarray) or x.dtype != np.dtype(dtype) or x.ndim != ndim or x.size>2000000:
        raise ValueError("Invalid array type, dtype, rank or size")
    if dtype != np.bool_ and (not np.isfinite(x).all() or np.any(np.abs(x.astype(float))>1e6)):
        raise ValueError("Nonfinite or out-of-range data")
    return x

def check(ok):
    if not ok: raise ValueError("Contract violation")

def real(x, low, high):
    check(type(x) in (int,float) and math.isfinite(x) and low<=x<=high)
    return x

def integer(x, low, high):
    check(type(x) is int and low<=x<=high)
    return x

def conditional_denoiser(actions, timesteps, context, kernel, context_weight, time_weight, head, bias):
    for a,n in ((actions,3),(timesteps,1),(context,2),(kernel,3),(context_weight,2),(time_weight,2),(head,2),(bias,1)):
        array(a,n);check(np.all(np.abs(a)<=100))
    b,h,a=actions.shape;c=kernel.shape[2]
    check(1<=b<=8 and 1<=h<=32 and 1<=a<=8 and 1<=c<=16 and timesteps.shape==(b,) and context.shape[0]==b and 1<=context.shape[1]<=16)
    check(kernel.shape==(3,a,c) and context_weight.shape==(context.shape[1],2*c) and time_weight.shape==(2,2*c) and head.shape==(c,a) and bias.shape==(a,) and np.all((timesteps>=0)&(timesteps<=1)))
    padded=np.pad(actions,((0,0),(1,1),(0,0)));conv=np.zeros((b,h,c))
    for k in range(3):conv+=padded[:,k:k+h]@kernel[k]
    time=np.stack((np.sin(np.pi*timesteps),np.cos(np.pi*timesteps)),axis=-1)
    film=context@context_weight+time@time_weight;gamma,beta=np.split(film,2,axis=-1)
    z=(1+gamma[:,None])*conv+beta[:,None];e=np.exp(-np.abs(z));sig=np.where(z>=0,1/(1+e),e/(1+e))
    return (z*sig)@head+bias
```
