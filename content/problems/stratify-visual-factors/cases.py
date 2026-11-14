"""Original deterministic synthetic fixtures, CC0-1.0."""
import copy
import numpy as np

def rejects(fn):
    try:fn()
    except ValueError:return
    raise AssertionError("Expected ValueError")


def two(m):
 p=np.array([[0,1,0,1],[1,0,1,0]],dtype=np.int64);np.testing.assert_allclose(m.stratify_visual_factors(p,np.full((2,4),.5)),[[.25,.75,.25,.75],[.75,.25,.75,.25]])
def one(m):
 j=np.array([[0,.2,.5,.9]]);r=m.stratify_visual_factors(np.zeros((1,4),dtype=np.int64),j);np.testing.assert_array_equal(r,j);assert not np.shares_memory(r,j)
def scale(m):
 n=10000;rng=np.random.default_rng(9);p=np.column_stack([rng.permutation(n) for _ in range(8)])[:,::2];j=rng.random((n,8))[:,::2];pc=p.copy();jc=j.copy();r=m.stratify_visual_factors(p,j)
 np.testing.assert_array_equal(np.floor(r*n).astype(np.int64),p);np.testing.assert_array_equal(p,pc);np.testing.assert_array_equal(j,jc);assert r.dtype==np.float64 and not np.shares_memory(r,j)
def joint(m):
 p=np.tile(np.arange(4,dtype=np.int64)[:,None],(1,4));r=m.stratify_visual_factors(p,np.zeros((4,4)));np.testing.assert_array_equal(r[:,0],r[:,3]);np.testing.assert_array_equal(r[:,0],[0,.25,.5,.75])
def invalid(m):
 p=np.array([[0,1,0,1],[1,0,1,0]],dtype=np.int64);j=np.zeros((2,4))
 for a,b in [(p.astype(np.int32),j),(p,j.astype(np.float32)),(p[:,:3],j[:,:3]),(np.zeros((2,4),dtype=np.int64),j),(p,np.ones((2,4))),(p,np.full((2,4),np.nan)),(p,np.full((2,4),-.1)),(p[:0],j[:0])]:rejects(lambda:m.stratify_visual_factors(a,b))

TESTS=[('Two complementary scenarios', 'public', two), ('One scenario storage', 'public', one), ('Ten thousand noncontiguous strata', 'hidden', scale), ('Marginal coverage is not full joint coverage', 'hidden', joint), ('Invalid permutations and jitter', 'hidden', invalid)]


def near_upper_boundary(m):
 p=np.array([[0,1,0,1],[1,0,1,0]],dtype=np.int64);j=np.full((2,4),np.nextafter(1.,0.));r=m.stratify_visual_factors(p,j)
 assert (r>=p/2).all() and (r<(p+1)/2).all()
 np.testing.assert_array_equal(r,np.nextafter((p+1)/2,p/2))
TESTS.append(('Upper jitter rounding remains inside each stratum','hidden',near_upper_boundary))
