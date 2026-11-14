"""Original deterministic synthetic fixtures; CC0-1.0."""
import numpy as np
import math

def arr(x):return np.array(x,dtype=np.float64)
def equal(actual,expected,dtype=np.float64):
    assert isinstance(actual,np.ndarray) and actual.dtype==np.dtype(dtype)
    assert actual.shape==np.asarray(expected).shape
    np.testing.assert_allclose(actual,expected,rtol=1e-9,atol=1e-10)
def reject(fn):
    try:fn()
    except ValueError:return
    raise AssertionError('Expected ValueError')
def preserve(before,after):
    for a,b in zip(before,after):np.testing.assert_array_equal(a,b)

def example1(m):
 r=m.layer_error_report(arr([[3,4],[0,0]]),arr([[3,5],[0,0]]),1);equal(r['row_rmse'],[math.sqrt(.5),0]);equal(r['row_max_abs'],[1,0]);equal(r['failed_rows'],[False,False],bool);assert r['relative_l2']==.2 and r['passed'] is True
def example2(m):
 r=m.layer_error_report(arr([[0]]),arr([[2]]),1);equal(r['row_rmse'],[2]);equal(r['failed_rows'],[True],bool);assert r['relative_l2']==2e12 and r['passed'] is False
def edges(m):
 r=m.layer_error_report(arr([[0,0]]),arr([[0,0]]),0);assert r['relative_l2']==0 and r['passed'] is True
 r=m.layer_error_report(np.array([[1]],dtype=np.float32),np.array([[1]],dtype=np.float32),0);assert type(r['relative_l2']) is float
 r=m.layer_error_report(arr([[1],[1]]),arr([[1],[1.0001]]),0);equal(r['failed_rows'],[False,True],bool)
def oracle(m):
 rng=np.random.default_rng(23);a=rng.normal(size=(512,64))[:,::2];b=a+np.linspace(0,.2,512)[:,None];before=[a.copy(),b.copy()];r=m.layer_error_report(a,b,.1)
 diffs=[[float(b[i,j])-float(a[i,j]) for j in range(32)] for i in range(512)];equal(r['row_rmse'],[math.sqrt(sum(e*e for e in row)/32) for row in diffs]);equal(r['row_max_abs'],[max(abs(e) for e in row) for row in diffs]);equal(r['failed_rows'],[max(abs(e) for e in row)>.1 for row in diffs],bool)
 assert math.isclose(r['relative_l2'],math.sqrt(sum(e*e for row in diffs for e in row))/math.sqrt(sum(float(v)**2 for v in a.flat)),rel_tol=1e-10);preserve(before,[a,b])
def invalid(m):
 for t in [-1,True,float('nan'),10**1000]:reject(lambda:m.layer_error_report(arr([[0]]),arr([[0]]),t))
 reject(lambda:m.layer_error_report(arr([[0]]),arr([[0,0]]),0));reject(lambda:m.layer_error_report(np.empty((0,1)),np.empty((0,1)),0));reject(lambda:m.layer_error_report(arr([[0]]),arr([[np.inf]]),0))

TESTS=[('Worked example 1','public',example1),('Worked example 2','public',example2),('Boundary and numerical conventions','hidden',edges),('Independent oracle, realistic scale and preservation','hidden',oracle),('Invalid documented contract','hidden',invalid)]
