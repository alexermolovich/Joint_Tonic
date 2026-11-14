import numpy as np
from numpy.testing import assert_allclose,assert_array_equal

def bad(fn):
    with np.testing.assert_raises(ValueError):fn()

def first(m):
 r=m.pullback_policy(np.array([[2.]]),np.array([[1.]]),np.array([3.]),np.array([[4.]]),np.array([20.]));assert_array_equal(r['metric'],[[16]]);assert_array_equal(r['force'],[16])
def second(m):
 r=m.pullback_policy(np.array([[2.]]),np.array([[0.]]),np.array([3.]),np.array([[4.]]),np.array([20.]));assert_array_equal(r['force'],[40])
def oracle(m):
 rng=np.random.default_rng(817);j=rng.normal(size=(16,32))[:,::2];dj=rng.normal(size=(16,32))[:,::2];v=rng.normal(size=32)[::2];a=rng.normal(size=(16,16));metric=a.T@a;f=rng.normal(size=16);before=[x.copy() for x in [j,dj,v,metric,f]];r=m.pullback_policy(j,dj,v,metric,f)
 acceleration=rng.normal(size=16);task_error=j@acceleration+dj@v-np.linalg.solve(metric,f)
 # Gradient of task-space weighted least squares equals Mq*a-fq.
 expected=j.T@metric@task_error;assert_allclose(r['metric']@acceleration-r['force'],expected,rtol=1e-10,atol=1e-10)
 for x,y in zip(before,[j,dj,v,metric,f]):assert_array_equal(x,y)
 assert not np.shares_memory(r['metric'],metric)
def numerical_psd(m):
 r=m.pullback_policy(np.eye(2),np.eye(2),np.ones(2),np.diag([-5e-11,2.]),np.array([3.,4.]));assert_allclose(r['metric'],np.diag([0,2]));assert_allclose(r['force'],[3,2])
 # Accepted asymmetry is explicitly symmetrized.
 metric=np.array([[1.,5e-11],[0.,1.]]);r=m.pullback_policy(np.eye(2),np.zeros((2,2)),np.zeros(2),metric,np.ones(2));assert_allclose(r['metric'],(metric+metric.T)/2,atol=1e-14)
def invalid(m):
 for metric in [np.array([[-1e-6]]),np.array([[np.nan]])]:bad(lambda:m.pullback_policy(np.ones((1,1)),np.zeros((1,1)),np.ones(1),metric,np.ones(1)))
 bad(lambda:m.pullback_policy(np.eye(2),np.eye(2),np.ones(2),np.array([[1.,.1],[0.,1.]]),np.ones(2)))
 bad(lambda:m.pullback_policy(np.eye(2),np.zeros((1,2)),np.ones(2),np.eye(2),np.ones(2)))
TESTS=[('Curvature-corrected pullback','public',first),('Constant Jacobian','public',second),('Weighted least-squares gradient oracle','hidden',oracle),('Numerical PSD normalization','hidden',numerical_psd),('Invalid policy contract','hidden',invalid)]
