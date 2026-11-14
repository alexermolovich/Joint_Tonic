import numpy as np

def _array(value, ndim=None, kind="real"):
    try: a=np.asarray(value)
    except (ValueError,TypeError,OverflowError) as e: raise ValueError("invalid array") from e
    if ndim is not None and a.ndim!=ndim: raise ValueError("invalid rank")
    if a.size>1000000: raise ValueError("array too large")
    if kind=="bool":
        if a.dtype.kind!='b': raise ValueError("boolean array required")
        return a.copy()
    if kind=="int":
        if a.dtype.kind not in 'iu': raise ValueError("integer array required")
    elif a.dtype.kind not in 'iuf': raise ValueError("real numeric array required")
    if not np.isfinite(a).all() or (np.abs(a.astype(np.float64))>1e6).any(): raise ValueError("invalid numeric values")
    return a.astype(np.int64 if kind=="int" else np.float64)

def _scalar(x,low=0,high=1e6,integer=False):
    if isinstance(x,(bool,np.bool_)) or not isinstance(x,(int,float,np.integer,np.floating)): raise ValueError("numeric scalar required")
    if integer and not isinstance(x,(int,np.integer)): raise ValueError("integer scalar required")
    if not low<=x<=high or not np.isfinite(x): raise ValueError("scalar outside bounds")
    return int(x) if integer else float(x)

def balanced_latent_loss(posterior_logits,prior_logits,prediction_loss,valid):
    ql=_array(posterior_logits,3);pl=_array(prior_logits,3);pred=_array(prediction_loss,1);m=_array(valid,1,"bool");b,g,c=ql.shape
    if not 1<=b<=128 or not 1<=g<=32 or not 2<=c<=32 or pl.shape!=ql.shape or pred.shape!=(b,) or m.shape!=(b,) or (np.abs(ql)>50).any() or (np.abs(pl)>50).any() or (pred<0).any():raise ValueError("latent loss contract")
    def softmax(x):
        e=np.exp(x-x.max(axis=-1,keepdims=True));return e/e.sum(axis=-1,keepdims=True)
    sq=softmax(ql);sp=softmax(pl);q=.99*sq+.01/c;p=.99*sp+.01/c;logratio=np.log(q)-np.log(p);kl=np.sum(q*logratio,axis=(1,2));n=int(m.sum());active=m&(kl>1)
    up=-q/p;uq=logratio+1;pg=.99*sp*(up-(sp*up).sum(axis=-1,keepdims=True));qg=.99*sq*(uq-(sq*uq).sum(axis=-1,keepdims=True))
    return {'kl':np.where(m,kl,np.nan),'loss':float(np.mean(pred[m]+1.1*np.maximum(1,kl[m]))) if n else 0.,'prior_gradient':np.where(active[:,None,None],pg/max(n,1),0.),'posterior_gradient':np.where(active[:,None,None],.1*qg/max(n,1),0.),'prediction_gradient':m.astype(float)/max(n,1)}
