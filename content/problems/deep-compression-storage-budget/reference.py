import numpy as np

def _array(x, rank):
    if not isinstance(x,np.ndarray) or x.dtype not in (np.dtype('float32'),np.dtype('float64')) or x.ndim!=rank or x.size>1000000 or not np.isfinite(x).all() or (x.size and np.max(np.abs(x))>1e6):
        raise ValueError('invalid numeric array')
    return x.astype(np.float64)

def _pair(x,w,limit=2048):
    x,w=_array(x,2),_array(w,2)
    if not all(1<=n<=limit for n in (*x.shape,*w.shape)) or x.shape[1]!=w.shape[0]:raise ValueError('shape')
    return x,w

def _real(v,lo=0,hi=1e6):
    if type(v) not in (int,float) or not lo<=v<=hi or not np.isfinite(v):raise ValueError('scalar')
    return float(v)

def compressed_storage_budget(dense_count, frequencies, code_lengths, index_bits, centroid_bits, header_bytes):
    for x,lo,hi in [(dense_count,1,10**12),(index_bits,1,64),(header_bytes,0,10**6)]:
        if type(x) is not int or not lo<=x<=hi:raise ValueError('integer')
    if type(centroid_bits) is not int or centroid_bits not in (16,32):raise ValueError('centroid bits')
    for x in (frequencies,code_lengths):
        if not isinstance(x,np.ndarray) or x.dtype!=np.int64 or x.ndim!=1 or not 1<=x.size<=256:raise ValueError('integer array')
    if frequencies.shape!=code_lengths.shape or np.any(frequencies<0) or np.any(frequencies>10**12) or np.any(code_lengths<1) or np.any(code_lengths>32):raise ValueError('counts/lengths')
    f=[int(x) for x in frequencies];lengths=[int(x) for x in code_lengths];n=sum(f)
    if n>dense_count or sum(1<<(32-l) for l in lengths)>1<<32:raise ValueError('representation infeasible')
    bits=sum(a*b for a,b in zip(f,lengths));symbols=(bits+7)//8;indices=(n*index_bits+7)//8;book=len(f)*centroid_bits//8;total=symbols+indices+book+header_bytes;dense=4*dense_count
    return {'symbol_bits':bits,'symbol_bytes':symbols,'index_bytes':indices,'codebook_bytes':book,'total_bytes':total,'dense_bytes':dense,'compression_ratio':dense/total}
