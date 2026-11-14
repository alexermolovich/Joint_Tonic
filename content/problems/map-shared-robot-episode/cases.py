from copy import deepcopy
from fractions import Fraction
import numpy as np

def invalid(call):
    try:
        call()
    except ValueError:
        return
    raise AssertionError("Expected ValueError")

def episode():
    return {"values":np.array([[90.,25.],[0.,-10.]]),"timestamps_ns":np.array([100,200],dtype=np.int64),
            "channels":[("yaw","deg"),("x","cm")],"frame":"base","control_mode":"delta",
            "dataset_id":"set_a","dataset_version":"v1","robot_id":"arm_a"}

def reordered(m):
    out=m.remap_robot_episode(episode(),[("x","m"),("yaw","rad")])
    np.testing.assert_allclose(out["values"],[[.25,np.pi/2],[-.1,0]],rtol=1e-12,atol=1e-12)
    assert out["channels"]==[("x","m"),("yaw","rad")]
    assert np.array_equal(out["timestamps_ns"],[100,200])
    for key in ("frame","control_mode","dataset_id","dataset_version","robot_id"):
        assert out[key]==episode()[key]

def empty_subset(m):
    e=episode();e["values"]=np.empty((0,2));e["timestamps_ns"]=np.empty((0,),dtype=np.int64)
    out=m.remap_robot_episode(e,[("x","mm")])
    assert out["values"].shape==(0,1) and out["timestamps_ns"].shape==(0,)
    assert out["channels"]==[("x","mm")]

def identity(m):
    e=episode();out=m.remap_robot_episode(e,e["channels"])
    np.testing.assert_allclose(out["values"],e["values"],rtol=1e-12,atol=1e-12)
    assert set(out)==set(e)

def incompatible(m):
    for target in [[("missing","m")],[("x","rad")],[("yaw","unitless")],[],[("x","m"),("x","cm")],[("x",np.array(["m"]))],[("Bad","m")]]:
        invalid(lambda:m.remap_robot_episode(episode(),target))

def malformed(m):
    for key,value in [("values",[[1,2]]),("values",np.ones((1,2),dtype=np.float32)),("values",np.ones((2,))),
                      ("values",np.ones((2,3))),("values",np.array([[np.nan,0],[0,0]])),("values",np.full((2,2),1e6+1)),
                      ("timestamps_ns",np.array([100,100],dtype=np.int64)),("timestamps_ns",np.array([-1,100],dtype=np.int64)),
                      ("timestamps_ns",np.array([100,200],dtype=np.float64)),("timestamps_ns",np.array([100],dtype=np.int64)),
                      ("channels",[("yaw","deg"),("yaw","deg")]),("frame","Bad"),("dataset_version","v1.0"),
                      ("control_mode",np.array(["delta"])),("control_mode","velocity")]:
        e=episode();e[key]=value;invalid(lambda:m.remap_robot_episode(e,[("x","m")]))
    invalid(lambda:m.remap_robot_episode({**episode(),"extra":1},[("x","m")]))
    invalid(lambda:m.remap_robot_episode(None,[("x","m")]))

def noncontiguous_exact_clock(m):
    e=episode();raw=np.arange(24.).reshape(4,6);e["values"]=raw[::2,::3]
    stamps=np.array([2**63-4,2**63-3,2**63-2,2**63-1],dtype=np.int64);e["timestamps_ns"]=stamps[::2]
    values_before=e["values"].copy();stamps_before=e["timestamps_ns"].copy();target=[("x","mm"),("yaw","rad")]
    out=m.remap_robot_episode(e,target)
    assert np.array_equal(out["timestamps_ns"],stamps_before) and out["timestamps_ns"].dtype==np.int64
    assert out["values"].dtype==np.float64
    assert not np.shares_memory(out["values"],e["values"]) and not np.shares_memory(out["timestamps_ns"],e["timestamps_ns"])
    assert out["channels"] is not target and out["channels"] is not e["channels"]
    assert np.array_equal(e["values"],values_before) and np.array_equal(e["timestamps_ns"],stamps_before)
    out["values"][0,0]=-42;out["timestamps_ns"][0]=0;out["channels"].append(("extra","m"))
    assert np.array_equal(e["values"],values_before) and np.array_equal(e["timestamps_ns"],stamps_before) and len(target)==2

def all_units_and_scale(m):
    e=episode();e["channels"]=[("yaw","rad"),("x","m")];e["values"]=np.array([[np.pi,1.],[0.,-1.]])
    out=m.remap_robot_episode(e,[("yaw","deg"),("x","mm")])
    np.testing.assert_allclose(out["values"],[[180.,1000.],[0.,-1000.]],rtol=1e-12,atol=1e-12)
    e=episode();e["values"]=np.ones((10000,2))*1e6;e["timestamps_ns"]=np.arange(10000,dtype=np.int64)
    assert m.remap_robot_episode(e,[("x","mm")])["values"].shape==(10000,1)
    e["values"]=np.ones((10001,2));e["timestamps_ns"]=np.arange(10001,dtype=np.int64)
    invalid(lambda:m.remap_robot_episode(e,[("x","m")]))

TESTS=[("Reorder and convert compatible units","public",reordered),("Empty episode subset","public",empty_subset),("Identity preserves metadata","public",identity),
       ("Unknown channels and incompatible units","hidden",incompatible),("Malformed episode contract","hidden",malformed),
       ("Noncontiguous ownership and exact clock","hidden",noncontiguous_exact_clock),("Unit directions and bounded scale","hidden",all_units_and_scale)]

