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

def version_dataset_manifest(datasets,schema_version):
    import re,json,hashlib
    if type(datasets)!=list or len(datasets)>128 or type(schema_version)!=int or not 1<=schema_version<=1000:raise ValueError("invalid manifest")
    keys={'dataset_id','version','embodiment','content_sha256','calibration_sha256'};seen=set();records=[]
    for row in datasets:
        if type(row)!=dict or set(row)!=keys or any(type(v)!=str for v in row.values()):raise ValueError("invalid record")
        if any(re.fullmatch(r'[A-Za-z][A-Za-z0-9_-]{0,31}',row[k]) is None for k in ['dataset_id','embodiment']):raise ValueError("invalid identity")
        if re.fullmatch(r'(0|[1-9][0-9]{0,3})\.(0|[1-9][0-9]{0,3})\.(0|[1-9][0-9]{0,3})',row['version']) is None:raise ValueError("invalid version")
        if any(re.fullmatch(r'[0-9a-f]{64}',row[k]) is None for k in ['content_sha256','calibration_sha256']) or row['dataset_id'] in seen:raise ValueError("invalid hash or duplicate dataset")
        seen.add(row['dataset_id']);records.append(dict(row))
    payload={'schema_version':schema_version,'datasets':sorted(records,key=lambda r:r['dataset_id'])};text=json.dumps(payload,sort_keys=True,separators=(',',':'),ensure_ascii=True)
    return {'canonical_json':text,'sha256':hashlib.sha256(text.encode('utf-8')).hexdigest()}
