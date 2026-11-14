"""Original robot-data fixtures; CC0-1.0."""
import copy


def _schema():
    return {"signals": {"joints": {"shape": [2], "dtype": "float",
            "unit": "rad", "frame": "robot", "min": -3, "max": 3}}}


def _episode():
    return {"timestamps": [0., 0.1], "signals": {"joints": {
        "values": [[0., 1.], [1., 2.]], "unit": "rad", "frame": "robot"}}}


def _issue(path, code, episode=0):
    return {"episode": episode, "path": path, "code": code}


def valid(m):
    assert m.validate_episodes([_episode()], _schema()) == []


def missing(m):
    e = _episode()
    e["signals"] = {}
    assert m.validate_episodes([e], _schema()) == [_issue("signals.joints", "missing")]


def range_and_time(m):
    e = _episode()
    e["timestamps"][1] = 0.
    e["signals"]["joints"]["values"][1][0] = 4.
    assert m.validate_episodes([e], _schema()) == [
        _issue("signals.joints.values[1]", "range"),
        _issue("timestamps[1]", "nonmonotonic")]


def optional_extra(m):
    schema = _schema()
    schema["signals"]["optional"] = {"shape": [], "dtype": "bool", "required": False}
    schema["allow_extra_signals"] = False
    e = _episode()
    e["signals"]["rogue"] = {"values": [1, 2]}
    assert m.validate_episodes([e], schema) == [_issue("signals.rogue", "unexpected")]


def row_error_hierarchy(m):
    rows = [[1.], ["bad", "bad"], [float("inf"), 0]]
    e = _episode()
    e["timestamps"] = [0., 1., 2.]
    e["signals"]["joints"]["values"] = rows
    assert m.validate_episodes([e], _schema()) == [
        _issue("signals.joints.values[0]", "shape"),
        _issue("signals.joints.values[1]", "dtype"),
        _issue("signals.joints.values[2]", "nonfinite")]


def metadata(m):
    e = _episode()
    e["signals"]["joints"]["unit"] = "degrees"
    del e["signals"]["joints"]["frame"]
    assert m.validate_episodes([e], _schema()) == [
        _issue("signals.joints.frame", "metadata"),
        _issue("signals.joints.unit", "metadata")]


def missing_fraction(m):
    e = _episode()
    e["signals"]["joints"]["values"][1] = None
    s = _schema()
    s["signals"]["joints"]["max_missing_fraction"] = 0.5
    assert m.validate_episodes([e], s) == []
    s["signals"]["joints"]["max_missing_fraction"] = 0.49
    assert m.validate_episodes([e], s) == [_issue("signals.joints.values", "missing_fraction")]


def scalar_dtype(m):
    schema = {"signals": {"enabled": {"shape": [], "dtype": "bool"}}}
    e = {"timestamps": [0., 1.], "signals": {"enabled": {"values": [True, 1]}}}
    assert m.validate_episodes([e], schema) == [_issue("signals.enabled.values[1]", "dtype")]


def containers_and_empty(m):
    result = m.validate_episodes([None, {"timestamps": None},
        {"timestamps": [], "signals": {}},
        {"timestamps": [0.], "signals": {"joints": {"unit": "rad", "frame": "robot", "values": []}}}], _schema())
    assert result == [
        _issue("", "type", 0), _issue("timestamps", "type", 1),
        _issue("signals.joints", "missing", 2), _issue("timestamps", "empty", 2),
        _issue("signals.joints.values", "length", 3)]


def nonfinite_and_immutable(m):
    e = _episode()
    e["timestamps"] = [float("inf"), 1.]
    before = copy.deepcopy(e)
    assert m.validate_episodes([e], _schema()) == [_issue("timestamps[0]", "nonfinite")]
    assert e == before


def invalid_schema(m):
    for s in ({}, {"signals": {"x": {"shape": [0], "dtype": "float"}}},
              {"signals": {"x": {"shape": [], "dtype": "complex"}}},
              {"signals": {}, "allow_extra_signals": "yes"}):
        try:
            m.validate_episodes([], s)
        except ValueError:
            continue
        raise AssertionError("invalid schema must raise ValueError")


TESTS = [
    ("Valid multimodal contract", "public", valid),
    ("Missing required signal", "public", missing),
    ("Joint range and repeated timestamp", "public", range_and_time),
    ("Optional and extra signals", "hidden", optional_extra),
    ("Shape before dtype before value checks", "hidden", row_error_hierarchy),
    ("Physical metadata mismatch", "hidden", metadata),
    ("Missing-fraction equality boundary", "hidden", missing_fraction),
    ("Scalar boolean dtype", "hidden", scalar_dtype),
    ("Malformed and empty episode containers", "hidden", containers_and_empty),
    ("Nonfinite time and immutability", "hidden", nonfinite_and_immutable),
    ("Schema is a validated caller contract", "hidden", invalid_schema),
]
