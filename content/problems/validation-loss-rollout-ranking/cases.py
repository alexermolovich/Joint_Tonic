from copy import deepcopy
from fractions import Fraction
import numpy as np

def invalid(call):
    try:
        call()
    except ValueError:
        return
    raise AssertionError("Expected ValueError")

def disagree(m):
    assert m.compare_checkpoint_metrics([("early",.1,1,10),("later",.2,8,10)])=={"offline_order":["early","later"],"rollout_order":["later","early"],"disagree":True}

def tied(m):
    assert m.compare_checkpoint_metrics([("zeta",.3,1,2),("alpha",.3,5,10)])=={"offline_order":["alpha","zeta"],"rollout_order":["alpha","zeta"],"disagree":False}

def one(m):
    assert m.compare_checkpoint_metrics([("only",0,0,1)])=={"offline_order":["only"],"rollout_order":["only"],"disagree":False}

def exact_rate_and_winner(m):
    rows=[("a",0,999998,999999),("b",1,999999,1000000),("winner",0,1,1)]
    before=deepcopy(rows);out=m.compare_checkpoint_metrics(rows)
    assert out["rollout_order"]==["winner","b","a"] and out["offline_order"]==["a","winner","b"]
    assert out["disagree"] is True and rows==before
    # Different full order but the same winner: disagreement is false.
    out=m.compare_checkpoint_metrics([("a",0,1,1),("b",1,0,1),("c",2,1,2)])
    assert out["disagree"] is False and out["offline_order"]!=out["rollout_order"]
    assert out["offline_order"] is not out["rollout_order"]

def malformed(m):
    for rows in [None,(),[],[["x",0,1,1]],[("x",0,1)],[("Bad",0,1,1)],[("x",0,1,1)]*2,
                 [("x",True,1,1)],[("x",float("nan"),1,1)],[("x",10**1000,1,1)],[("x",-1,1,1)],
                 [("x",0,True,1)],[("x",0,1,True)],[("x",0,1,np.int64(1))],[("x",0,0,0)],
                 [("x",0,2,1)],[("x",0,-1,1)],[("x",0,1,1000001)]]:
        invalid(lambda:m.compare_checkpoint_metrics(rows))

def large(m):
    rows=[(f"c{i}",i,10000-i,10000) for i in range(10000)]
    out=m.compare_checkpoint_metrics(rows[::-1])
    assert out["offline_order"]==[f"c{i}" for i in range(10000)]==out["rollout_order"]
    assert out["disagree"] is False
    invalid(lambda:m.compare_checkpoint_metrics(rows+[("overflow",0,1,1)]))

TESTS=[("Offline and rollout winners disagree","public",disagree),("Exact fractional ties","public",tied),("One candidate","public",one),
       ("Exact near-ratios and winner semantics","hidden",exact_rate_and_winner),("Malformed metrics","hidden",malformed),("Bounded scale ordering","hidden",large)]

