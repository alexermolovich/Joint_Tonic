"""Original deterministic synthetic fixtures, CC0-1.0."""
import copy
import numpy as np

def rejects(fn):
    try:fn()
    except ValueError:return
    raise AssertionError("Expected ValueError")


def tradeoff(m):
 assert m.select_pareto_model([('a',.9,10),('b',.8,5),('c',.7,12)],.8,10)==dict(frontier=['a','b'],selected='a')
def infeasible(m):
 assert m.select_pareto_model([('a',.9,10),('b',.8,5)],1,1)==dict(frontier=['a','b'],selected=None)
def ties(m):
 a=[('z',.9,2),('a',.9,2),('b',.9,3),('c',.8,2)];saved=copy.deepcopy(a)
 assert m.select_pareto_model(a,.9,2)==dict(frontier=['a','z'],selected='a');assert a==saved
 assert m.select_pareto_model([],0,1)==dict(frontier=[],selected=None)
def scale(m):
 records=[('m'+str(i),i/1000,(i+1)/10) for i in range(1000)]
 r=m.select_pareto_model(records,.5,75);assert r['frontier']==sorted(x[0] for x in records);assert r['selected']=='m749'
 records.append(('overflow',1,1));rejects(lambda:m.select_pareto_model(records,0,1))
def invalid(m):
 for records,a,l in [([('x',.9,0)],0,1),([('x',True,1)],0,1),([('x',np.nan,1)],0,1),([('x',10**1000,1)],0,1),([('x',.9,1),('x',.8,2)],0,1),([('X',.9,1)],0,1),([],False,1),([],0,np.inf),([],0,0)]:rejects(lambda:m.select_pareto_model(records,a,l))

TESTS=[('Accuracy latency tradeoff', 'public', tradeoff), ('No feasible model', 'public', infeasible), ('Identical metrics retain IDs and deterministic ties', 'hidden', ties), ('Thousand point frontier', 'hidden', scale), ('Invalid identities and metrics', 'hidden', invalid)]
