from copy import deepcopy


def invalid(call):
    try: call()
    except ValueError: return
    raise AssertionError("Expected ValueError")


def example(m):
    events=[(900,"arm","model_error"),(950,"arm","safety_stop"),(920,"camera","sensor_stale"),(800,"camera","model_error"),(980,"planner","deadline_miss")]
    assert m.triage_events(events,1000,150)==[("arm","P0",2,900),("camera","P1",1,920),("planner","P1",1,980)]


def cutoff_duplicates(m):
    events=[(90,"b","model_error"),(100,"a","model_error"),(90,"b","model_error"),(89,"a","safety_stop")]
    assert m.triage_events(events,100,10)==[("b","P2",2,90),("a","P2",1,100)]


def empty_and_zero(m):
    assert m.triage_events([],0,0)==[]
    assert m.triage_events([(0,"a","safety_stop")],1,0)==[]
    assert m.triage_events([(1,"a","safety_stop")],1,0)==[("a","P0",1,1)]


def sort_ties(m):
    events=[(10,"b","sensor_stale"),(10,"a","deadline_miss"),(9,"z","sensor_stale"),(11,"urgent","safety_stop")]
    expected=[("urgent","P0",1,11),("z","P1",1,9),("a","P1",1,10),("b","P1",1,10)]
    assert m.triage_events(events,11,100)==expected
    assert m.triage_events(list(reversed(events)),11,100)==expected


def invalid_records(m):
    for events in [(),[(1,"a","model_error")],[[0,"a","model_error"]],[(0,"A","model_error")],[(0,"a",[])],[(True,"a","safety_stop")],[(-1,"a","safety_stop")],[(0,"a","unknown")],[(0,[],"model_error")],[(0,"a"*65,"model_error")]]:
        invalid(lambda: m.triage_events(events,0,0))
    for now,window in [(False,0),(0,False),(-1,0),(0,10**1000)]:
        invalid(lambda: m.triage_events([],now,window))
    invalid(lambda: m.triage_events([(0,"a","model_error")]*100001,0,0))


def large_clock_and_storage(m):
    now=2**63-1;args=[(now-1,"a","model_error"),(now,"a","deadline_miss")];saved=deepcopy(args)
    out=m.triage_events(args,now,1);assert out==[("a","P1",2,now-1)] and args==saved
    assert type(out) is list and type(out[0]) is tuple and all(type(v) is int for v in out[0][2:])
    assert m.triage_events([(0,"a","model_error")]*100000,0,0)==[("a","P2",100000,0)]


TESTS=[("Grouped priority queue","public",example),("Closed window and duplicates","public",cutoff_duplicates),("Empty and zero-width windows","public",empty_and_zero),
       ("Priority time and ID ties","hidden",sort_ties),("Malformed or future records","hidden",invalid_records),
       ("Large clocks counts and storage","hidden",large_clock_and_storage)]
