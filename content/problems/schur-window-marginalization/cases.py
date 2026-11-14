import numpy as np
from numpy.testing import assert_allclose,assert_array_equal

def bad(fn):
    with np.testing.assert_raises(ValueError):fn()

def coupled(m):
 r=m.marginalize_window(np.array([[2.,1.],[1.,2.]]),np.array([1.,0.]),1);assert_allclose(r['normal'],[[1.5]]);assert_allclose(r['reduced_rhs'],[1]);assert_allclose(r['retained_step'],[2/3]);assert_allclose(r['removed_step'],[-1/3]);assert r['constant_shift']==0
def diagonal(m):
 r=m.marginalize_window(np.diag([2.,4.]),np.array([2.,8.]),1);assert_allclose(r['normal'],[[2]]);assert_allclose(r['reduced_rhs'],[2]);assert_allclose(r['retained_step'],[1]);assert_allclose(r['removed_step'],[2]);assert r['constant_shift']==-8
def oracle(m):
 rng=np.random.default_rng(845);q=rng.normal(size=(96,96));h=q.T@q+np.eye(96);storage=np.zeros((96,192));storage[:,::2]=h;h=storage[:,::2];b=rng.normal(size=96);before=h.copy();r=m.marginalize_window(h,b,40);expected=np.linalg.solve(h,b);assert_allclose(np.r_[r['retained_step'],r['removed_step']],expected,atol=1e-12)
 # Verify minimum quadratic value for arbitrary retained points, not just the optimum.
 for _ in range(8):
  xa=rng.normal(size=40);xb=np.linalg.solve(h[40:,40:],b[40:]-h[40:,:40]@xa);x=np.r_[xa,xb];full=.5*x@h@x-b@x;reduced=.5*xa@r['normal']@xa-r['reduced_rhs']@xa+r['constant_shift'];assert_allclose(full,reduced,rtol=1e-12)
 assert_array_equal(h,before);assert not np.shares_memory(r['normal'],h)
def edges(m):
 r=m.marginalize_window(np.diag([1e-8,1.]),np.ones(2),1);assert_allclose(r['retained_step'],[1e8])
 h=np.array([[2.,1.+1e-10],[1.,2.]]);r=m.marginalize_window(h,np.array([1.,0.]),1);expected=np.linalg.solve((h+h.T)/2,[1,0]);assert_allclose(np.r_[r['retained_step'],r['removed_step']],expected)
def invalid(m):
 for h,b,n in [(np.diag([1e-9,1.]),np.ones(2),1),(np.diag([1e-8,100.]),np.ones(2),1),(np.array([[1.,1.],[0.,1.]]),np.ones(2),1),(np.eye(2),np.ones(2),True),(np.eye(2),np.ones(2),10**1000)]:bad(lambda:m.marginalize_window(h,b,n))
TESTS=[('Coupled marginalization','public',coupled),('Reduced quadratic constant','public',diagonal),('Independent full solve and eliminated quadratic identity at scale','hidden',oracle),('Condition bound and symmetry normalization','hidden',edges),('Invalid gauge conditioning and partition','hidden',invalid)]
