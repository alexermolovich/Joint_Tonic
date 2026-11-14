"""Original deterministic synthetic fixtures; CC0-1.0."""
import numpy as np
import math

def arr(v):return np.array(v,dtype=np.float64)
def reject(fn):
 try:fn()
 except ValueError:return
 raise AssertionError('Expected ValueError')
def oracle(calibration,evaluation,weights,alphas,tol):
 a,x,w=calibration.tolist(),evaluation.tolist(),weights.tolist();M=len(a);N=len(x);C=len(w);D=len(w[0]);result=[];scores=[];rows=[];scales=[]
 baseline=[[sum(x[i][j]*w[j][d] for j in range(C)) for d in range(D)] for i in range(N)]
 for alpha in alphas:
  scale=[min(1e6,max(1e-6,max(max(abs(a[i][j]) for i in range(M)),1e-6)**float(alpha)/max(max(abs(v) for v in w[j]),1e-6)**(1-float(alpha)))) for j in range(C)];scales.append(scale)
  xx=[[v/scale[j] for j,v in enumerate(row)] for row in x];ww=[[v*scale[j] for v in row] for j,row in enumerate(w)]
  xs=[max(abs(v) for v in row)/127 or 1 for row in xx];ws=[max(abs(ww[j][d]) for j in range(C))/127 or 1 for d in range(D)]
  qx=[[max(-127,min(127,round(v/xs[i]))) for v in row] for i,row in enumerate(xx)];qw=[[max(-127,min(127,round(v/ws[d]))) for d,v in enumerate(row)] for row in ww]
  output=[[sum(qx[i][j]*qw[j][d] for j in range(C))*xs[i]*ws[d] for d in range(D)] for i in range(N)];result.append(output)
  errors=[[output[i][d]-baseline[i][d] for d in range(D)] for i in range(N)];scores.append(sum(v*v for row in errors for v in row)/(N*D));rows.append([max(abs(v) for v in row) for row in errors])
 chosen=min(range(len(scores)),key=lambda k:scores[k]);accepted=[all(v<=tol for v in row) for row in rows]
 return dict(scales=arr(scales),output_mse=arr(scores),row_max_abs=arr(rows),accepted=np.array(accepted),selected_index=chosen,selected_output=arr(result[chosen]),passed=bool(accepted[chosen]))
def check(actual,wanted):
 assert set(actual)==set(wanted)
 for k,v in wanted.items():
  if isinstance(v,np.ndarray):
   assert isinstance(actual[k],np.ndarray) and actual[k].shape==v.shape and actual[k].dtype==v.dtype
   np.testing.assert_allclose(actual[k],v,rtol=1e-8,atol=1e-9)
  else:assert type(actual[k]) is type(v) and actual[k]==v

def example1(m):
 r=m.evaluate_smoothing_pipeline(arr([[2]]),arr([[4]]),arr([[2]]),arr([.5]),1e-9)
 check(r,dict(scales=arr([[1]]),output_mse=arr([0]),row_max_abs=arr([[0]]),accepted=np.array([True]),selected_index=0,selected_output=arr([[8]]),passed=True))
def example2(m):
 r=m.evaluate_smoothing_pipeline(arr([[0,0]]),arr([[0,0]]),arr([[0],[0]]),arr([0,1]),0)
 check(r,dict(scales=arr([[1e6,1e6],[1e-6,1e-6]]),output_mse=arr([0,0]),row_max_abs=arr([[0],[0]]),accepted=np.array([True,True]),selected_index=0,selected_output=arr([[0]]),passed=True))
def calibration_only(m):
 a=arr([[1,10],[2,1]]);x=arr([[100,1],[1,200]]);w=arr([[1,2],[3,4]]);alphas=arr([.25,.5,.75]);expected=oracle(a,x,w,alphas,.1)
 check(m.evaluate_smoothing_pipeline(a,x,w,alphas,.1),expected)
 altered=x*2;r=m.evaluate_smoothing_pipeline(a,altered,w,alphas,.1)
 np.testing.assert_array_equal(r['scales'],expected['scales'])
def edge_guards(m):
 a=np.array([[1e-38,0]],dtype=np.float32);x=np.array([[2e-38,0]],dtype=np.float32);w=np.array([[3e-38],[0]],dtype=np.float32);alphas=arr([0,1,.5,.5]);r=m.evaluate_smoothing_pipeline(a,x,w,alphas,0)
 for v in r.values():
  if isinstance(v,np.ndarray):assert np.isfinite(v).all()
 r=m.evaluate_smoothing_pipeline(arr([[1,3]]),arr([[1,3]]),arr([[2],[4]]),arr([.5,.5]),1e6);assert r['selected_index']==0 and r['passed'] is True

 a=arr([[1.]]);x=arr([[np.nextafter(0.,1.)]]);w=arr([[1.]]);r=m.evaluate_smoothing_pipeline(a,x,w,arr([.5]),0)
 assert r['selected_output'][0,0]==0 and r['row_max_abs'][0,0]==np.nextafter(0.,1.) and r['passed'] is False

def scale_and_preservation(m):
 rng=np.random.default_rng(909);a=rng.normal(size=(64,32))[:,::2];x=rng.normal(size=(32,32))[:,::2];w=rng.normal(size=(16,16))[:,::2];alphas=arr([0,.25,.5,.75,1]);before=[v.copy() for v in (a,x,w,alphas)]
 r=m.evaluate_smoothing_pipeline(a,x,w,alphas,.05);check(r,oracle(a,x,w,alphas,.05))
 for old,new in zip(before,(a,x,w,alphas)):np.testing.assert_array_equal(old,new)
 assert not np.shares_memory(r['selected_output'],x)

def selection_is_not_a_gate_filter(m):
 rng=np.random.default_rng(6);a=rng.normal(size=(4,4));x=rng.normal(size=(8,4));w=rng.normal(size=(4,3));alphas=arr([0,.25,.5,.75,1]);r=m.evaluate_smoothing_pipeline(a,x,w,alphas,.018)
 check(r,oracle(a,x,w,alphas,.018));assert r['selected_index']==0 and r['accepted'][1] and r['passed'] is False

def invalid(m):
 good=(arr([[1]]),arr([[1]]),arr([[1]]),arr([.5]),0)
 for i,bad in [(0,np.empty((0,1))),(1,arr([[1,2]])),(2,arr([[1],[2]])),(3,arr([])),(3,arr([-1])),(3,arr([1.1])),(3,np.array([1])),(0,arr([[np.nan]])),(2,arr([[1001]])),(4,True),(4,float('inf')),(4,10**1000)]:
  args=list(good);args[i]=bad;reject(lambda:m.evaluate_smoothing_pipeline(*args))
TESTS=[('Scalar calibration and validation','public',example1),('Zero channels and deterministic tie','public',example2),('Calibration split never reads validation ranges','hidden',calibration_only),('Float32 promotion, guards and equal candidates','hidden',edge_guards),('Independent scalar pipeline oracle, scale and preservation','hidden',scale_and_preservation),('MSE choice remains separate from release acceptance','hidden',selection_is_not_a_gate_filter),('Complete input contract','hidden',invalid)]
