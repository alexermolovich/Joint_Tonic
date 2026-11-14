import numpy as np

def shift_bucket_metrics(bucket_ids, errors, bucket_count):
    if type(bucket_count) is not int or not 1<=bucket_count<=256:raise ValueError('bucket count')
    if not isinstance(bucket_ids,np.ndarray) or bucket_ids.dtype!=np.int64 or bucket_ids.ndim!=1 or len(bucket_ids)>100000 or (bucket_ids<0).any() or (bucket_ids>=bucket_count).any():raise ValueError('bucket IDs')
    if not isinstance(errors,np.ndarray) or errors.dtype!=np.float64 or errors.shape!=bucket_ids.shape or not np.isfinite(errors).all() or (errors<0).any() or (errors>1000000).any():raise ValueError('errors')
    counts=np.bincount(bucket_ids,minlength=bucket_count).astype(np.int64);sums=np.bincount(bucket_ids,weights=errors,minlength=bucket_count)
    mean=np.full(bucket_count,np.nan);np.divide(sums,counts,out=mean,where=counts>0)
    worst=np.full(bucket_count,-np.inf);np.maximum.at(worst,bucket_ids,errors);worst[counts==0]=np.nan
    return dict(counts=counts,mean_error=mean,worst_error=worst)
