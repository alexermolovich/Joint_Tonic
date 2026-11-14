import numpy as np
from numpy.testing import assert_allclose,assert_array_equal


def nearest(m):
    p,s=m.knn_classify(np.array([[1.,0.],[0.,1.],[-1.,0.]]),np.array([0,1,1],dtype=np.int64),np.array([[1.,0.],[0.,1.]]),1,2,1.)
    assert_array_equal(p,[0,1]);assert_array_equal(s,[[1,0],[0,1]])


def weighted(m):
    p,s=m.knn_classify(np.eye(2),np.array([0,1],dtype=np.int64),np.array([[1.,0.]]),2,2,1.)
    assert_array_equal(p,[0]);assert_allclose(s,[[.7310585786,.2689414214]],atol=1e-9)


def empty(m):
    p,s=m.knn_classify(np.eye(2),np.array([0,1],dtype=np.int64),np.empty((0,2)),1,2,1.)
    assert p.shape==(0,) and s.shape==(0,2) and p.dtype==np.int64


def ties_and_duplicates(m):
    train=np.array([[1.,0.],[1.,0.],[1.,0.]])
    labels=np.array([1,0,2],dtype=np.int64)
    p,s=m.knn_classify(train,labels,np.array([[1.,0.]]),1,3,.1)
    assert_array_equal(p,[1]);assert_array_equal(s,[[0,1,0]])
    p,s=m.knn_classify(train,labels,np.array([[1.,0.]]),2,3,.1)
    assert_array_equal(p,[0]);assert_allclose(s,[[.5,.5,0]])


def oracle(m):
    rng=np.random.default_rng(20261113);train=rng.normal(size=(31,7));train/=np.linalg.norm(train,axis=1,keepdims=True);q=rng.normal(size=(9,7));q/=np.linalg.norm(q,axis=1,keepdims=True);labels=rng.integers(0,4,31,dtype=np.int64)
    p,s=m.knn_classify(train,labels,q,5,4,.3)
    for i in range(9):
        scores=[float(q[i]@row) for row in train];idx=sorted(range(31),key=lambda j:(-scores[j],j))[:5]
        v=np.exp(np.array([scores[j] for j in idx])/.3);v/=v.sum();expected=np.zeros(4)
        for j,w in zip(idx,v):expected[labels[j]]+=w
        assert_allclose(s[i],expected,atol=1e-9);assert p[i]==np.argmax(expected)


def invalid(m):
    def call(t=np.eye(2),l=np.array([0,1],dtype=np.int64),q=np.eye(2),k=1,c=2,temp=1.):return m.knn_classify(t,l,q,k,c,temp)
    with np.testing.assert_raises(TypeError):call(t=[])
    for kwargs in [dict(t=np.zeros((2,2))),dict(l=np.array([0,2],dtype=np.int64)),dict(q=np.ones((1,3))),dict(k=True),dict(k=3),dict(c=0),dict(temp=10**1000),dict(temp=0)]:
        with np.testing.assert_raises(ValueError):call(**kwargs)


TESTS=[("Closest prototypes","public",nearest),("Weighted class vote","public",weighted),("Empty queries","public",empty),
       ("Neighbor and class ties","hidden",ties_and_duplicates),("Independent neighbor oracle","hidden",oracle),("Validation","hidden",invalid)]
