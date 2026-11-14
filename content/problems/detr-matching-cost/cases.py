import numpy as np
from numpy.testing import assert_allclose, assert_array_equal


def inputs():
    return (np.array([[.8,.1,.1],[.2,.7,.1]]), np.array([[.25,.5,.5,1],[.75,.5,.5,1]]),
            np.array([0,1],dtype=np.int64),np.array([[.25,.5,.5,1],[.75,.5,.5,1]]))


def competition(m):
    assert_allclose(m.detr_matching_cost(*inputs(),(1.,1.,1.)),[[-1.8,.4],[.3,-1.7]],atol=1e-9)


def disjoint(m):
    p=np.array([[.6,.4]])
    a=np.array([[.1,.5,.2,.2]]); b=np.array([[.9,.5,.2,.2]])
    result=m.detr_matching_cost(p,a,np.array([0],dtype=np.int64),b,(0.,0.,1.))
    assert_allclose(result,[[.6]],atol=1e-9)


def empty(m):
    p,a,_,_=inputs()
    result=m.detr_matching_cost(p,a,np.empty(0,dtype=np.int64),np.empty((0,4)))
    assert result.shape==(2,0) and result.dtype==np.float64


def independent_terms(m):
    p,a,l,b=inputs()
    assert_allclose(m.detr_matching_cost(p,a,l,b,(1.,0.,0.)),-p[:,l])
    assert_allclose(m.detr_matching_cost(p,a,l,b,(0.,1.,0.)),[[0,.5],[.5,0]])
    assert_allclose(m.detr_matching_cost(p,a,l,b,(0.,0.,1.)),[[-1,0],[0,-1]],atol=1e-9)


def boundaries(m):
    p=np.array([[.9,.1],[.4,.6]])
    a=np.array([[0.,0.,1.,1.],[1.,1.,1e-6,1e-6]])
    l=np.array([0,0],dtype=np.int64)
    result=m.detr_matching_cost(p,a,l,a.copy(),(0.,0.,1.))
    assert_allclose(np.diag(result),[-1,-1],atol=1e-9)
    assert np.isfinite(result).all()
    # Corners outside the image must remain unclipped.
    b=np.array([[.5,0.,1.,1.]])
    assert_allclose(m.detr_matching_cost(p,a,np.array([0],dtype=np.int64),b,(0.,0.,1.))[0,0],-1/3,atol=1e-9)


def scalar_oracle(m):
    rng=np.random.default_rng(20261113)
    p=rng.uniform(.1,1,(37,5));p/=p.sum(1,keepdims=True)
    a=np.column_stack([rng.uniform(0,1,(37,2)),rng.uniform(.03,1,(37,2))])
    b=np.column_stack([rng.uniform(0,1,(11,2)),rng.uniform(.03,1,(11,2))])
    labels=rng.integers(0,4,11,dtype=np.int64)
    result=m.detr_matching_cost(p,a,labels,b)
    expected=np.empty((37,11))
    for i in range(37):
        for j in range(11):
            ax,ay,aw,ah=a[i];bx,by,bw,bh=b[j]
            left=max(ax-aw/2,bx-bw/2);right=min(ax+aw/2,bx+bw/2)
            top=max(ay-ah/2,by-bh/2);bottom=min(ay+ah/2,by+bh/2)
            inter=max(0,right-left)*max(0,bottom-top)
            union=aw*ah+bw*bh-inter
            encl=(max(ax+aw/2,bx+bw/2)-min(ax-aw/2,bx-bw/2))*(max(ay+ah/2,by+bh/2)-min(ay-ah/2,by-bh/2))
            g=inter/union-(encl-union)/encl
            expected[i,j]=-p[i,labels[j]]+5*sum(abs(a[i]-b[j]))-2*g
    assert_allclose(result,expected,atol=1e-9)


def validation(m):
    p,a,l,b=inputs()
    with np.testing.assert_raises(TypeError):m.detr_matching_cost(p.tolist(),a,l,b)
    variants=[(p.astype(np.float32),a,l,b),(p*2,a,l,b),(p,a,l.astype(np.int32),b),(p,a,np.array([2,1],dtype=np.int64),b),(p,a,l,b[:1])]
    tiny=a.copy();tiny[0,2]=1e-20;variants.append((p,tiny,l,b))
    bad=a.copy();bad[0,0]=np.nan;variants.append((p,bad,l,b))
    for args in variants:
        with np.testing.assert_raises(ValueError):m.detr_matching_cost(*args)
    for w in [(0,0,0),(True,1,1),[1,1,1],(1,np.nan,1),(101,1,1),(10**1000,1,1)]:
        with np.testing.assert_raises(ValueError):m.detr_matching_cost(p,a,l,b,w)


def preservation(m):
    args=inputs();copies=[x.copy() for x in args]
    out=m.detr_matching_cost(*args)
    for a,b in zip(args,copies):
        assert_array_equal(a,b)
        assert not np.shares_memory(a,out)


TESTS=[("Competing queries","public",competition),("Disjoint geometry","public",disjoint),("Empty targets","public",empty),
       ("Separate weighted terms","hidden",independent_terms),("Box boundary convention","hidden",boundaries),
       ("Independent scalar oracle","hidden",scalar_oracle),("Validation","hidden",validation),("Input preservation","hidden",preservation)]
