from copy import deepcopy
import numpy as np


def invalid(call):
    try: call()
    except ValueError: return
    raise AssertionError("Expected ValueError")


def chain(m):
    a={"data":("dataset","1"*64),"norm":("transform","2"*64),"policy":("model","3"*64),"score":("evaluator","4"*64)}
    p={"data":[],"norm":["data"],"policy":["data","norm"],"score":["policy","data"]}
    assert m.lineage_record(a,p,"score")==[(name,*a[name]) for name in ["data","norm","policy","score"]]


def equal_hash(m):
    a={"a":("dataset","a"*64),"b":("dataset","a"*64),"model":("model","b"*64),"unused":("transform","c"*64)}
    p={"a":[],"b":[],"model":["b","a","a"],"unused":[]}
    assert m.lineage_record(a,p,"model")==[("a","dataset","a"*64),("b","dataset","a"*64),("model","model","b"*64)]


def target_only(m):
    a={"a":("dataset","0"*64),"later":("model","1"*64)}
    assert m.lineage_record(a,{"a":[],"later":["a"]},"a")==[("a","dataset","0"*64)]


def cycles_and_unknowns(m):
    a={"a":("dataset","0"*64),"b":("model","1"*64),"c":("model","2"*64)}
    for p in [{"a":[],"b":["c"],"c":["b"]},{"a":["a"],"b":[],"c":[]},{"a":[],"b":[]},{"a":[],"b":[],"c":["missing"]}]:
        invalid(lambda: m.lineage_record(a,p,"a"))


def malformed(m):
    invalid(lambda: m.lineage_record({"a":(np.array(["model"]),"a"*64)},{"a":[]},"a"))
    good={"a":("dataset","0"*64)}
    for a,p,t in [({},{},"a"),([],{},"a"),({"a":("bad","0"*64)},{"a":[]},"a"),({"a":("dataset","A"*64)},{"a":[]},"a"),({"a":["dataset","0"*64]},{"a":[]},"a"),(good,{"a":()},"a"),(good,{"a":[[]]},"a"),(good,{"a":[]},"missing"),(good,{"a":[]} ,False)]:
        invalid(lambda: m.lineage_record(a,p,t))
    invalid(lambda: m.lineage_record(good,{"a":["a"]*50001},"a"))
    a={"n"+str(i):("dataset","0"*64) for i in range(10001)}
    invalid(lambda: m.lineage_record(a,{n:[] for n in a},"n0"))


def deep_and_storage(m):
    nodes=["n"+str(i).zfill(5) for i in range(7000)]
    a={n:("model","a"*64) for n in nodes};p={n:[] if i==0 else [nodes[i-1]] for i,n in enumerate(nodes)}
    saved=deepcopy((a,p));out=m.lineage_record(a,p,nodes[-1])
    assert out==[(n,"model","a"*64) for n in nodes] and (a,p)==saved
    assert type(out) is list and all(type(row) is tuple for row in out)


TESTS=[("Complete evaluation lineage","public",chain),("Distinct IDs with identical bytes","public",equal_hash),("Target without ancestors","public",target_only),
       ("Whole graph validation","hidden",cycles_and_unknowns),("Malformed records and size bounds","hidden",malformed),
       ("Deep graph and input preservation","hidden",deep_and_storage)]
