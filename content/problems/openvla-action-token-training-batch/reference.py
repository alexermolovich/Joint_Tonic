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

def build_action_token_batch(prompts,actions,pad_id,eos_id,vocab_size):
    v=_scalar(vocab_size,4,1000000,True);pad=_scalar(pad_id,0,v-1,True);eos=_scalar(eos_id,0,v-1,True)
    if pad==eos or type(prompts)!=list or type(actions)!=list or not 1<=len(prompts)<=32 or len(prompts)!=len(actions):raise ValueError("token lists")
    ps=[_array(x,1,"int") for x in prompts];ac=[_array(x,1,"int") for x in actions]
    if any(not 1<=len(x)<=bound or (x<0).any() or (x>=v).any() or (x==pad).any() or (x==eos).any() for xs,bound in [(ps,256),(ac,64)] for x in xs):raise ValueError("source tokens")
    lengths=np.array([len(p)+len(a)+1 for p,a in zip(ps,ac)],dtype=np.int64);n=int(lengths.max());b=len(ps);ids=np.full((b,n),pad,dtype=np.int64);labels=np.full((b,n),-100,dtype=np.int64);mask=np.arange(n)[None,:]<lengths[:,None]
    for i,(p,a) in enumerate(zip(ps,ac)):
        seq=np.r_[p,a,eos];ids[i,:len(seq)]=seq;labels[i,len(p):len(seq)]=seq[len(p):]
    return {'input_ids':ids,'labels':labels,'attention_mask':mask,'lengths':lengths}
