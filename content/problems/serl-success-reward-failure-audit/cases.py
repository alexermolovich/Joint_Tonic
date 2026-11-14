import numpy as np
from numpy.testing import assert_allclose,assert_array_equal

def bad(fn):
    try: fn()
    except ValueError: return
    raise AssertionError("expected ValueError")

def one(m):
    r=m.audit_success_rewards([.9,.8,.2],[True,False,False],[-1,0,1],[True]*3,.5,2);assert_array_equal(r['confusion'],[1,1,0,1]);assert r['precision']==.5 and r['recall']==1;assert_array_equal(r['false_positive_rate'],[1,0])
def equality(m):
    r=m.audit_success_rewards([.5],[False],[0],[True],.5,2);assert_array_equal(r['false_positive_counts'],[1,0]);assert_allclose(r['false_positive_rate'],[1,np.nan],equal_nan=True);assert np.isnan(r['recall'])
def oracle(m):
    rng=np.random.default_rng(548);p=rng.random(32768)[::2];y=rng.random(16384)>.7;typ=np.where(y,-1,rng.integers(0,32,16384));v=rng.random(16384)>.1;before=p.copy();r=m.audit_success_rewards(p,y,typ,v,.6,32)
    counts=np.zeros(32,int);fp=counts.copy();conf=np.zeros(4,int)
    for i in range(len(p)):
        if not v[i]:continue
        positive=p[i]>=.6;conf[0 if y[i] and positive else 1 if not y[i] and positive else 2 if y[i] else 3]+=1
        if not y[i]:counts[typ[i]]+=1;fp[typ[i]]+=int(positive)
    assert_array_equal(r['confusion'],conf);assert_array_equal(r['failure_counts'],counts);assert_allclose(r['false_positive_rate'],fp/counts);assert_array_equal(p,before);assert not np.shares_memory(r['failure_counts'],typ)
    r=m.audit_success_rewards(np.empty(0),np.empty(0,bool),np.empty(0,int),np.empty(0,bool),0,1);assert np.isnan(r['precision']) and not r['confusion'].any()
    r=m.audit_success_rewards([0],[True],[-1],[True],1,1);assert r['recall']==0

def invalid(m):
    for args in [([.5],[True],[0],[True],.5,1),([.5],[False],[-1],[True],.5,1),([np.nan],[False],[0],[False],.5,1),([.5],[False],[0],[True],10**1000,1)]:bad(lambda:m.audit_success_rewards(*args))
TESTS=[('Classifier failure breakdown','public',one),('Inclusive reward threshold and missing type','public',equality),('Independent record oracle noncontiguous scale and missing support','hidden',oracle),('Invalid classifier evidence','hidden',invalid)]
