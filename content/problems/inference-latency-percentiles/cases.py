import math


def check_result(actual, expected):
    assert type(actual) is dict and set(actual) == set(expected)
    for key, value in expected.items():
        if value is None:
            assert actual[key] is None
        else:
            assert type(actual[key]) is float
            assert math.isclose(actual[key], value, rel_tol=0, abs_tol=1e-9)


def invalid(call):
    try:
        call()
    except ValueError:
        return
    raise AssertionError("Expected ValueError")


def long_tail(m):
    check_result(m.latency_percentiles([0, 10000000, 20000000, 30000000, 40000000],
                                      [1000000, 12000000, 23000000, 34000000, 60000000]),
                 {"p50_ms": 3., "p90_ms": 20., "p99_ms": 20.})


def even_count(m):
    check_result(m.latency_percentiles([0] * 4, [1000000, 4000000, 2000000, 3000000]),
                 {"p50_ms": 2., "p90_ms": 4., "p99_ms": 4.})


def empty(m):
    check_result(m.latency_percentiles([], []), {"p50_ms": None, "p90_ms": None, "p99_ms": None})


def clock_precision(m):
    clock = 2**63 - 1
    check_result(m.latency_percentiles([clock, clock - 1, clock - 5], [clock] * 3),
                 {"p50_ms": .000001, "p90_ms": .000005, "p99_ms": .000005})


def rank_and_pairing(m):
    check_result(m.latency_percentiles([100000000] * 10,
                                      [100000000 + i * 1000000 for i in range(10, 0, -1)]),
                 {"p50_ms": 5., "p90_ms": 9., "p99_ms": 10.})
    check_result(m.latency_percentiles([100, 0, 50], [101, 10, 52]),
                 {"p50_ms": .000002, "p90_ms": .000010, "p99_ms": .000010})


def singleton_and_extremes(m):
    check_result(m.latency_percentiles([123], [123]), {"p50_ms": 0., "p90_ms": 0., "p99_ms": 0.})
    check_result(m.latency_percentiles([0], [10**12]),
                 {"p50_ms": 1e6, "p90_ms": 1e6, "p99_ms": 1e6})


def invalid_inputs(m):
    for args in [
        ((), []), ([], ()), ([0], []), ([True], [1]), ([0.], [1]),
        ([0], [None]), ([-1], [0]), ([0], [2**63]), ([2], [1]),
        ([0], [10**12 + 1]), ([0], ["1"]), ([[0]], [1]),
    ]:
        invalid(lambda args=args: m.latency_percentiles(*args))
    invalid(lambda: m.latency_percentiles([0] * 1000001, [0] * 1000001))


def independence_and_scale(m):
    starts = [7, 3, 9]
    ends = [8, 8, 9]
    expected_starts, expected_ends = starts.copy(), ends.copy()
    m.latency_percentiles(starts, ends)
    assert starts == expected_starts and ends == expected_ends
    check_result(m.latency_percentiles([0] * 100000, [1000] * 100000),
                 {"p50_ms": .001, "p90_ms": .001, "p99_ms": .001})


TESTS = [
    ("Long-tail trace", "public", long_tail),
    ("Even-count nearest rank", "public", even_count),
    ("Empty measured trace", "public", empty),
    ("Large-origin nanosecond precision", "hidden", clock_precision),
    ("Ranks and original request pairing", "hidden", rank_and_pairing),
    ("Singleton and duration boundary", "hidden", singleton_and_extremes),
    ("Declared invalid timestamps", "hidden", invalid_inputs),
    ("Input independence and realistic trace", "hidden", independence_and_scale),
]
