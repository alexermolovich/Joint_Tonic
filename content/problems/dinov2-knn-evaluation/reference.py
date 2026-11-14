import numpy as np


def knn_classify(train,labels,queries,k,num_classes,temperature):
    for x in (train,labels,queries):
        if not isinstance(x,np.ndarray):raise TypeError("Expected NumPy arrays")
    if type(num_classes) is not int or not 1<=num_classes<=1000:raise ValueError("Invalid class count")
    if train.dtype!=np.float64 or queries.dtype!=np.float64 or train.ndim!=2 or queries.ndim!=2:
        raise ValueError("Invalid feature dtype or rank")
    m,d=train.shape;n=queries.shape[0]
    if not 1<=m<=512 or not 0<=n<=512 or not 1<=d<=256 or queries.shape[1]!=d or labels.dtype!=np.int64 or labels.shape!=(m,):
        raise ValueError("Invalid feature or label shape")
    for x in (train,queries):
        if not np.isfinite(x).all() or not np.allclose(np.linalg.norm(x,axis=1),1,atol=1e-6,rtol=0):raise ValueError("Rows must be finite unit features")
    if np.any(labels<0) or np.any(labels>=num_classes) or type(k) is not int or not 1<=k<=m or type(temperature) not in (int,float) or not 1e-4<=temperature<=1e4:
        raise ValueError("Invalid labels or voting parameters")
    similarities=queries@train.T
    indices=np.argsort(-similarities,axis=1,kind="stable")[:,:k]
    selected=np.take_along_axis(similarities,indices,axis=1)/temperature
    exp=np.exp(selected-selected.max(axis=1,keepdims=True))
    votes=exp/exp.sum(axis=1,keepdims=True)
    scores=np.zeros((n,num_classes),dtype=np.float64)
    np.add.at(scores,(np.arange(n)[:,None],labels[indices]),votes)
    return scores.argmax(axis=1).astype(np.int64),scores
