from copy import deepcopy
from fractions import Fraction
import numpy as np

def invalid(call):
    try:
        call()
    except ValueError:
        return
    raise AssertionError("Expected ValueError")

def gated(m):
    assert m.select_checkpoint([("fit",.2,8,10),("risky",.8,9,10),("short",.1,1,1)],.3,(4,5),10)=="fit"

def tied(m):
    assert m.select_checkpoint([("zeta",.1,1,2),("alpha",.1,5,10)],.1,(1,2),2)=="alpha"

def none_pass(m):
    assert m.select_checkpoint([("x",.1,1,2)],.1,(1,2),3) is None
    assert m.select_checkpoint([],0,(0,1),1) is None

def priorities_and_zero(m):
    rows=[("zero",0,0,0),("low_loss",0,8,10),("best_rate",1,9,10),("tie",2,9,10)]
    saved=deepcopy(rows);assert m.select_checkpoint(rows,2,(0,1),1)=="best_rate" and rows==saved
    assert m.select_checkpoint([("a",0,999998,999999),("b",1,999999,1000000)],2,(0,1),1)=="b"
    assert m.select_checkpoint([("x",0,2,3)],0,(2,3),1)=="x"
    assert m.select_checkpoint([("x",0,2,3)],0,(666667,1000000),1) is None

def malformed(m):
    good=[("x",0,1,1)]
    for loss in [True,-1,float("nan"),float("inf"),10**1000,np.float64(0)]:
        invalid(lambda:m.select_checkpoint([],loss,(0,1),1))
    for threshold in [None,[0,1],(0,0),(2,1),(-1,1),(0,1000001),(True,1),(0,np.int64(1)),(0,10**1000)]:
        invalid(lambda:m.select_checkpoint([],0,threshold,1))
    for n in [True,0,-1,1000001,1.]:
        invalid(lambda:m.select_checkpoint([],0,(0,1),n))
    for rows in [None,(),[["x",0,1,1]],good*2,[("Bad",0,1,1)],[("x",-1,1,1)],[("x",True,1,1)],
                 [("x",0,2,1)],[("x",0,True,1)],[("x",0,0,-1)],[("x",0,1,1000001)]]:
        invalid(lambda:m.select_checkpoint(rows,0,(0,1),1))

def large(m):
    rows=[(f"c{i}",i,1,1) for i in range(10000)]
    assert m.select_checkpoint(rows,10000,(1,1),1)=="c0"
    invalid(lambda:m.select_checkpoint(rows+[("overflow",0,0,0)],0,(0,1),1))

TESTS=[("Multiple evidence gates","public",gated),("Equality and deterministic ties","public",tied),("No eligible candidate","public",none_pass),
       ("Selection priorities and zero trials","hidden",priorities_and_zero),("Malformed evidence and thresholds","hidden",malformed),("Large bounded candidate list","hidden",large)]

