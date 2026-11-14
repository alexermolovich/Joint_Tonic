"""Original deterministic synthetic fixtures, CC0-1.0."""
import copy
import numpy as np

def rejects(fn):
    try:fn()
    except ValueError:return
    raise AssertionError("Expected ValueError")


def three(m):
 r=m.episode_mean_interval(np.array([[1.],[3.],[5.]]),2);np.testing.assert_array_equal(r['mean'],[3]);np.testing.assert_allclose(r['standard_error'],[2/np.sqrt(3)]);np.testing.assert_allclose(r['interval'],[[3-4/np.sqrt(3),3+4/np.sqrt(3)]])
def fixed(m):
 r=m.episode_mean_interval(np.array([[2.,7.],[2.,7.]]),3);np.testing.assert_array_equal(r['standard_error'],[0,0]);np.testing.assert_array_equal(r['interval'],[[2,2],[7,7]])
def scale(m):
 x=np.repeat(np.arange(10000,dtype=float)[:,None],40,axis=1)[:,::2];before=x.copy();r=m.episode_mean_interval(x,1.96);np.testing.assert_array_equal(r['mean'],np.full(20,4999.5));variance=10000*10001/12;np.testing.assert_allclose(r['standard_error'],np.full(20,np.sqrt(variance/10000)));np.testing.assert_array_equal(x,before);assert not np.shares_memory(r['mean'],r['interval'])
def units(m):
 x=np.array([[0.,0.],[2.,20.]]);r=m.episode_mean_interval(x,2);np.testing.assert_array_equal(r['standard_error'],[1,10]);np.testing.assert_array_equal(r['interval'],[[-1,3],[-10,30]])
 r=m.episode_mean_interval(x,0);np.testing.assert_array_equal(r['interval'],[[1,1],[10,10]])
def invalid(m):
 for x,c in [(np.ones((1,1)),2),(np.ones((2,1),dtype=np.float32),2),(np.full((2,1),np.inf),2),(np.ones((2,0)),2),(np.ones((2,1)),True),(np.ones((2,1)),-1),(np.ones((2,1)),101),(np.ones((10000,21)),2)]:rejects(lambda:m.episode_mean_interval(x,c))

TESTS=[('Three episode uncertainty', 'public', three), ('Constant metric observations', 'public', fixed), ('Closed-form arithmetic progression variance at scale', 'hidden', scale), ('Separate metric units and unclipped intervals', 'hidden', units), ('Invalid episode interval inputs', 'hidden', invalid)]
