import numpy as np


def invalid(call,error=ValueError):
    try: call()
    except error: return
    raise AssertionError("Expected "+error.__name__)


def checked(m,logits,quality,args,expected):
    before=(logits.copy(),quality.copy())
    out=m.filter_stable_masks(logits,quality,*args)
    assert isinstance(out,np.ndarray) and out.dtype==np.int64 and out.ndim==1
    np.testing.assert_array_equal(out,np.array(expected,dtype=np.int64))
    assert np.array_equal(logits,before[0]) and np.array_equal(quality,before[1])
    assert not np.shares_memory(out,logits) and not np.shares_memory(out,quality)


def stability_before_rank(m):
    checked(m,np.array([[[2.,2.,-2.]],[[2.,2.,-2.]],[[.2,2.,-2.]]]),np.array([.6,.9,1.]),
            (0.,1.,.75,.5),[1])


def equality_and_empty(m):
    checked(m,np.array([[[2.,-2.]],[[2.,2.]], [[-2.,-2.]]]),np.array([1.,1.,4.]),
            (0.,1.,0.,.5),[0,1])


def empty_batch(m):
    checked(m,np.empty((0,2,3)),np.empty((0,)),(0.,1.,0.,0.),[])
    checked(m,np.full((2,1,2),-2.),np.ones(2),(0.,1.,0.,0.),[])


def suppressed_not_suppressor(m):
    masks=np.array([[[1,1,0,0]],[[0,1,1,0]],[[0,0,1,1]]],dtype=bool)
    checked(m,np.where(masks,2.,-2.),np.array([3.,2.,1.]),(0.,1.,1.,.3),[0,2])
    checked(m,np.full((3,1,2),2.),np.ones(3),(0.,1.,1.,.99),[0])
    checked(m,np.array([[[1.,0.,-1.]]]),np.array([-8.]),(0.,1.,0.,1.),[0])
    checked(m,np.array([[[1.,0.,-1.]]]),np.array([-8.]),(0.,1.,.01,1.),[])


def independent_sets(m):
    rng=np.random.default_rng(41)
    raw=rng.integers(-3,4,(12,4,10)).astype(np.float64)
    logits=raw[:,:,::2];quality=np.arange(24,dtype=np.float64)[::2]%4
    theta,delta,stable,overlap=0.,1.,.2,.3
    base=[];eligible=[]
    for i,mask in enumerate(logits):
        flat=mask.ravel().tolist()
        base.append({p for p,value in enumerate(flat) if value>theta})
        high={p for p,value in enumerate(flat) if value>theta+delta}
        low={p for p,value in enumerate(flat) if value>theta-delta}
        score=len(high)/len(low) if low else 0.
        if base[-1] and score>=stable: eligible.append(i)
    kept=[]
    for i in sorted(eligible,key=lambda i:(-quality[i],i)):
        if all(len(base[i]&base[j])/len(base[i]|base[j])<=overlap for j in kept):
            kept.append(i)
    checked(m,logits,quality,(theta,delta,stable,overlap),kept)


def malformed(m):
    l=np.ones((1,1,1));q=np.ones(1)
    invalid(lambda:m.filter_stable_masks(l.tolist(),q,0,1,0,0),TypeError)
    invalid(lambda:m.filter_stable_masks(l,q.tolist(),0,1,0,0),TypeError)
    for bad in [l.astype(np.float32),l[0],np.ones((129,1,1)),np.ones((1,0,1)),np.ones((0,513,1)),
                np.full_like(l,np.nan),np.full_like(l,np.inf),np.full_like(l,1e6+1),np.ones((128,128,64))]:
        invalid(lambda:m.filter_stable_masks(bad,q,0,1,0,0))
    for bad in [q.astype(np.float32),q[:,None],np.ones(2),np.array([np.nan]),np.array([1e6+1])]:
        invalid(lambda:m.filter_stable_masks(l,bad,0,1,0,0))
    for args in [(True,1,0,0),(1001,1,0,0),(0,0,0,0),(0,-1,0,0),(0,1001,0,0),
                 (0,1,-.1,0),(0,1,1.1,0),(0,1,0,1.1),(0,1,0,np.nan),(0,1,0,10**1000)]:
        invalid(lambda:m.filter_stable_masks(l,q,*args))


def realistic(m):
    logits=np.full((128,64,64),-2.)
    for i in range(128):
        logits[i,i//64,i%64]=2.
    checked(m,logits,np.arange(128,dtype=np.float64),(0.,1.,1.,0.),list(range(127,-1,-1)))


TESTS=[
 ("Stability before score ranking","public",stability_before_rank),
 ("Overlap equality and empty masks","public",equality_and_empty),
 ("Empty candidates","public",empty_batch),
 ("Kept-only suppression and strict thresholds","hidden",suppressed_not_suppressor),
 ("Independent set overlap and strided arrays","hidden",independent_sets),
 ("Malformed mask contract","hidden",malformed),
 ("Many separate masks","hidden",realistic),
]

