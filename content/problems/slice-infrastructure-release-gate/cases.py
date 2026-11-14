from copy import deepcopy
import numpy as np


def invalid(call):
    try: call()
    except ValueError: return
    raise AssertionError("Expected ValueError")


def example(m):
    required=["slice/night","infra/rollback","infra/runtime","slice/rain"]
    evidence={"slice/night":("v2",900,"pass"),"infra/rollback":("v1",990,"pass"),"infra/runtime":("v2",950,"fail")}
    assert m.release_rejections(required,evidence,"v2",1000,100)==[("infra/rollback","wrong_version"),("infra/runtime","failed"),("slice/rain","missing")]


def boundaries(m):
    args=["slice/fog","infra/timing","slice/fog"],{"slice/fog":("v3",99,"pass"),"infra/timing":("v3",201,"pass")},"v3",200,100
    assert m.release_rejections(*args)==[("infra/timing","future"),("slice/fog","stale")]


def accepted(m):
    assert m.release_rejections(["slice/a"],{"slice/a":("v1",5,"pass")},"v1",5,0)==[]
    assert m.release_rejections(["infra/a"],{},"v1",0,0)==[("infra/a","missing")]


def priority_and_extra(m):
    records={"slice/a":("v0",101,"fail"),"slice/b":("v1",101,"fail"),"slice/c":("v1",0,"fail"),"slice/d":("v1",100,"fail"),"infra/extra":("v0",999,"pass")}
    assert m.release_rejections(["slice/d","slice/b","slice/a","slice/c"],records,"v1",100,1)==[("slice/a","wrong_version"),("slice/b","future"),("slice/c","stale"),("slice/d","failed")]


def integer_time(m):
    now=2**63-1
    assert m.release_rejections(["slice/a","slice/b"],{"slice/a":("v1",now-1,"pass"),"slice/b":("v1",now-2,"pass")},"v1",now,1)==[("slice/b","stale")]


def malformed(m):
    invalid(lambda: m.release_rejections(["infra/x"], {"infra/x":("v1",1,np.array(["pass"]))}, "v1",1,0))
    good=(["slice/a"],{},"v1",0,0)
    for index,bad in [(0,[]),(0,()),(0,["a"]),(0,[False]),(1,[]),(1,{"slice/x":["v1",0,"pass"]}),(1,{"slice/x":("v1",-1,"pass")}),(1,{"slice/x":("v1",0,"unknown")}),(1,{"slice/x":("v1",0,[])}),(2,"V1"),(3,True),(4,10**1000)]:
        args=list(good);args[index]=bad;invalid(lambda: m.release_rejections(*args))
    invalid(lambda: m.release_rejections(["slice/a"]*10001,{},"v1",0,0))
    invalid(lambda: m.release_rejections(["slice/a"],{"slice/n"+str(i):("v1",0,"pass") for i in range(10001)},"v1",0,0))


def immutable(m):
    args=(["slice/a","slice/a"],{"slice/a":("v1",0,"fail")},"v1",0,0);saved=deepcopy(args)
    out=m.release_rejections(*args);assert out==[("slice/a","failed")] and type(out) is list and type(out[0]) is tuple
    assert args==saved


TESTS=[("Mixed rejection reasons","public",example),("Cutoff and duplicate requirements","public",boundaries),("Accepted and missing evidence","public",accepted),
       ("Reason priority and unrequired evidence","hidden",priority_and_extra),("Large integer timestamps","hidden",integer_time),
       ("Malformed metadata and declared bounds","hidden",malformed),("Immutable evidence and exact output","hidden",immutable)]
