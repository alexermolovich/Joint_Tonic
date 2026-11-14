# Reference solution

Compute shared dot-product scores, apply two independent stable masked softmax operations, and multiply each weight matrix by the opposite modality's tokens.

Language grounding connects a phrase such as 'red handle' to visible regions. Simply transposing image-to-text probabilities does not yield text-to-image probabilities. Including padded tokens can shift grounding even when the real words are unchanged.

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

def bidirectional_context(image_tokens, text_tokens, image_valid, text_valid):
    array(image_tokens,3);array(text_tokens,3);array(image_valid,2,np.bool_);array(text_valid,2,np.bool_)
    b,p,d=image_tokens.shape;bt,t,dt=text_tokens.shape
    check(1<=b<=8 and bt==b and 1<=p<=128 and 1<=t<=64 and 1<=d<=64 and dt==d and image_valid.shape==(b,p) and text_valid.shape==(b,t))
    scores=image_tokens@text_tokens.transpose(0,2,1)/math.sqrt(d)
    def attention(s,q,k):
        mask=q[:,:,None]&k[:,None,:];masked=np.where(mask,s,-np.inf)
        maximum=np.max(masked,axis=-1,keepdims=True);maximum=np.where(np.isfinite(maximum),maximum,0)
        ex=np.exp(masked-maximum);den=ex.sum(axis=-1,keepdims=True)
        return np.divide(ex,den,out=np.zeros_like(ex),where=den>0)
    iw=attention(scores,image_valid,text_valid);tw=attention(scores.transpose(0,2,1),text_valid,image_valid)
    return dict(image_context=iw@text_tokens,text_context=tw@image_tokens,image_weights=iw,text_weights=tw)
```
