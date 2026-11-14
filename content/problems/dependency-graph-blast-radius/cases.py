from copy import deepcopy


def expect_value_error(call):
    try:
        call()
    except ValueError:
        return
    raise AssertionError("Expected ValueError")


def calibration(m):
    result = m.blast_radius(
        ["calib", "images", "features", "policy", "monitor"],
        [("calib", "features"), ("images", "features"),
         ("features", "policy"), ("policy", "monitor")], ["calib"])
    assert type(result) is list
    assert result == ["features", "monitor", "policy"]


def feedback(m):
    assert m.blast_radius(
        ["data", "policy", "log", "dashboard"],
        [("data", "policy"), ("policy", "log"),
         ("log", "data"), ("log", "dashboard")], ["policy", "policy"]
    ) == ["dashboard", "data", "log"]


def empty(m):
    assert m.blast_radius([], [], []) == []
    assert m.blast_radius(["camera"], [], []) == []


def overlapping_roots(m):
    nodes = ["sensor", "features", "model", "report"]
    edges = [("sensor", "features"), ("features", "model"), ("model", "report")]
    assert m.blast_radius(nodes, edges, ["sensor", "model"]) == ["features", "report"]


def repeated_edges_and_self_loop(m):
    assert m.blast_radius(["a", "b", "c"],
                         [("a", "a"), ("a", "b"), ("a", "b"), ("b", "a")],
                         ["a", "a"]) == ["b"]


def immutability(m):
    args = (["sensor", "model", "unrelated"], [("sensor", "model")], ["sensor"])
    before = deepcopy(args)
    result = m.blast_radius(*args)
    assert args == before and result == ["model"]
    result.append("extra")
    assert args == before


def invalid_inputs(m):
    invalid = [
        (("a",), [], []), (["a"], (), []), (["a"], [], ()),
        (["a", "a"], [], []), (["A"], [], []), ([1], [], []),
        (["a"], [["a", "a"]], []), (["a"], [("a",)], []),
        (["a"], [("a", "missing")], []), (["a"], [("a", [])], []),
        (["a"], [], ["missing"]), (["a"], [], [[]]),
        (["a" * 65], [], []), (["a b"], [], []),
    ]
    for args in invalid:
        expect_value_error(lambda args=args: m.blast_radius(*args))


def bounds(m):
    expect_value_error(lambda: m.blast_radius(["n" + str(i) for i in range(10001)], [], []))
    expect_value_error(lambda: m.blast_radius(["a"], [("a", "a")] * 50001, []))
    expect_value_error(lambda: m.blast_radius(["a"], [], ["a"] * 10001))


def deep_cycle(m):
    nodes = ["n" + str(i).zfill(5) for i in range(6000)]
    edges = list(zip(nodes, nodes[1:])) + [(nodes[-1], nodes[0])]
    assert m.blast_radius(nodes, edges, [nodes[0]]) == nodes[1:]


TESTS = [
    ("Calibration fan-out", "public", calibration),
    ("Feedback cycle", "public", feedback),
    ("Empty graph and change set", "public", empty),
    ("Overlapping changed roots", "hidden", overlapping_roots),
    ("Repeated edges and self-loop", "hidden", repeated_edges_and_self_loop),
    ("Input and output independence", "hidden", immutability),
    ("Declared invalid inputs", "hidden", invalid_inputs),
    ("Declared size bounds", "hidden", bounds),
    ("Deep cyclic dependency chain", "hidden", deep_cycle),
]
