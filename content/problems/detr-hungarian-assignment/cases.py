import itertools
import numpy as np


def invalid(call, error=ValueError):
    try:
        call()
    except error:
        return
    raise AssertionError("Expected " + error.__name__)


def checked(module, cost, optimum):
    before = cost.copy()
    out = module.match_queries(cost)
    assert isinstance(out, np.ndarray) and out.dtype == np.int64 and out.shape == (cost.shape[1],)
    assert ((out >= 0) & (out < cost.shape[0])).all()
    assert len(set(out.tolist())) == cost.shape[1]
    assert not np.shares_memory(cost, out) and np.array_equal(cost, before)
    objective = float(cost[out, np.arange(cost.shape[1])].sum())
    np.testing.assert_allclose(objective, optimum, rtol=1e-9, atol=1e-7)
    return out


def greedy_trap(m):
    np.testing.assert_array_equal(checked(m, np.array([[1.,2.],[2.,100.]]), 4.), [1,0])


def rectangular(m):
    np.testing.assert_array_equal(checked(m, np.array([[4.,1.],[1.,5.],[3.,3.]]), 2.), [1,0])


def empty_and_ties(m):
    checked(m, np.empty((4,0)), 0.)
    checked(m, np.zeros((3,2)), 0.)
    checked(m, np.array([[-7.]]), -7.)


def exhaustive_small(m):
    rng = np.random.default_rng(20261113)
    for q in range(1,8):
        for n in range(1,min(q,4)+1):
            cost = rng.integers(-7,8,(q,n)).astype(np.float64)
            optimum = min(sum(cost[p[j],j] for j in range(n)) for p in itertools.permutations(range(q),n))
            checked(m, cost, optimum)


def noncontiguous_fractional(m):
    cost = np.array([[8.,99.,-1.,99.],[3.5,99.,4.,99.],[-2.25,99.,1.,99.]])[:,::2]
    checked(m, cost, -3.25)
    checked(m, np.array([[1e6,-1e6],[-1e6,1e6]]), -2e6)


def malformed(m):
    invalid(lambda:m.match_queries([[1.]]), TypeError)
    for cost in [np.ones((1,1),dtype=np.float32),np.ones((2,)),np.ones((1,1,1)),
                 np.ones((0,0)),np.ones((129,1)),np.ones((1,2)),
                 np.array([[np.nan]]),np.array([[np.inf]]),np.array([[1e6+1]])]:
        invalid(lambda:m.match_queries(cost))


def planted_scale(m):
    rng=np.random.default_rng(93)
    cost=rng.uniform(0.,10.,(128,96))
    queries=rng.permutation(128)[:96]
    cost[queries,np.arange(96)]=-1000.
    np.testing.assert_array_equal(checked(m,cost,-96000.),queries)


TESTS=[
 ("Greedy query choices can fail","public",greedy_trap),
 ("More queries than targets","public",rectangular),
 ("Empty targets and tied optima","public",empty_and_ties),
 ("Independent exhaustive assignment oracle","hidden",exhaustive_small),
 ("Noncontiguous fractional and signed costs","hidden",noncontiguous_fractional),
 ("Malformed assignment contract","hidden",malformed),
 ("Planted rectangular scale optimum","hidden",planted_scale),
]

