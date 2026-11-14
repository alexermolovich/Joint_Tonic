from copy import deepcopy
import numpy as np

def invalid(call):
    try:
        call()
    except ValueError:
        return
    raise AssertionError("Expected ValueError")

def critical_and_warning(m):
    assert m.data_anomaly_gate(["camera","joints"],["camera","joints"],[("camera","brightness","warning"),("joints","unit","critical")])=={"blocking":[("joints","unit")],"warnings":[("camera","brightness")],"missing_sources":[],"blocked":True}

def missing_coverage(m):
    assert m.data_anomaly_gate(["joints","camera","camera"],["joints"],[])=={"blocking":[],"warnings":[],"missing_sources":["camera"],"blocked":True}

def passing(m):
    assert m.data_anomaly_gate(["x"],["x"],[("x","light","warning")])=={"blocking":[],"warnings":[("x","light")],"missing_sources":[],"blocked":False}

def duplicate_and_extra(m):
    rows=[("b","unit","critical"),("a","noise","warning"),("b","unit","critical")]
    args=(["a","a"],["b","a","b"],rows);saved=deepcopy(args)
    out=m.data_anomaly_gate(*args)
    assert out=={"blocking":[("b","unit")],"warnings":[("a","noise")],"missing_sources":[],"blocked":True}
    assert args==saved and type(out["blocked"]) is bool
    invalid(lambda: m.data_anomaly_gate(["a"],["a"],[("a","x","warning"),("a","x","critical")]))

def malformed(m):
    good=(["a"],["a"],[])
    for bad in [None,(),[],["Bad"],[1]]:
        invalid(lambda: m.data_anomaly_gate(bad,good[1],[]))
    for bad in [None,(),["Bad"],[1]]:
        invalid(lambda: m.data_anomaly_gate(good[0],bad,[]))
    for rows in [None,(),[["a","x","critical"]],[("b","x","critical")],[("a","Bad","critical")],[("a","x","other")],[("a","x",np.array(["critical"]))],[("a","x")]]:
        invalid(lambda: m.data_anomaly_gate(*good[:2],rows))
    invalid(lambda: m.data_anomaly_gate(["a"]*10001,["a"],[]))
    invalid(lambda: m.data_anomaly_gate(["a"],["a"]*10001,[]))

def scale_and_order(m):
    sources=[f"s{i}" for i in range(10000)]
    rows=[(source,"noise","warning") for source in reversed(sources)]*5
    out=m.data_anomaly_gate(sources,sources,rows)
    assert out=={"blocking":[],"warnings":sorted((source,"noise") for source in sources),"missing_sources":[],"blocked":False}
    invalid(lambda: m.data_anomaly_gate(sources,sources,rows+[rows[0]]))

TESTS=[("Critical evidence preserves warnings","public",critical_and_warning),("Missing validation blocks","public",missing_coverage),("Warning alone passes","public",passing),
       ("Deduplication extra sources and conflicts","hidden",duplicate_and_extra),("Invalid schema and sources","hidden",malformed),("Declared anomaly budget and stable ordering","hidden",scale_and_order)]

