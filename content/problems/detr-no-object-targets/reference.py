import numpy as np


def build_query_targets(labels,target_valid,matches,num_classes,eos_weight):
    for x in (labels,target_valid,matches):
        if not isinstance(x,np.ndarray):raise TypeError("Expected NumPy arrays")
    if type(num_classes) is not int or not 1<=num_classes<=1000 or type(eos_weight) not in (int,float) or not 0<=eos_weight<=1:
        raise ValueError("Invalid class parameters")
    if labels.dtype!=np.int64 or target_valid.dtype!=np.bool_ or matches.dtype!=np.int64 or labels.ndim!=2 or matches.ndim!=2 or target_valid.shape!=labels.shape:
        raise ValueError("Invalid target arrays")
    b,m=labels.shape
    if not 1<=b<=128 or not 0<=m<=300 or matches.shape[0]!=b or not 1<=matches.shape[1]<=300 or np.any(labels<0) or np.any(labels>=num_classes) or np.any(matches< -1) or np.any(matches>=m):
        raise ValueError("Invalid shape or index")
    selected=matches>=0
    for row in range(b):
        indices=matches[row,selected[row]]
        if np.unique(indices).size!=indices.size or not target_valid[row,indices].all():raise ValueError("Invalid one-to-one target assignment")
    classes=np.full(matches.shape,num_classes,dtype=np.int64)
    rows,cols=np.nonzero(selected)
    classes[rows,cols]=labels[rows,matches[rows,cols]]
    weights=np.full(matches.shape,float(eos_weight),dtype=np.float64)
    weights[selected]=1.
    return classes,weights
