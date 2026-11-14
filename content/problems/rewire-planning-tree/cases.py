import numpy as np
from numpy.testing import assert_allclose,assert_array_equal

def bad(fn):
    with np.testing.assert_raises(ValueError):fn()

def fixture():return np.array([-1,0,1,0],dtype=np.int64),np.array([0.,5,2,1])
def first(m):
 p,e=fixture();r=m.rewire_tree(p,e,1,3,1,True);assert_array_equal(r['parents'],[-1,3,1,0]);assert_array_equal(r['edge_costs'],[0,1,2,1]);assert_array_equal(r['root_costs'],[0,2,4,1]);assert r['changed'] is True;assert_array_equal(p,[-1,0,1,0])
def cycle(m):
 p,e=fixture();r=m.rewire_tree(p,e,1,2,0,True);assert not r['changed'];assert_array_equal(r['root_costs'],[0,5,7,1]);assert_array_equal(r['parents'],p)
def gates(m):
 for parent,c,ok in [(1,0,True),(3,4,True),(3,9,True),(3,0,False)]:
  p,e=fixture();r=m.rewire_tree(p,e,1,parent,c,ok);assert not r['changed'];assert_array_equal(r['parents'],p);assert not np.shares_memory(r['parents'],p)
def scale(m):
 n=10000;store=np.zeros(n*2,dtype=np.int64);p=store[::2];p[:]=np.arange(n)-1;estore=np.ones(n*2);e=estore[::2];e[0]=0;before=[p.copy(),e.copy()];r=m.rewire_tree(p,e,5000,0,1,True)
 expected=np.arange(n,dtype=float);expected[5000:]-=4999;assert_array_equal(r['root_costs'],expected);assert r['parents'][5000]==0 and r['edge_costs'][5000]==1
 for a,b in zip(before,[p,e]):assert_array_equal(a,b)
 # Labels need not be topologically ordered.
 r=m.rewire_tree(np.array([-1,3,1,0],dtype=np.int64),np.array([0.,1,2,1]),2,0,1,True);assert_array_equal(r['root_costs'],[0,2,1,1])
def invalid(m):
 for p,e in [(np.array([-1,2,1],dtype=np.int64),np.array([0.,1,1])),(np.array([-1,-1],dtype=np.int64),np.zeros(2)),(np.array([-1,0],dtype=np.int64),np.array([1.,1]))]:bad(lambda:m.rewire_tree(p,e,1,0,0,True))
 p,e=fixture()
 for v,parent,c,ok in [(0,0,0,True),(1,4,0,True),(1,0,-1,True),(1,0,10**1000,True),(1,0,0,1),(True,0,0,True)]:bad(lambda:m.rewire_tree(p,e,v,parent,c,ok))
TESTS=[('Cheaper edge updates descendants','public',first),('Descendant proposal rejected','public',cycle),('Strict improvement and feasibility','hidden',gates),('Long chain, arbitrary labels and preservation','hidden',scale),('Invalid trees and arguments','hidden',invalid)]
