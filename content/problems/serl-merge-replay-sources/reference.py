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

def merge_replay(online,demonstration):
    keys={'ids','observations','actions','rewards','next_observations','terminated'}
    def parse(data):
        if type(data) is not dict or set(data)!=keys:raise ValueError("replay schema")
        x={k:_array(data[k],1 if k in ['ids','rewards','terminated'] else 2,'int' if k=='ids' else 'bool' if k=='terminated' else 'real') for k in keys};n=len(x['ids']);d=x['observations'].shape[1];a=x['actions'].shape[1]
        if n>4096 or not 1<=d<=16 or not 1<=a<=16 or (x['ids']<0).any() or len(np.unique(x['ids']))!=n or any(len(v)!=n for v in x.values()) or x['next_observations'].shape!=(n,d):raise ValueError("replay field shape or identity")
        return x
    pools=[parse(online),parse(demonstration)]
    if pools[0]['observations'].shape[1]!=pools[1]['observations'].shape[1] or pools[0]['actions'].shape[1]!=pools[1]['actions'].shape[1]:raise ValueError("source feature schemas differ")
    rows={}
    for source,pool in enumerate(pools):
        for j,identity in enumerate(pool['ids']):
            identity=int(identity)
            if identity in rows:
                previous,index,origin=rows[identity]
                if any(not np.array_equal(pools[previous][key][index],pool[key][j]) for key in keys-{'ids'}):raise ValueError("conflicting immutable transition")
                rows[identity]=(previous,index,origin|(1<<source))
            else:rows[identity]=(source,j,1<<source)
    ids=sorted(rows);count=len(ids);out={key:np.empty((count,)+pools[0][key].shape[1:],dtype=pools[0][key].dtype) for key in keys};origin=np.empty(count,np.int64)
    for pos,identity in enumerate(ids):
        source,index,origin[pos]=rows[identity]
        for key in keys:out[key][pos]=pools[source][key][index]
    return {**out,'origin':origin}
