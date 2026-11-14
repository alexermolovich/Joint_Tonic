from copy import deepcopy
import numpy as np

def invalid(call):
    try:
        call()
    except ValueError:
        return
    raise AssertionError("Expected ValueError")

def same_distribution(m):
    assert m.categorical_skew({"indoor":2,"outdoor":2},{"indoor":20,"outdoor":20},0)=={"deltas":[("indoor",0.0),("outdoor",0.0)],"distance":0.0,"flagged":False}

def new_category(m):
    assert m.categorical_skew({"dry":3,"wet":1},{"dry":1,"snow":1},.25)=={"deltas":[("dry",-.25),("snow",.5),("wet",-.25)],"distance":.5,"flagged":True}

def exact_boundary(m):
    out=m.categorical_skew({"a":1,"b":1},{"a":1},.5)
    assert out=={"deltas":[("a",.5),("b",-.5)],"distance":.5,"flagged":False}

def zero_and_types(m):
    train={"z":0,"a":10**12};serve={"a":10**12,"b":0};before=deepcopy((train,serve))
    out=m.categorical_skew(train,serve,0)
    assert out["deltas"]==[("a",0.),("b",0.),("z",0.)]
    assert type(out["distance"]) is float and type(out["flagged"]) is bool
    assert all(type(t) is tuple and type(t[1]) is float for t in out["deltas"])
    assert (train,serve)==before

def malformed(m):
    good={"a":1}
    for bad in [None,[],{},{"a":0},{"a":True},{"a":-1},{"a":10**12+1},{"a":1.0},{"a":np.int64(1)},{"Bad":1},{1:1}]:
        invalid(lambda: m.categorical_skew(bad,good,0))
        invalid(lambda: m.categorical_skew(good,bad,0))
    for threshold in [True,-.1,1.1,float("nan"),float("inf"),10**1000,np.float64(.5),"0"]:
        invalid(lambda: m.categorical_skew(good,good,threshold))
    invalid(lambda: m.categorical_skew({"a"+str(i):1 for i in range(10001)},good,0))

def independent_histogram(m):
    # Integer cross-products independently give the probability differences.
    rng=np.random.default_rng(20261113)
    a={f"c{i}":int(x) for i,x in enumerate(rng.integers(0,100,200))}
    b={f"c{i+100}":int(x) for i,x in enumerate(rng.integers(0,100,200))}
    sa,sb=sum(a.values()),sum(b.values())
    expected=[(key,(b.get(key,0)*sa-a.get(key,0)*sb)/(sa*sb)) for key in sorted(a.keys()|b.keys())]
    out=m.categorical_skew(a,b,.01)
    assert [x[0] for x in out["deltas"]]==[x[0] for x in expected]
    np.testing.assert_allclose([x[1] for x in out["deltas"]],[x[1] for x in expected],rtol=1e-12,atol=1e-12)
    assert np.isclose(out["distance"],max(abs(x[1]) for x in expected),rtol=1e-12,atol=1e-12)
    assert out["flagged"] is (out["distance"]>.01)

def realistic(m):
    a={"a"+str(i):10**12 for i in range(10000)}
    out=m.categorical_skew(a,a,0)
    assert len(out["deltas"])==10000 and out["distance"]==0. and out["flagged"] is False

TESTS=[("Different totals same distribution","public",same_distribution),("Aligned new category","public",new_category),("Strict threshold boundary","public",exact_boundary),
       ("Zero categories and immutable typed output","hidden",zero_and_types),("Invalid histogram contracts","hidden",malformed),("Independent integer-product oracle","hidden",independent_histogram),("Large valid histogram","hidden",realistic)]

