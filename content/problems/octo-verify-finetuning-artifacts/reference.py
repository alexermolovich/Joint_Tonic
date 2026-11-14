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

def verify_finetuning(parameters,artifacts,allowed_prefixes,base_sha256):
    import re,math
    name=lambda x:type(x)==str and len(x)<=80 and re.fullmatch(r'[A-Za-z_][A-Za-z0-9_]*(\.[A-Za-z_][A-Za-z0-9_]*)*',x) is not None
    digest=lambda x:type(x)==str and re.fullmatch(r'[0-9a-f]{64}',x) is not None
    shape=lambda s:type(s)==list and 1<=len(s)<=4 and all(type(v)==int and 1<=v<=10000 for v in s) and math.prod(s)<=1000000000
    if type(parameters)!=list or type(artifacts)!=list or len(parameters)>256 or len(artifacts)>256 or type(allowed_prefixes)!=list or not 1<=len(allowed_prefixes)<=16 or not all(name(x) for x in allowed_prefixes) or len(set(allowed_prefixes))!=len(allowed_prefixes) or not digest(base_sha256):raise ValueError("artifact inputs")
    table={};saved={}
    for p in parameters:
        if type(p)!=dict or set(p)!={'name','shape','trainable'} or not name(p['name']) or not shape(p['shape']) or type(p['trainable'])!=bool or p['name'] in table:raise ValueError("parameter schema")
        table[p['name']]=p
    for a in artifacts:
        if type(a)!=dict or set(a)!={'name','shape','base_sha256'} or not name(a['name']) or not shape(a['shape']) or not digest(a['base_sha256']) or a['name'] in saved or a['name'] not in table or a['shape']!=table[a['name']]['shape']:raise ValueError("artifact schema")
        saved[a['name']]=a
    train={n for n,p in table.items() if p['trainable']};total=sum(math.prod(p['shape']) for p in table.values());count=sum(math.prod(table[n]['shape']) for n in train)
    r={'total_count':total,'trainable_count':count,'frozen_count':total-count,'unexpected_trainable':sorted(n for n in train if not any(n==p or n.startswith(p+'.') for p in allowed_prefixes)),'missing_artifacts':sorted(train-saved.keys()),'frozen_artifacts':sorted(saved.keys()-train),'mismatched_base':sorted(n for n,a in saved.items() if a['base_sha256']!=base_sha256)}
    r['ready']=not any(r[k] for k in ['unexpected_trainable','missing_artifacts','frozen_artifacts','mismatched_base']);return r
