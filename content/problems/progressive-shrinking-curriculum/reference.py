import numpy as np

def sample_progressive_subnets(depths, widths, kernels, phase, count, seed):
    for choices,limit,odd in [(depths,16,False),(widths,256,False),(kernels,9,True)]:
        if type(choices) is not list or not 1<=len(choices)<=16 or any(type(v) is not int or not 1<=v<=limit or (odd and v%2!=1) for v in choices) or any(a<=b for a,b in zip(choices,choices[1:])):raise ValueError('choices')
    if type(phase) is not int or not 0<=phase<=3 or type(count) is not int or not 0<=count<=10000 or type(seed) is not int or not 0<=seed<=2**32-1:raise ValueError('sampling parameters')
    choices=[depths if phase>=3 else depths[:1],widths if phase>=2 else widths[:1],kernels if phase>=1 else kernels[:1]]
    u=np.random.Generator(np.random.PCG64(seed)).random((count,3));out=np.empty((count,3),dtype=np.int64)
    for j,values in enumerate(choices):out[:,j]=np.asarray(values,dtype=np.int64)[np.floor(u[:,j]*len(values)).astype(np.int64)]
    return out
