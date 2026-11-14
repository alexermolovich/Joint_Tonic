from copy import deepcopy
import numpy as np


BOUNDS = {"mass_kg": (1., 9.), "friction": (.25, 1.),
          "delay_ticks": (0, 3), "gain_scale": (.5, 2.)}


def invalid(call):
    try:
        call()
    except ValueError:
        return
    raise AssertionError("Expected ValueError")


def check_output(actual, expected):
    assert type(actual) is dict and set(actual) == set(expected)
    for key, values in expected.items():
        array = actual[key]
        assert isinstance(array, np.ndarray) and array.shape == (len(values),)
        assert array.dtype == (np.int64 if key == "delay_ticks" else np.float64)
        if key == "delay_ticks":
            assert np.array_equal(array, values)
        else:
            np.testing.assert_allclose(array, values, rtol=1e-12, atol=1e-12)


def endpoint_and_midpoint(m):
    out = m.sample_dynamics(np.array([[0.] * 4, [.5] * 4]), deepcopy(BOUNDS), .01)
    check_output(out, {"mass_kg": [1., 3.], "friction": [.25, .5],
                       "delay_ticks": [0, 2], "gain_scale": [.5, 1.], "delay_s": [0., .02]})


def fixed_ranges(m):
    bounds = {"mass_kg": (2., 2.), "friction": (.5, .5),
              "delay_ticks": (1, 1), "gain_scale": (1., 1.)}
    check_output(m.sample_dynamics(np.array([[.75, .25, .9, .1]]), bounds, .02),
                 {"mass_kg": [2.], "friction": [.5], "delay_ticks": [1],
                  "gain_scale": [1.], "delay_s": [.02]})


def empty(m):
    out = m.sample_dynamics(np.empty((0, 4)), deepcopy(BOUNDS), .01)
    check_output(out, {key: [] for key in ("mass_kg", "friction", "delay_ticks", "gain_scale", "delay_s")})


def bucket_boundaries(m):
    draws = np.zeros((5, 4))
    draws[:, 2] = [0., .25, .5, .75, np.nextafter(1., 0.)]
    result = m.sample_dynamics(draws, deepcopy(BOUNDS), .01)
    assert np.array_equal(result["delay_ticks"], [0, 1, 2, 3, 3])


def alternate_formula_and_independence(m):
    rng = np.random.default_rng(20261113)
    draws = rng.random((50, 8))[:, ::2]
    before = draws.copy()
    bounds = deepcopy(BOUNDS)
    result = m.sample_dynamics(draws, bounds, .02)
    for key, column in [("mass_kg", 0), ("friction", 1), ("gain_scale", 3)]:
        lo, hi = bounds[key]
        np.testing.assert_allclose(result[key], lo * (hi / lo) ** draws[:, column], rtol=1e-12, atol=1e-12)
    assert np.array_equal(draws, before) and bounds == BOUNDS
    for value in result.values():
        assert not np.shares_memory(value, draws)
    np.testing.assert_allclose(result["delay_s"], result["delay_ticks"] * .02, rtol=1e-12, atol=1e-12)


def invalid_draws(m):
    for draws in [[], np.zeros((1, 4), dtype=np.float32), np.zeros(4),
                  np.zeros((1, 3)), np.zeros((10001, 4)),
                  np.full((1, 4), 1.), np.full((1, 4), -.1),
                  np.full((1, 4), np.nan), np.full((1, 4), np.inf)]:
        invalid(lambda draws=draws: m.sample_dynamics(draws, deepcopy(BOUNDS), .01))


def invalid_bounds_and_time(m):
    for key, interval in [("mass_kg", (0., 2.)), ("friction", (.5, .1)),
                          ("gain_scale", (1., np.inf)), ("delay_ticks", (0., 3.)),
                          ("delay_ticks", (False, 3)), ("mass_kg", [1., 9.]),
                          ("gain_scale", (1.,)), ("mass_kg", (1e-10, 2.))]:
        bounds = deepcopy(BOUNDS)
        bounds[key] = interval
        invalid(lambda bounds=bounds: m.sample_dynamics(np.empty((0, 4)), bounds, .01))
    for bounds in [{}, {**BOUNDS, "extra": (1, 2)}, []]:
        invalid(lambda bounds=bounds: m.sample_dynamics(np.zeros((1, 4)), bounds, .01))
    for dt in [True, 0., 1.1, float("nan"), float("inf"), "0.1", np.float64(.01), 10**1000]:
        invalid(lambda dt=dt: m.sample_dynamics(np.zeros((1, 4)), deepcopy(BOUNDS), dt))


def large_batch(m):
    draws = np.full((10000, 4), .5)
    result = m.sample_dynamics(draws, deepcopy(BOUNDS), .01)
    assert all(value.shape == (10000,) for value in result.values())
    assert np.all(result["delay_ticks"] == 2)
    np.testing.assert_allclose(result["mass_kg"], 3., rtol=1e-12, atol=1e-12)


TESTS = [
    ("Lower endpoints and log midpoints", "public", endpoint_and_midpoint),
    ("Fixed physical configuration", "public", fixed_ranges),
    ("Empty episode batch", "public", empty),
    ("Discrete delay bucket boundaries", "hidden", bucket_boundaries),
    ("Independent power formula and no mutation", "hidden", alternate_formula_and_independence),
    ("Invalid unit draws and shapes", "hidden", invalid_draws),
    ("Invalid physical bounds and control interval", "hidden", invalid_bounds_and_time),
    ("Maximum episode batch", "hidden", large_batch),
]
