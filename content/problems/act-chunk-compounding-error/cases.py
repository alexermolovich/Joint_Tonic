import numpy as np
from numpy.testing import assert_allclose,assert_array_equal

def bad(fn):
    try: fn()
    except ValueError: return
    raise AssertionError("expected ValueError")

def example1(m):assert_allclose(m.chunk_error_scores([[1],[1],[1]],[1,2,3]),[1,2,14/3])
def example2(m):assert_allclose(m.chunk_error_scores([[1],[-1]],[2,1]),[.5,1])
def invariant(m):
    x=np.array([[1.,2.],[-1.,1.],[2.,-2.]]);c=x.copy();r=m.chunk_error_scores(x,[1,3,1]);assert_allclose(r,[2.5,19/6,2.5]);assert_array_equal(x,c)
    assert_array_equal(m.chunk_error_scores(np.zeros((1024,4)),[1,17,1024]),[0,0,0])
def invalid(m):
    for e,l in [([], [1]),([[1]],[]),([[1]],[0]),([[1]],[2]),([[1]],[1.]),([[np.nan]],[1]),([[101]],[1]),([[1]], [True])]:bad(lambda:m.chunk_error_scores(e,l))
TESTS=[('Feedback intervals','public',example1),('Residual cancellation','public',example2),('Multichannel and zero errors','hidden',invariant),('Invalid diagnostic inputs','hidden',invalid)]

# Added realistic scale contract check
def scale_storage(m):
    e=np.ones((4096,32))[:,::2];l=np.array([1,2,4,8]);copy=e.copy();out=m.chunk_error_scores(e,l)
    assert_allclose(out,[(n+1)*(2*n+1)/6 for n in l]);assert_array_equal(e,copy);assert not np.shares_memory(e,out)

TESTS.append(('Realistic scale and input preservation','hidden',scale_storage))
