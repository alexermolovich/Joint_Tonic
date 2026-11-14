from copy import deepcopy
import numpy as np

def invalid(call):
    try:
        call()
    except ValueError:
        return
    raise AssertionError("Expected ValueError")

def signal(values, unit="rad", frame="robot"):
    return {"values": np.asarray(values, dtype=np.float64), "unit": unit, "frame": frame}

def required_optional(m):
    episodes=[{"joints":signal([[0,2],[1,4]]),"force":signal([[5]],"n","tool")},{"joints":signal([[-1,3]])}]
    out=m.infer_episode_schema(episodes)
    assert set(out)=={"joints","force"}
    for name,low,high,required in [("joints",[-1,2],[1,4],True),("force",[5],[5],False)]:
        item=out[name]
        assert set(item)=={"shape","unit","frame","minimum","maximum","required"}
        assert item["shape"]==(len(low),) and type(item["shape"]) is tuple
        assert np.array_equal(item["minimum"],low) and np.array_equal(item["maximum"],high)
        assert item["required"] is required
    assert out["joints"]["unit"]=="rad" and out["force"]["frame"]=="tool"

def empty_episode(m):
    out=m.infer_episode_schema([{},{"speed":signal([[2],[4]],"m/s","base")}])["speed"]
    assert out["required"] is False and np.array_equal(out["minimum"],[2]) and np.array_equal(out["maximum"],[4])

def empty_collection(m):
    assert m.infer_episode_schema([])=={} and m.infer_episode_schema([{},{}])=={}

def physical_consistency(m):
    for other in [signal([[1,2]]),signal([[1]],"m"),signal([[1]],"rad","tool")]:
        invalid(lambda: m.infer_episode_schema([{"x":signal([[0]])},{"x":other}]))
    out=m.infer_episode_schema([{"x":signal([[2]])},{"x":signal([[1],[3],[0]])}])
    assert out["x"]["shape"]==(1,) and np.array_equal(out["x"]["minimum"],[0])

def malformed(m):
    for episodes in [None,{},[[]],[{"Bad":signal([[1]])}],[{"x":None}],[{"x":{**signal([[1]]),"extra":1}}],
                     [{"x":signal([[1]],"") }],[{"x":signal([[1]],"rad","world space")}],
                     [{"x":{"values":[[1]],"unit":"m","frame":"base"}}],
                     [{"x":signal([1])}],[{"x":signal([[]])}],[{"x":signal([[float("nan")]])}],
                     [{"x":signal([[float("inf")]])}],[{"x":signal([[1000001]])}],
                     [{"x":{**signal([[1]]),"values":np.ones((1,1),dtype=np.float32)}}],
                     [{"x":signal(np.ones((1,129)))}],[{"x":signal(np.ones((10001,1)))}],
                     [{"x":signal([[1]],np.array(["rad"]))}],[{}]*1001]:
        invalid(lambda: m.infer_episode_schema(episodes))
    invalid(lambda: m.infer_episode_schema([{"s"+str(i):signal([[0]]) for i in range(129)}]))

def storage_and_noncontiguous(m):
    values=np.arange(24.,dtype=np.float64).reshape(4,6)[:,::2]; saved=values.copy()
    out=m.infer_episode_schema([{"x":{"values":values,"unit":"m","frame":"base"}}])["x"]
    assert np.array_equal(values,saved)
    assert out["minimum"].dtype==np.float64 and out["maximum"].dtype==np.float64
    assert out["minimum"].shape==(3,) and out["maximum"].shape==(3,)
    assert not np.shares_memory(values,out["minimum"]) and not np.shares_memory(values,out["maximum"])
    assert not np.shares_memory(out["minimum"],out["maximum"])
    out["minimum"][0]=-42
    assert np.array_equal(values,saved) and out["maximum"][0]==18

def realistic_budget(m):
    a=np.linspace(-1000000,1000000,1000000).reshape(10000,100)
    out=m.infer_episode_schema([{"x":signal(a)},{"x":signal(a[::-1])}])
    assert out["x"]["required"] is True
    assert np.array_equal(out["x"]["minimum"],a[0]) and np.array_equal(out["x"]["maximum"],a[-1])
    invalid(lambda: m.infer_episode_schema([{"x":signal(a)},{"x":signal(a)},{"y":signal([[0]])}]))

TESTS=[("Required and optional signals","public",required_optional),("Empty episode changes presence","public",empty_episode),("Empty collection","public",empty_collection),
       ("Physical metadata consistency","hidden",physical_consistency),("Malformed bounded contract","hidden",malformed),
       ("Noncontiguous inputs and independent outputs","hidden",storage_and_noncontiguous),("Declared scalar budget","hidden",realistic_budget)]

