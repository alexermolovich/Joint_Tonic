import numpy as np
from numpy.testing import assert_allclose,assert_array_equal

def bad(fn):
    try: fn()
    except ValueError: return
    raise AssertionError("expected ValueError")

def one(m):
    r=m.sample_video_triplets([3,2],np.zeros((1,6)));assert_array_equal(r['video_ids'],[0]);assert_array_equal(r['frames'],[[0,1,2]]);assert_array_equal(r['negative_video_ids'],[1]);assert_array_equal(r['negative_frames'],[0])

def other(m):
    r=m.sample_video_triplets([5,3,4],[[.5,.9,.9,.9,.9,.9]]);assert_array_equal(r['video_ids'],[1]);assert_array_equal(r['frames'],[[0,1,2]]);assert_array_equal(r['negative_video_ids'],[2]);assert_array_equal(r['negative_frames'],[3])

def oracle(m):
    rng=np.random.default_rng(555);lengths=rng.integers(1,100001,1024);lengths[:4]=[1,2,3,5];u=rng.random((16384,12))[:,::2];u[-1]=np.nextafter(1.,0.);before=u.copy();r=m.sample_video_triplets(lengths,u);eligible=[i for i,n in enumerate(lengths) if n>=3]
    for row in range(len(u)):
        draw=u[row];v=eligible[int(draw[0]*len(eligible))];n=int(lengths[v]);i=int(draw[1]*(n-2));j=i+1+int(draw[2]*(n-i-2));k=j+1+int(draw[3]*(n-j-1));others=[x for x in range(len(lengths)) if x!=v];o=others[int(draw[4]*len(others))];f=int(draw[5]*lengths[o]);assert r['video_ids'][row]==v;assert_array_equal(r['frames'][row],[i,j,k]);assert r['negative_video_ids'][row]==o and r['negative_frames'][row]==f
    assert_array_equal(u,before);assert not np.shares_memory(r['frames'],u);assert r['frames'].dtype==np.int64
    r=m.sample_video_triplets([3,1],np.empty((0,6)));assert r['frames'].shape==(0,3)
    r=m.sample_video_triplets([3,1],np.full((1,6),np.nextafter(1.,0.)));assert_array_equal(r['frames'],[[0,1,2]]);assert_array_equal(r['negative_frames'],[0])

def invalid(m):
    for lengths,u in [([2,2],np.empty((0,6))),([3],np.zeros((1,6))),([3.,2.],np.zeros((1,6))),([3,2],np.ones((1,6))),([3,2],np.full((1,6),np.nan)),([3,2],np.zeros((1,5)))]:bad(lambda:m.sample_video_triplets(lengths,u))
TESTS=[('Minimum ordered triple','public',one),('Different-video recorded draw','public',other),('Scalar sequential sampler oracle at strided scale and upper draw boundary','hidden',oracle),('Invalid video lengths and draws','hidden',invalid)]
