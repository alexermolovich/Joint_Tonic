import numpy as np

def stratify_visual_factors(permutations, jitter):
    if not isinstance(permutations,np.ndarray) or permutations.dtype!=np.int64 or permutations.ndim!=2 or permutations.shape[1]!=4 or not 1<=len(permutations)<=10000:raise ValueError('permutation shape/dtype')
    if not isinstance(jitter,np.ndarray) or jitter.dtype!=np.float64 or jitter.shape!=permutations.shape or not np.isfinite(jitter).all() or (jitter<0).any() or (jitter>=1).any():raise ValueError('jitter')
    n=len(permutations)
    if not np.array_equal(np.sort(permutations,axis=0),np.broadcast_to(np.arange(n)[:,None],(n,4))):raise ValueError('column permutation')
    lower=permutations/n;upper=(permutations+1)/n
    return np.maximum(lower,np.minimum((permutations+jitter)/n,np.nextafter(upper,lower)))
