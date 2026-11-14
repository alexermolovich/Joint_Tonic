import numpy as np

def scenario_coverage(bucket_ids, success, bucket_count):
    if type(bucket_count) is not int or not 1<=bucket_count<=256:raise ValueError('bucket count')
    if not isinstance(bucket_ids,np.ndarray) or bucket_ids.dtype!=np.int64 or bucket_ids.ndim!=1 or len(bucket_ids)>100000 or (bucket_ids<0).any() or (bucket_ids>=bucket_count).any():raise ValueError('bucket IDs')
    if not isinstance(success,np.ndarray) or success.dtype!=np.bool_ or success.shape!=bucket_ids.shape:raise ValueError('success mask')
    counts=np.bincount(bucket_ids,minlength=bucket_count).astype(np.int64);wins=np.bincount(bucket_ids,weights=success,minlength=bucket_count)
    rate=np.full(bucket_count,np.nan);np.divide(wins,counts,out=rate,where=counts>0)
    observed=counts>0;n=counts[observed].astype(float);p=rate[observed];z=1.96;d=1+z*z/n
    center=(p+z*z/(2*n))/d;half=z*np.sqrt(p*(1-p)/n+z*z/(4*n*n))/d
    interval=np.full((bucket_count,2),np.nan);interval[observed]=np.column_stack((np.maximum(0,center-half),np.minimum(1,center+half)))
    return dict(counts=counts,success_rate=rate,wilson=interval,coverage=float(observed.sum()/bucket_count))
