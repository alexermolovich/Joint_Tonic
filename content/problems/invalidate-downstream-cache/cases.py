from copy import deepcopy


def invalid(call):
    try:
        call()
    except ValueError:
        return
    raise AssertionError("Expected ValueError")


def uncached_intermediate(m):
    graph = {"raw": [], "features": ["raw"], "model": ["features"],
             "report": ["model"], "lookup": []}
    assert m.invalidated_artifacts(graph, ["raw"], ["model", "report", "lookup"]) == ["model", "report"]


def cached_root(m):
    assert m.invalidated_artifacts({"raw": [], "model": ["raw"], "report": ["model"]},
                                  ["model"], ["raw", "model", "report"]) == ["model", "report"]


def empty_inputs(m):
    assert m.invalidated_artifacts({}, [], []) == []
    assert m.invalidated_artifacts({"raw": []}, [], ["raw"]) == []
    assert m.invalidated_artifacts({"raw": []}, ["raw"], []) == []


def duplicates_and_fan_in(m):
    graph = {"left": [], "right": [], "merged": ["left", "right", "left"], "report": ["merged"]}
    assert m.invalidated_artifacts(graph, ["right", "right"], ["report", "merged", "merged"]) == ["merged", "report"]
    assert m.invalidated_artifacts(graph, ["merged"], ["left", "right"]) == []


def invalid_graphs(m):
    for graph in [{"a": ["a"]}, {"a": ["b"], "b": ["a"], "unused": []}]:
        invalid(lambda graph=graph: m.invalidated_artifacts(graph, [], []))
    for args in [
        ([], [], []), ({"A": []}, [], []), ({"a": ()}, [], []),
        ({"a": ["missing"]}, [], []), ({"a": [[]]}, [], []),
        ({"a": []}, ["missing"], []), ({"a": []}, [], ["missing"]),
        ({"a": []}, (), []), ({"a": []}, [], ()),
        ({"a": []}, [False], []), ({1: []}, [], []),
    ]:
        invalid(lambda args=args: m.invalidated_artifacts(*args))


def limits(m):
    invalid(lambda: m.invalidated_artifacts({"n" + str(i): [] for i in range(10001)}, [], []))
    invalid(lambda: m.invalidated_artifacts({"a": [], "b": ["a"] * 50001}, [], []))
    invalid(lambda: m.invalidated_artifacts({"a": []}, ["a"] * 10001, []))
    invalid(lambda: m.invalidated_artifacts({"a": []}, [], ["a"] * 10001))


def immutable(m):
    args = ({"a": [], "b": ["a"], "c": ["b"]}, ["a"], ["c", "a"])
    before = deepcopy(args)
    out = m.invalidated_artifacts(*args)
    assert type(out) is list and out == ["a", "c"] and args == before
    out.append("new")
    assert args == before


def deep_uncached_path(m):
    nodes = ["a" + str(i).zfill(5) for i in range(6000)]
    graph = {node: ([] if i == 0 else [nodes[i - 1]]) for i, node in enumerate(nodes)}
    assert m.invalidated_artifacts(graph, [nodes[0]], [nodes[-1]]) == [nodes[-1]]


TESTS = [
    ("Traverse an uncached intermediate", "public", uncached_intermediate),
    ("Invalidate a changed cached root", "public", cached_root),
    ("Empty change and cache sets", "public", empty_inputs),
    ("Duplicate parents and merged inputs", "hidden", duplicates_and_fan_in),
    ("Invalid references and disconnected cycles", "hidden", invalid_graphs),
    ("Declared input limits", "hidden", limits),
    ("Input independence and lexical output", "hidden", immutable),
    ("Deep uncached dependency chain", "hidden", deep_uncached_path),
]
