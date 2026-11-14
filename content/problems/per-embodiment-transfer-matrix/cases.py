"""Original deterministic synthetic fixtures, CC0-1.0."""
import copy
import numpy as np

def rejects(fn):
    try:fn()
    except ValueError:return
    raise AssertionError("Expected ValueError")

def check(m,s,t,records,expected_s,expected_t):
 before=copy.deepcopy((s,t,records));out=m.build_transfer_matrix(s,t,records)
 assert type(out) is dict and set(out)=={'successes','trials','observed','rates'}
 shape=(len(s),len(t));xs=np.array(expected_s,dtype=np.int64);xt=np.array(expected_t,dtype=np.int64)
 for k,d in [('successes',np.int64),('trials',np.int64),('observed',np.bool_),('rates',np.float64)]:assert isinstance(out[k],np.ndarray) and out[k].shape==shape and out[k].dtype==d
 np.testing.assert_array_equal(out['successes'],xs);np.testing.assert_array_equal(out['trials'],xt);np.testing.assert_array_equal(out['observed'],xt>0)
 expected=np.full(shape,np.nan);np.divide(xs,xt,out=expected,where=xt>0);np.testing.assert_allclose(out['rates'],expected,rtol=1e-12,atol=1e-12,equal_nan=True)
 assert (s,t,records)==before
 for a in out:
  for b in out:
   if a!=b:assert not np.shares_memory(out[a],out[b])
def pooled(m):check(m,['solo','mixed'],['arm_a','arm_b'],[('mixed','arm_b',1,2),('mixed','arm_b',9,10),('solo','arm_a',2,4)],[[2,0],[0,10]],[[4,0],[0,12]])
def missing(m):check(m,['mixed'],['arm_b','arm_a'],[('mixed','arm_a',0,3)],[[0,0]],[[0,3]])
def empty(m):check(m,['a'],['b'],[],[[0]],[[0]])
def repetitions(m):check(m,['a'],['b'],[('a','b',999999,1000000)]*100000,[[99999900000]],[[100000000000]])
def axes(m):
 s=['s'+str(i) for i in range(128)];t=list(reversed(['t'+str(i) for i in range(128)]));records=[(a,b,i+j,i+j+1) for i,a in enumerate(s) for j,b in enumerate(t)]
 expected=[[i+j for j in range(128)] for i in range(128)];check(m,s,t,records,expected,[[v+1 for v in row] for row in expected])
def invalid(m):
 for s,t,r in [([],['b'],[]),(['a','a'],['b'],[]),(['A'],['b'],[]),(['á'],['b'],[]),(['a'],('b',),[]),(['a'],['b'],()),(['a'],['b'],[('c','b',1,2)]),(['a'],['b'],[['a','b',1,2]]),(['a'],['b'],[('a','b',True,2)]),(['a'],['b'],[('a','b',1,0)]),(['a'],['b'],[('a','b',3,2)]),(['a'],['b'],[('a','b',1,1000001)]),(['a'],['b'],[('a','b',-1,2)])]:rejects(lambda:m.build_transfer_matrix(s,t,r))

TESTS=[('Pool trials rather than percentages', 'public', pooled), ('Missing differs from measured zero', 'public', missing), ('Empty evidence', 'hidden', empty), ('Large duplicate counts remain int64', 'hidden', repetitions), ('Independent axis ordering at scale', 'hidden', axes), ('Malformed axes and records', 'hidden', invalid)]
