"""Original deterministic synthetic fixtures, CC0-1.0."""
import copy
import numpy as np

def rejects(fn):
    try:fn()
    except ValueError:return
    raise AssertionError("Expected ValueError")


def slices(m):
 r=m.shift_bucket_metrics(np.array([0,1,0],dtype=np.int64),np.array([1.,9.,3.]),3);np.testing.assert_array_equal(r['counts'],[2,1,0]);np.testing.assert_allclose(r['mean_error'],[2,9,np.nan],equal_nan=True);np.testing.assert_allclose(r['worst_error'],[3,9,np.nan],equal_nan=True)
def empty(m):
 r=m.shift_bucket_metrics(np.array([],dtype=np.int64),np.array([],dtype=np.float64),2);np.testing.assert_array_equal(r['counts'],[0,0]);assert np.isnan(r['mean_error']).all() and np.isnan(r['worst_error']).all()
def scale(m):
 ids=(np.arange(200000)%16)[::2];errors=(np.arange(200000,dtype=float)%100)[::2];ic=ids.copy();ec=errors.copy();r=m.shift_bucket_metrics(ids,errors,32)
 for b in range(32):
  values=[float(errors[i]) for i in range(len(ids)) if ids[i]==b];assert r['counts'][b]==len(values)
  if values:assert abs(r['mean_error'][b]-sum(values)/len(values))<1e-10 and r['worst_error'][b]==max(values)
  else:assert np.isnan(r['mean_error'][b]) and np.isnan(r['worst_error'][b])
 np.testing.assert_array_equal(ids,ic);np.testing.assert_array_equal(errors,ec)
def boundary_storage(m):
 ids=np.array([0,1],dtype=np.int64);errors=np.array([0.,1e6]);r=m.shift_bucket_metrics(ids,errors,2);assert r['counts'].dtype==np.int64;np.testing.assert_array_equal(r['mean_error'],errors)
 assert not np.shares_memory(r['mean_error'],r['worst_error']) and not np.shares_memory(r['mean_error'],errors)
def invalid(m):
 for ids,e,b in [(np.array([0],dtype=np.int32),np.array([1.]),1),(np.array([0],dtype=np.int64),np.array([1.],dtype=np.float32),1),(np.array([1],dtype=np.int64),np.array([1.]),1),(np.array([0],dtype=np.int64),np.array([np.nan]),1),(np.array([0],dtype=np.int64),np.array([-1.]),1),(np.array([0],dtype=np.int64),np.array([1.]),True),(np.array([0],dtype=np.int64),np.array([1.]),257)]:rejects(lambda:m.shift_bucket_metrics(ids,e,b))

TESTS=[('Weak and missing shift slices', 'public', slices), ('Empty evidence', 'public', empty), ('Scalar oracle over hundred thousand cases', 'hidden', scale), ('Bounds types and independent storage', 'hidden', boundary_storage), ('Invalid metric schema', 'hidden', invalid)]
