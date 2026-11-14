from copy import deepcopy
import numpy as np

def invalid(call):
    try:
        call()
    except ValueError:
        return
    raise AssertionError("Expected ValueError")

def numeric(shape=(2,), required=True):
    return {"kind":"numeric","shape":shape,"required":required,"minimum":-1.0,"maximum":1.0,"domain":None}

def categorical():
    return {"kind":"categorical","shape":(),"required":False,"minimum":None,"maximum":None,"domain":("dry","wet")}

def missing_and_range(m):
    assert m.feature_anomalies([{"joint":np.array([0.,2.])},{}],{"joint":numeric()})==[(0,"joint","range"),(1,"joint","missing")]

def categorical_priority(m):
    records=[{"terrain":np.array("snow")},{"terrain":np.array(["snow"])},{"extra":None},{}]
    assert m.feature_anomalies(records,{"terrain":categorical()})==[(0,"terrain","domain"),(1,"terrain","shape"),(2,"extra","unexpected")]

def valid_edges(m):
    assert m.feature_anomalies([],{"joint":numeric()})==[]
    assert m.feature_anomalies([{"joint":np.array([-1.,1.])}],{"joint":numeric()})==[]
    assert m.feature_anomalies([{"terrain":np.array("dry")},{}],{"terrain":categorical()})==[]

def priority_and_dtypes(m):
    records=[{"x":None},{"x":np.array([np.nan])},{"x":np.array([2,3])},
             {"x":np.array([np.nan,2.])},{"x":np.array([np.inf,-2.])},{"x":np.array([0.,1.])}]
    assert m.feature_anomalies(records,{"x":numeric()})==[(0,"x","type"),(1,"x","shape"),(2,"x","dtype"),(3,"x","nonfinite"),(4,"x","nonfinite")]
    assert m.feature_anomalies([{"x":np.array("dry",dtype=object)},{"x":np.array(b"dry")}],{"x":categorical()})==[(0,"x","dtype"),(1,"x","dtype")]
    assert m.feature_anomalies([{"x":np.array(1.)}],{"x":numeric(())})==[]

def malformed_schema(m):
    for spec in [None,{**numeric(),"extra":1},{**numeric(),"kind":np.array(["numeric"])},{**numeric(),"shape":[2]},
                 {**numeric(),"shape":(True,)},{**numeric(),"shape":(0,)},{**numeric(),"shape":(129,)},{**numeric(),"shape":(8,8,8,8)},
                 {**numeric(),"shape":(1,1,1,1,1)},{**numeric(),"required":1},{**numeric(),"minimum":10**1000},
                 {**numeric(),"maximum":float("nan")},{**numeric(),"minimum":2},{**numeric(),"domain":("x",)},
                 {**categorical(),"domain":[]},{**categorical(),"domain":("dry","dry")},{**categorical(),"domain":("Bad",)},
                 {**categorical(),"minimum":0}]:
        invalid(lambda: m.feature_anomalies([],{"x":spec}))
    for schema in [None,[],{},{"Bad":numeric()}]:
        invalid(lambda: m.feature_anomalies([],schema))
    for records in [None,{},[[]],[{"Bad":None}], [{}]*1001]:
        invalid(lambda: m.feature_anomalies(records,{"x":numeric()}))

def budget(m):
    invalid(lambda: m.feature_anomalies([{"extra":np.zeros(1025)}],{"x":numeric()}))
    invalid(lambda: m.feature_anomalies([{f"f{i}":None for i in range(129)}],{"x":numeric()}))
    invalid(lambda: m.feature_anomalies([], {f"f{i}":numeric() for i in range(129)}))
    # Repeated occurrences count toward the workload even if arrays share storage.
    records=[{"x":np.zeros(1000)} for _ in range(1000)]
    out=m.feature_anomalies(records,{"x":numeric((100,10))})
    assert len(out)==1000 and out[0]==(0,"x","shape")
    records[0]["extra"]=np.zeros(1)
    invalid(lambda: m.feature_anomalies(records,{"x":numeric((100,10))}))

def ordering_and_preservation(m):
    values=np.array([1.,99.,-1.,99.])[::2];before=values.copy()
    records=[{"z":None,"a":values}]
    schema={"b":numeric(required=True),"a":numeric()}
    out=m.feature_anomalies(records,schema)
    assert out==[(0,"b","missing"),(0,"z","unexpected")]
    assert np.array_equal(values,before)
    assert all(type(row) is tuple and type(row[0]) is int for row in out)

TESTS=[("Missing and inclusive range","public",missing_and_range),("Categorical shape priority","public",categorical_priority),("Valid boundaries and empty records","public",valid_edges),
       ("Ordered dtype and numeric reasons","hidden",priority_and_dtypes),("Invalid schemas and containers","hidden",malformed_schema),
       ("Declared per-array and total budget","hidden",budget),("Stable issue order and noncontiguous preservation","hidden",ordering_and_preservation)]

