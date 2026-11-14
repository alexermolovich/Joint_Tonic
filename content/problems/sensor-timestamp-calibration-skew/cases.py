from copy import deepcopy
import numpy as np

def invalid(call):
    try:
        call()
    except ValueError:
        return
    raise AssertionError("Expected ValueError")

def dual_reason(m):
    assert m.sensor_metadata_skew({"camera":(1000,"cal_v1"),"joints":(1000,"joint_v1")},{"camera":(1011,"cal_v2"),"joints":(1010,"joint_v1")},10)==[("camera","calibration"),("camera","timing")]

def changed_identity(m):
    assert m.sensor_metadata_skew({"wrist":(50,"c1")},{"overhead":(50,"c1")},0)==[("overhead","unexpected"),("wrist","missing")]

def empty(m):
    assert m.sensor_metadata_skew({}, {},0)==[]
    assert m.sensor_metadata_skew({"x":(1,"c")},{"x":(1,"c")},0)==[]

def exact_nanoseconds(m):
    top=2**63-1
    assert m.sensor_metadata_skew({"x":(top,"c")},{"x":(top-1,"c")},0)==[("x","timing")]
    assert m.sensor_metadata_skew({"x":(top,"c")},{"x":(0,"c")},top)==[]
    assert m.sensor_metadata_skew({"x":(0,"c")},{"x":(top,"c")},top-1)==[("x","timing")]

def malformed(m):
    good={"x":(0,"c")}
    for bad in [[],None,{"Bad":(0,"c")},{"x":[0,"c"]},{"x":(0,)},{"x":(True,"c")},{"x":(np.int64(0),"c")},{"x":(-1,"c")},{"x":(2**63,"c")},{"x":(0,"")},{"x":(0,np.array(["c"]))}]:
        invalid(lambda: m.sensor_metadata_skew(bad,good,0))
        invalid(lambda: m.sensor_metadata_skew(good,bad,0))
    for limit in [True,-1,2**63,10**1000,1.,np.int64(0)]:
        invalid(lambda: m.sensor_metadata_skew(good,good,limit))

def scale_order_preservation(m):
    expected={f"s{i}":(100,"c") for i in range(1000)}
    observed={f"s{i}":(99,"d") for i in reversed(range(1000))}
    saved=deepcopy((expected,observed));out=m.sensor_metadata_skew(expected,observed,0)
    assert out==sorted([(f"s{i}",reason) for i in range(1000) for reason in ("calibration","timing")])
    assert (expected,observed)==saved
    expected["overflow"]=(0,"c")
    invalid(lambda: m.sensor_metadata_skew(expected,{},0))

TESTS=[("Timing and calibration can both fail","public",dual_reason),("Missing and unexpected sensor","public",changed_identity),("Empty and exact matches","public",empty),
       ("Exact integer nanosecond differences","hidden",exact_nanoseconds),("Malformed metadata","hidden",malformed),("Bounded scale sorted output and preservation","hidden",scale_order_preservation)]

