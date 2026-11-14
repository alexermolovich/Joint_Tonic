import numpy as np
from numpy.testing import assert_array_equal


def one_step(m):
    result = m.rt1_attention_mask(1, 2, 2)
    assert_array_equal(result, [[1, 0, 0, 0], [1, 1, 0, 0], [1, 1, 0, 0], [1, 1, 0, 0]])
    assert result.dtype == np.bool_ and result.shape == (4, 4)


def two_steps(m):
    assert_array_equal(m.rt1_attention_mask(2, 1, 1), [[1, 0, 0, 0], [1, 0, 0, 0], [1, 1, 1, 0], [1, 0, 1, 0]])


def minimum(m):
    assert_array_equal(m.rt1_attention_mask(1, 1, 1), [[1, 0], [1, 0]])


def oracle(m):
    for t, v, a in [(3, 2, 1), (2, 1, 3), (1, 7, 2), (4, 3, 2)]:
        labels = [kind for _ in range(t) for kind in ["visual"] * v + ["action"] * a]
        expected = [[j <= i and not (qi == kj == "action") for j, kj in enumerate(labels)] for i, qi in enumerate(labels)]
        assert_array_equal(m.rt1_attention_mask(t, v, a), expected)


def largest(m):
    result = m.rt1_attention_mask(256, 3, 1)
    assert result.shape == (1024, 1024) and result.dtype == np.bool_
    assert not np.triu(result, 1).any()
    assert not result[3::4, 3::4].any()
    assert result[4, 3] and result[1022, 1022]


def fresh(m):
    first = m.rt1_attention_mask(1, 1, 1)
    first[:] = False
    second = m.rt1_attention_mask(1, 1, 1)
    assert second[0, 0] and not np.shares_memory(first, second)


def expect(error, call):
    try:
        call()
    except error:
        return
    raise AssertionError("expected " + error.__name__)


def invalid_types(m):
    for value in (True, False, 1., "1", np.int64(1), None):
        for index in range(3):
            args = [1, 1, 1]; args[index] = value
            expect(TypeError, lambda args=args: m.rt1_attention_mask(*args))


def invalid_sizes(m):
    for value in (0, -1, 1025):
        for index in range(3):
            args = [1, 1, 1]; args[index] = value
            expect(ValueError, lambda args=args: m.rt1_attention_mask(*args))
    expect(ValueError, lambda: m.rt1_attention_mask(513, 1, 1))


TESTS = [
    ("One timestep", "public", one_step),
    ("Visual queries and earlier placeholders", "public", two_steps),
    ("Smallest sequence", "hidden", minimum),
    ("Independent slot-label oracle", "hidden", oracle),
    ("Largest supported sequence", "hidden", largest),
    ("Fresh result storage", "hidden", fresh),
    ("Strict integer types", "hidden", invalid_types),
    ("Dimension bounds", "hidden", invalid_sizes),
]
