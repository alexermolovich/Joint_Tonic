import numpy as np
from numpy.testing import assert_allclose, assert_array_equal

def example(m):
    r=m.audit_frame_ids([3,4,4,6]); assert_array_equal(r['missing'],[5]); assert_array_equal(r['duplicates'],[4])
def repeated(m):
    r=m.audit_frame_ids([7,7,7]); assert_array_equal(r['missing'],[]); assert_array_equal(r['duplicates'],[7])
def boundary(m):
    for ids in [[],[0],[100000]]:
        r=m.audit_frame_ids(ids); assert set(r)=={'missing','duplicates'}
        for a in r.values(): assert a.shape==(0,) and a.dtype==np.int64
    assert len(m.audit_frame_ids([0,100000])['missing'])==99999
def oracle(m):
    ids=np.sort(np.random.default_rng(12).integers(10,90,200)); original=ids.copy(); r=m.audit_frame_ids(ids)
    assert_array_equal(r['missing'],[i for i in range(int(ids[0]),int(ids[-1])+1) if i not in ids])
    assert_array_equal(r['duplicates'],sorted({int(i) for i in ids if list(ids).count(i)>1})); assert_array_equal(ids,original)
def invalid(m):
    for ids in [[2,1],[-1],[100001],[.5],[True],['1'],[np.nan],[[1]]]:
        with np.testing.assert_raises(ValueError): m.audit_frame_ids(ids)
TESTS=[('Gap and repetition','public',example),('Repeated ID once','public',repeated),('Empty and bounded span','hidden',boundary),('Counting oracle','hidden',oracle),('Invalid counters','hidden',invalid)]
