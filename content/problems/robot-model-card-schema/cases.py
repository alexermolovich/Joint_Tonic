"""Original deterministic synthetic fixtures; CC0-1.0."""
import copy
import numpy as np

def reject(fn):
    try:fn()
    except ValueError:return
    raise AssertionError('Expected ValueError')
def same(a,b):np.testing.assert_array_equal(a,b)

def card(metrics=None):return dict(model_id='policy',artifacts=dict(weights='1'*64,preprocessing='2'*64,action_decoder='3'*64,runtime='4'*64),intended_embodiments=['fr3'],limitations='One room only',metrics=[] if metrics is None else metrics)
def metric(s,n,k):return dict(slice_id=s,trials=n,successes=k)
def example1(m):assert m.validate_robot_model_card(card([metric('day',10,2)]),['day'])==[]
def example2(m):assert m.validate_robot_model_card(card([metric('night',0,1)]),['day','night'])==[('day','missing'),('night','invalid_success_count'),('night','no_trials')]
def edges(m):
 assert m.validate_robot_model_card(card([metric('day',10,0),metric('extra',1,1)]),['day'])==[]
 assert m.validate_robot_model_card(card(),[])==[]
 assert m.validate_robot_model_card(card([metric('zero',0,0)]),[])==[('zero','no_trials')]
 assert m.validate_robot_model_card(card([metric('large',10**9,10**9)]),['large'])==[]
def oracle_scale(m):
 records=[];expected=[]
 for i in range(10000):
  n=0 if i%3==0 else 10;k=11 if i%5==0 else 0;s='s'+str(i);records.append(metric(s,n,k))
  if n==0:expected.append((s,'no_trials'))
  if k>n:expected.append((s,'invalid_success_count'))
 c=card(records);before=copy.deepcopy(c);r=m.validate_robot_model_card(c,['missing']);assert r==sorted(expected+[('missing','missing')]);assert c==before

def invalid(m):
 c=card();del c['artifacts']['runtime'];reject(lambda:m.validate_robot_model_card(c,[]))
 c=card();c['artifacts']['weights']='BAD';reject(lambda:m.validate_robot_model_card(c,[]))
 for metrics in [[metric('x',True,0)],[metric('x',-1,0)],[metric('x',1,0)]*2,[metric('x',1,10**9+1)]]:reject(lambda:m.validate_robot_model_card(card(metrics),[]))
 reject(lambda:m.validate_robot_model_card(card(),['x','x']));c=card();c['limitations']=' ';reject(lambda:m.validate_robot_model_card(c,[]))

TESTS=[('Worked example1','public',example1),('Worked example2','public',example2),('Boundary semantics','hidden',edges),('Independent oracle,scale and preservation','hidden',oracle_scale),('Invalid documented inputs','hidden',invalid)]
