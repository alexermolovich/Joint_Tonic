import numpy as np
from numpy.testing import assert_allclose,assert_array_equal

def bad(fn):
    try: fn()
    except ValueError: return
    raise AssertionError("expected ValueError")

def one(m):
    r=m.augmented_targets([1],[[2,4]],[False],[[True,True]],.5);assert_allclose(r['targets'],[2.5]);assert_allclose(r['mean_next'],[3]);assert_array_equal(r['counts'],[2])
def terminal(m):
    r=m.augmented_targets([1],[[2]],[True],[[False]],.5);assert_array_equal(r['targets'],[1]);assert np.isnan(r['mean_next'][0]) and r['counts'][0]==0
def scale(m):
    v=np.full((128,128),4.)[:,::2];mask=np.ones_like(v,dtype=bool);mask[:,::2]=False;r=m.augmented_targets(np.ones(128),v,np.zeros(128,bool),mask,.5);assert_allclose(r['targets'],3);assert_array_equal(r['counts'],np.full(128,32));assert not np.shares_memory(r['mean_next'],v)
def invalid(m):
    for args in [([1],[[2]],[False],[[False]],0),([1],[[np.nan]],[True],[[False]],1),([1],[[2]],[1],[[True]],1)]:bad(lambda:m.augmented_targets(*args))
TESTS=[('Augmented target mean','public',one),('Terminal without views','public',terminal),('Scale masked views','hidden',scale),('Invalid target support','hidden',invalid)]
