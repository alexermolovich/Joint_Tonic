"""Original deterministic synthetic fixtures, CC0-1.0."""
import copy
import numpy as np

def rejects(fn):
    try:fn()
    except ValueError:return
    raise AssertionError("Expected ValueError")


def fractional(m):
 r=m.aggregate_policy_returns(np.array([[0.,2.,4.,6.]]),.375);np.testing.assert_array_equal(r['mean'],[3]);np.testing.assert_array_equal(r['worst'],[0]);np.testing.assert_allclose(r['lower_tail'],[2/3])
def extremes(m):
 x=np.array([[4.,-2.]]);np.testing.assert_array_equal(m.aggregate_policy_returns(x,1)['lower_tail'],[1]);np.testing.assert_array_equal(m.aggregate_policy_returns(x,.1)['lower_tail'],[-2])
def subnormal(m):
 x=np.array([[.25,.75],[-.25,1.]])
 for a in [float(np.nextafter(0.,1.)),1e-300]:np.testing.assert_array_equal(m.aggregate_policy_returns(x,a)['lower_tail'],[.25,-.25])
def scale(m):
 x=np.tile(np.arange(10000,dtype=float),(20,1))[:,::-1];copyx=x.copy();r=m.aggregate_policy_returns(x,.12505)
 n=10000;q=.12505*n;k=int(q);want=(k*(k-1)/2+(q-k)*k)/q;np.testing.assert_allclose(r['lower_tail'],np.full(20,want));np.testing.assert_array_equal(r['mean'],np.full(20,4999.5));np.testing.assert_array_equal(r['worst'],np.zeros(20));np.testing.assert_array_equal(x,copyx)
 assert not np.shares_memory(r['worst'],r['lower_tail']) and not np.shares_memory(r['mean'],x)
def invalid(m):
 for x,a in [(np.array([[1]],dtype=np.int64),.5),(np.zeros((1,0)),.5),(np.zeros((65,1)),.5),(np.full((1,1),np.nan),.5),(np.zeros((1,1)),0),(np.zeros((1,1)),True),(np.zeros((1,1)),1.1),(np.zeros((1,1)),10**1000),(np.zeros((21,10000)),.5)]:rejects(lambda:m.aggregate_policy_returns(x,a))

TESTS=[('Fractional empirical tail mass', 'public', fractional), ('Full and tiny tails', 'public', extremes), ('Subnormal fraction avoids underflow', 'hidden', subnormal), ('Noncontiguous two hundred thousand returns', 'hidden', scale), ('Invalid return schema', 'hidden', invalid)]
