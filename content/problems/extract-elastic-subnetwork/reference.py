import numpy as np

def extract_subnetwork(weights, depth, width, kernel):
    if type(weights) is not list or not 1<=len(weights)<=16:raise ValueError("layer list")
    shape=None;total=0
    for weight in weights:
        if not isinstance(weight,np.ndarray) or weight.dtype!=np.float64 or weight.ndim!=4:raise ValueError("float64 convolution weights")
        c,ci,k,ki=weight.shape
        if not 1<=c<=64 or c!=ci or not 1<=k<=9 or k%2!=1 or ki!=k:raise ValueError("square channel/kernel contract")
        if shape is not None and weight.shape!=shape:raise ValueError("layer shape mismatch")
        if not np.isfinite(weight).all() or (np.abs(weight)>100).any():raise ValueError("weight values")
        shape=weight.shape;total+=weight.size
    if total>1000000:raise ValueError("weight budget")
    c,_,k,_=shape
    if type(depth) is not int or not 1<=depth<=len(weights) or type(width) is not int or not 1<=width<=c or type(kernel) is not int or not 1<=kernel<=k or kernel%2!=1:raise ValueError("subnetwork dimensions")
    offset=(k-kernel)//2
    return [w[:width,:width,offset:offset+kernel,offset:offset+kernel].copy() for w in weights[:depth]]
