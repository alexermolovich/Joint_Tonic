from copy import deepcopy
from itertools import permutations
import random


def expect_value_error(call):
    try:
        call()
    except ValueError:
        return
    raise AssertionError("Expected ValueError")


def newly_ready(m):
    result = m.schedule_pipeline(["z-audit", "decode", "train"], [("decode", "train")])
    assert type(result) is list and result == ["decode", "train", "z-audit"]


def merge_inputs(m):
    assert m.schedule_pipeline(["report", "labels", "fit", "images"],
                               [("images", "fit"), ("labels", "fit"), ("fit", "report")]
                               ) == ["images", "labels", "fit", "report"]


def empty(m):
    assert m.schedule_pipeline([], []) == []


def duplicates_and_independence(m):
    args = (["c", "b", "a"], [("a", "b"), ("a", "b")])
    before = deepcopy(args)
    result = m.schedule_pipeline(*args)
    assert result == ["a", "b", "c"] and args == before
    result.append("extra")
    assert args == before


def cyclic_graphs(m):
    for nodes, edges in [
        (["a"], [("a", "a")]),
        (["a", "b"], [("a", "b"), ("b", "a")]),
        (["a", "b", "c"], [("b", "c"), ("c", "b")]),
    ]:
        expect_value_error(lambda nodes=nodes, edges=edges: m.schedule_pipeline(nodes, edges))


def exhaustive_small_orders(m):
    rng = random.Random(20261113)
    for _ in range(5):
        nodes = ["a", "b", "c", "d", "e", "f"]
        hidden_order = rng.sample(nodes, len(nodes))
        edges = [(hidden_order[i], hidden_order[j]) for i in range(6)
                 for j in range(i + 1, 6) if rng.random() < 0.35]
        valid = []
        for candidate in permutations(nodes):
            positions = {node: i for i, node in enumerate(candidate)}
            if all(positions[a] < positions[b] for a, b in edges):
                valid.append(candidate)
        assert m.schedule_pipeline(rng.sample(nodes, len(nodes)), edges) == list(min(valid))


def invalid_inputs(m):
    invalid = [
        (("a",), []), (["a"], ()), (["a", "a"], []), ([False], []),
        (["A"], []), (["a" * 65], []), (["a"], [["a", "a"]]),
        (["a"], [("a",)]), (["a"], [("a", "missing")]),
        (["a"], [("a", [])]),
    ]
    for args in invalid:
        expect_value_error(lambda args=args: m.schedule_pipeline(*args))
    expect_value_error(lambda: m.schedule_pipeline(["n" + str(i) for i in range(10001)], []))
    expect_value_error(lambda: m.schedule_pipeline(["a"], [("a", "a")] * 50001))


def long_pipeline(m):
    nodes = ["stage" + str(i).zfill(5) for i in range(6000)]
    edges = list(zip(nodes, nodes[1:]))
    assert m.schedule_pipeline(list(reversed(nodes)), edges) == nodes


TESTS = [
    ("Newly ready lexical priority", "public", newly_ready),
    ("Two-input artifact merge", "public", merge_inputs),
    ("Empty pipeline", "public", empty),
    ("Duplicates and input independence", "hidden", duplicates_and_independence),
    ("Cycles including disconnected work", "hidden", cyclic_graphs),
    ("Independent exhaustive order oracle", "hidden", exhaustive_small_orders),
    ("Declared invalid inputs and limits", "hidden", invalid_inputs),
    ("Deep dependency pipeline", "hidden", long_pipeline),
]
