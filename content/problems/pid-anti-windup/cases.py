import numpy as np
from numpy.testing import assert_allclose


def positive_saturation(m):
    assert_allclose(m.pid_step(1, 1, 0, .1, (2, 1, 0), (-1, 1)), (1, 0, 0))


def feasible(m):
    assert_allclose(m.pid_step(.2, .2, 0, .1, (2, 1, 0), (-1, 1)), (.42, .02, 0))


def unwind(m):
    assert_allclose(m.pid_step(-.5, -.5, 3, 1, (0, 1, 0), (-1, 1)), (1, 2.5, 0))
    assert_allclose(m.pid_step(.5, .5, -3, 1, (0, 1, 0), (-1, 1)), (-1, -2.5, 0))


def negative_and_equality(m):
    assert_allclose(m.pid_step(-1, -1, 0, .1, (2, 1, 0), (-1, 1)), (-1, 0, 0))
    assert_allclose(m.pid_step(1, 1, 0, 1, (0, 1, 0), (-1, 1)), (1, 1, 0))
    assert_allclose(m.pid_step(-1, -1, 0, 1, (0, 1, 0), (-1, 1)), (-1, -1, 0))


def derivative_and_recompute(m):
    # Candidate saturation rejects I=1.2, leaving command .4 rather than 1.
    assert_allclose(m.pid_step(1, 0, .2, 1, (0, 2, 0), (-1, 1)), (.4, .2, 1))
    assert_allclose(m.pid_step(.5, .25, 0, .25, (0, 0, .2), (-1, 1)), (.2, .125, 1))
    assert_allclose(m.pid_step(0, 1, 5, .5, (0, .1, .2), (-1, 1)), (.1, 5, -2))


def invalid(m):
    good = [1, 1, 0, .1, (2, 1, 0), (-1, 1)]
    bads = [(3, 0), (3, -1), (4, (1, -1, 0)), (4, (1, 2)), (4, (1, 2, 3, 4)),
            (4, ((1,), (2,), (3,))), (5, (1, 1)), (5, (2, 1)), (5, (1,)),
            (4, (True, 1, 0)), (5, (False, 1)), (3, np.array(.1))]
    for i, value in bads:
        args = good.copy(); args[i] = value
        with np.testing.assert_raises(ValueError):
            m.pid_step(*args)
    for i in range(6):
        for bad in [np.nan, np.inf, -np.inf, "1", True, np.bool_(True), 1j, 1000001]:
            args = good.copy()
            args[i] = (bad, 1, 0) if i == 4 else (-1, bad) if i == 5 else bad
            with np.testing.assert_raises(ValueError):
                m.pid_step(*args)
    with np.testing.assert_raises(ValueError):
        m.pid_step(1, -1, 0, 1e-320, (1, 1, 1), (-1, 1))


def numpy_scalars_and_trajectory(m):
    gains = np.array([2., 1., 0.]); bounds = np.array([-1., 1.])
    state = 0.
    for _ in range(1000):
        out = m.pid_step(np.float32(1), np.float64(1), state, np.float64(.01), gains, bounds)
        assert all(type(x) is float for x in out)
        assert out == (1., 0., 0.)
        state = out[1]
    assert_allclose(gains, [2, 1, 0]); assert_allclose(bounds, [-1, 1])


TESTS = [("Upper saturation", "public", positive_saturation), ("Feasible effort", "public", feasible),
         ("Unwind while saturated", "public", unwind), ("Lower limit and exact equality", "hidden", negative_and_equality),
         ("Derivative and recomputed effort", "hidden", derivative_and_recompute), ("Invalid scalar contracts", "hidden", invalid),
         ("Repeated control steps and numpy scalars", "hidden", numpy_scalars_and_trajectory)]
