from copy import deepcopy
from fractions import Fraction
import numpy as np

def invalid(call):
    try:
        call()
    except ValueError:
        return
    raise AssertionError("Expected ValueError")

def pooled_vs_macro(m):
    out=m.quality_performance([("expert","easy",True)]*9+[("expert","hard",False)])
    assert out=={"by_slice":[("expert","easy",9,9,1.),("expert","hard",1,0,0.)],"by_quality":[("expert",10,9,.9,.5)]}

def qualities(m):
    assert m.quality_performance([("mixed","lift",False),("expert","lift",True),("mixed","lift",True)])=={"by_slice":[("expert","lift",1,1,1.),("mixed","lift",2,1,.5)],"by_quality":[("expert",1,1,1.,1.),("mixed",2,1,.5,.5)]}

def empty(m):
    assert m.quality_performance([])=={"by_slice":[],"by_quality":[]}

def independent_slices(m):
    rows=[("q","a",True),("q","a",False),("q","a",False),("q","b",True),("q","b",True)]
    saved=deepcopy(rows);out=m.quality_performance(rows)
    expected=float((Fraction(1,3)+1)/2)
    assert out["by_quality"][0][:3]==("q",5,3)
    np.testing.assert_allclose(out["by_quality"][0][3:],[.6,expected],rtol=1e-12,atol=1e-12)
    assert rows==saved
    for row in out["by_slice"]:
        assert type(row) is tuple and type(row[2]) is int and type(row[3]) is int and type(row[4]) is float
    row=out["by_quality"][0];assert type(row[3]) is float and type(row[4]) is float

def malformed(m):
    for rows in [None,(),[["q","t",True]],[("q","t")],[("Bad","t",True)],[("q",1,True)],
                 [("q","t",1)],[("q","t",np.bool_(True))],[("q","t",None)]]:
        invalid(lambda:m.quality_performance(rows))
    invalid(lambda:m.quality_performance([("q","t",True)]*100001))
    invalid(lambda:m.quality_performance([("q",f"t{i}",True) for i in range(10001)]))

def scale(m):
    rows=[(f"q{i%10}",f"t{i%10000}",bool(i%2)) for i in range(100000)]
    out=m.quality_performance(rows)
    assert len(out["by_slice"])==10000 and sum(row[2] for row in out["by_slice"])==100000
    assert sum(row[3] for row in out["by_slice"])==50000
    assert out["by_slice"]==sorted(out["by_slice"]) and out["by_quality"]==sorted(out["by_quality"])

TESTS=[("Pooled versus task-balanced rate","public",pooled_vs_macro),("Separate quality conditions","public",qualities),("Empty evaluation","public",empty),
       ("Independent rational aggregate and types","hidden",independent_slices),("Malformed trials and budgets","hidden",malformed),("Large bounded slice report","hidden",scale)]

