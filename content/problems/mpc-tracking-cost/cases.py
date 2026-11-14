import numpy as np
from numpy.testing import assert_allclose, assert_array_equal

def example(m):
    assert m.mpc_tracking_cost([[1],[2],[3]],np.zeros((3,1)),[[1],[2]],[1],[2],[3])==42.
def terminal(m):
    assert m.mpc_tracking_cost([[2,-1]],[[0,0]],np.empty((0,1)),[9,9],[1],[2,3])==11.
def loop_oracle(m):
    rng=np.random.default_rng(10); x=rng.normal(size=(7,3)); r=rng.normal(size=(7,3)); u=rng.normal(size=(6,2)); old=x.copy(); q=[1,2,0]; s=[.1,3]; p=[4,1,2]
    expected=sum(q[d]*(x[k,d]-r[k,d])**2 for k in range(6) for d in range(3))+sum(s[j]*u[k,j]**2 for k in range(6) for j in range(2))+sum(p[d]*(x[-1,d]-r[-1,d])**2 for d in range(3))
    result=m.mpc_tracking_cost(x,r,u,q,s,p); assert isinstance(result,float); assert_allclose(result,expected); assert_array_equal(x,old)
def invariance(m):
    x=np.array([[1.,2],[3,4]]); r=np.array([[0.,0],[1,1]]); u=[[2]]
    a=m.mpc_tracking_cost(x,r,u,[1,2],[3],[4,5]); b=m.mpc_tracking_cost(x+7,r+7,u,[1,2],[3],[4,5]); assert a==b
def invalid(m):
    for weights in [[-1],[np.nan],[True],[[1]]]:
        with np.testing.assert_raises(ValueError): m.mpc_tracking_cost([[0],[1]],[[0],[1]],[[0]],weights,[1],[1])
    with np.testing.assert_raises(ValueError): m.mpc_tracking_cost([[0],[1]],[[0]],[[0]],[1],[1],[1])
TESTS=[('Stage effort and terminal terms','public',example),('Zero horizon','public',terminal),('Scalar loop oracle','hidden',loop_oracle),('Translation invariance','hidden',invariance),('Invalid objective','hidden',invalid)]
