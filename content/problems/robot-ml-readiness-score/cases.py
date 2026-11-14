from copy import deepcopy


def invalid(call):
    try: call()
    except ValueError: return
    raise AssertionError("Expected ValueError")


def example(m):
    result=m.readiness_score({"data":["automated","manual"],"model":["automated"],"infrastructure":["manual","none"],"monitoring":["automated","automated"]})
    assert result=={"categories":{"data":1.5,"model":1.0,"infrastructure":.5,"monitoring":2.0},"score":.5}


def empty(m):
    assert m.readiness_score({k:[] for k in ["data","model","infrastructure","monitoring"]})=={"categories":{"data":0.,"model":0.,"infrastructure":0.,"monitoring":0.},"score":0.}


def full(m):
    args={k:["automated"]*7 for k in ["data","model","infrastructure","monitoring"]}
    assert m.readiness_score(args)=={"categories":{k:7. for k in args},"score":7.}


def half_and_bottleneck(m):
    args={k:["manual"]*7 for k in ["data","model","infrastructure","monitoring"]}
    assert m.readiness_score(args)["score"]==3.5
    args["data"]=[];assert m.readiness_score(args)["score"]==0.
    args["data"]=["none","manual"];assert m.readiness_score(args)["score"]==.5


def invalid_inputs(m):
    base={k:[] for k in ["data","model","infrastructure","monitoring"]}
    for bad in [[],{},{"data":[]},{**base,"extra":[]},{**base,"data":()}, {**base,"data":["automatic"]},{**base,"data":[False]},{**base,"data":[[]]}, {**base,"data":["manual"]*8}]:
        invalid(lambda: m.readiness_score(bad))


def types_and_storage(m):
    args={k:["none","manual"] for k in ["data","model","infrastructure","monitoring"]};saved=deepcopy(args)
    out=m.readiness_score(args);assert type(out) is dict and set(out)=={"categories","score"}
    assert type(out["categories"]) is dict and all(type(x) is float for x in [out["score"],*out["categories"].values()])
    out["categories"]["data"]=99.;assert args==saved


TESTS=[("Unequal category coverage","public",example),("Empty evidence","public",empty),("Full automated coverage","public",full),
       ("Manual credits and weakest category","hidden",half_and_bottleneck),("Invalid questionnaire","hidden",invalid_inputs),
       ("Exact types and independent result","hidden",types_and_storage)]
