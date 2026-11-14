from copy import deepcopy
from fractions import Fraction
import numpy as np

def invalid(call):
    try:
        call()
    except ValueError:
        return
    raise AssertionError("Expected ValueError")

def ties(m):
    out=m.allocate_dataset_batch({"c":1,"a":1,"b":1},2)
    assert out=={"a":1,"b":1,"c":0} and list(out)==["a","b","c"]

def unequal(m):
    assert m.allocate_dataset_batch({"large":30,"small":10,"disabled":0},5)=={"disabled":0,"large":4,"small":1}

def empty_batch(m):
    assert m.allocate_dataset_batch({"z":1,"a":0},0)=={"a":0,"z":0}

def rational_oracle(m):
    rng=np.random.default_rng(20261113)
    weights={f"d{i}":int(x) for i,x in enumerate(rng.integers(0,1000000,50))}
    saved=deepcopy(weights);n=999983;total=sum(weights.values())
    quotas={name:Fraction(n*w,total) for name,w in weights.items()}
    expected={name:q.numerator//q.denominator for name,q in quotas.items()}
    remaining=n-sum(expected.values())
    order=sorted(weights,key=lambda name:(-(quotas[name]-expected[name]),name))
    for name in order[:remaining]:expected[name]+=1
    out=m.allocate_dataset_batch(weights,n)
    assert out==expected and list(out)==sorted(out) and sum(out.values())==n
    assert all(type(v) is int for v in out.values()) and weights==saved

def malformed(m):
    for weights in [None,[],{},{"x":0},{"Bad":1},{"x":True},{"x":1.},{"x":np.int64(1)},{"x":-1},{"x":10**12+1}]:
        invalid(lambda:m.allocate_dataset_batch(weights,0))
    for size in [True,-1,1000001,1.,np.int64(1),10**1000]:
        invalid(lambda:m.allocate_dataset_batch({"x":1},size))

def scale_large_weights(m):
    weights={f"d{i}":10**12 for i in range(10000)}
    out=m.allocate_dataset_batch(weights,1000000)
    assert len(out)==10000 and all(v==100 for v in out.values())
    invalid(lambda:m.allocate_dataset_batch({**weights,"overflow":1},0))

TESTS=[("Exact remainder ties","public",ties),("Unequal weights and disabled source","public",unequal),("Zero-sized batch","public",empty_batch),
       ("Independent rational quota oracle","hidden",rational_oracle),("Malformed weights and batch size","hidden",malformed),("Large integer product and source budget","hidden",scale_large_weights)]

