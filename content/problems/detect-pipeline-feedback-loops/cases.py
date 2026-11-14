from copy import deepcopy
import random


def invalid(call):
    try:
        call()
    except ValueError:
        return
    raise AssertionError("Expected ValueError")


def branch(m):
    nodes = ["dataset", "train", "policy", "logger", "dashboard"]
    edges = [("dataset","train"),("train","policy"),("policy","logger"),("logger","dataset"),("logger","dashboard")]
    assert m.feedback_groups(nodes, edges) == [["dataset","logger","policy","train"]]


def separate(m):
    assert m.feedback_groups(["monitor","b","a","isolated"],[("b","a"),("a","b"),("monitor","monitor"),("a","b")]) == [["a","b"],["monitor"]]


def empty(m):
    assert m.feedback_groups([], []) == []
    assert m.feedback_groups(["a","b"], [("a","b")]) == []


def closure_oracle(m):
    rng = random.Random(20261113)
    for _ in range(12):
        nodes = [chr(97+i) for i in range(7)]
        edges = [(a,b) for a in nodes for b in nodes if rng.random() < .16]
        reachable = {(a,a) for a in nodes} | set(edges)
        for k in nodes:
            for a in nodes:
                for b in nodes:
                    if (a,k) in reachable and (k,b) in reachable:
                        reachable.add((a,b))
        groups = {tuple(n for n in nodes if (n,a) in reachable and (a,n) in reachable) for a in nodes}
        expected = sorted([list(group) for group in groups if len(group)>1 or (group[0],group[0]) in edges])
        assert m.feedback_groups(nodes, edges) == expected


def invalid_graph(m):
    for nodes,edges in [((),[]),([],()),(["a","a"],[]),(["A"],[]),(["a"],[("a","missing")]),(["a"],[["a","a"]]),(["a"],[("a",[])]),([False],[]),(["a"*65],[])]:
        invalid(lambda: m.feedback_groups(nodes,edges))
    invalid(lambda: m.feedback_groups(["a"],[("a","a")]*50001))
    invalid(lambda: m.feedback_groups(["n"+str(i) for i in range(10001)],[]))


def storage(m):
    nodes,edges=["b","a","c"],[("b","a"),("a","b"),("c","a")]
    saved=deepcopy((nodes,edges));out=m.feedback_groups(nodes,edges)
    assert type(out) is list and all(type(g) is list for g in out)
    assert out==[["a","b"]] and (nodes,edges)==saved
    out[0].append("new");assert (nodes,edges)==saved


def long_graph(m):
    nodes=["n"+str(i).zfill(5) for i in range(8000)]
    edges=list(zip(nodes[:-1],nodes[1:]))+[(nodes[-1],nodes[0])]
    assert m.feedback_groups(nodes,edges)==[nodes]


TESTS=[("Feedback and consumer","public",branch),("Separate cycles","public",separate),("Empty and acyclic","public",empty),
       ("Independent reachability oracle","hidden",closure_oracle),("Malformed and bounded graph","hidden",invalid_graph),
       ("Output storage and preservation","hidden",storage),("Deep cyclic graph","hidden",long_graph)]
