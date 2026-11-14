import numpy as np
import math, hashlib, json, copy
from numpy.testing import assert_allclose, assert_array_equal
def f(x):return np.array(x,dtype=np.float64)
def i(x):return np.array(x,dtype=np.int64)
def b(x):return np.array(x,dtype=bool)
def eq(got,want):
    if isinstance(want,dict):
        assert isinstance(got,dict) and got.keys()==want.keys()
        for k in want:eq(got[k],want[k])
    elif isinstance(want,np.ndarray):
        assert isinstance(got,np.ndarray) and got.shape==want.shape and got.dtype==want.dtype
        assert_allclose(got,want,rtol=1e-6,atol=1e-7)
    else:
        assert type(got) is type(want)
        if isinstance(want,float):assert_allclose(got,want,rtol=1e-6,atol=1e-7)
        else:assert got==want
def rejected(fn):
    try:fn()
    except ValueError:return
    raise AssertionError('Expected ValueError')
def checked(fn,args):
    before=copy.deepcopy(args);out=fn(*args)
    arrays=[v for v in args if isinstance(v,np.ndarray)]
    for old,new in zip(before,args):
        if isinstance(old,np.ndarray):assert_array_equal(old,new)
        else:assert old==new
    values=list(out.values()) if isinstance(out,dict) else [out]
    for x in values:
        if isinstance(x,np.ndarray):
            for a in arrays:assert not np.shares_memory(x,a)
            for y in values:
                if isinstance(y,np.ndarray) and y is not x:assert not np.shares_memory(x,y)
    return out
def generic_invalid(fn,args):
    for index,a in enumerate(args):
        if isinstance(a,np.ndarray):
            bad=list(args);bad[index]=a.tolist();rejected(lambda:fn(*bad))
            bad=list(args);bad[index]=a.astype(np.float32) if a.dtype==np.float64 else a.astype(np.float64);rejected(lambda:fn(*bad))
            if a.dtype==np.float64 and a.size:
                for value in (np.nan,np.inf,1000001.):
                    bad=list(args);bad[index]=a.copy();bad[index].flat[0]=value;rejected(lambda:fn(*bad))
def args():return [f([[0]]),f([[1]]),f([[[1,0,0]]]),f([0,0,0]),f([[0,0,0]])]
def example1(m):eq(checked(m.render_color_gradients,args()),dict(rgb=f([[0,0,0]]),loss=0.,density_gradient=f([[0]]),color_gradient=f([[[0,0,0]]])))
def example2(m):
 a=args();a[0][:]=math.log(2);eq(m.render_color_gradients(*a),dict(rgb=f([[.5,0,0]]),loss=1/12,density_gradient=f([[1/6]]),color_gradient=f([[[1/6,0,0]]])))
def loss(a):
 rows=[]
 for r in range(a[0].shape[0]):
  trans=1.;rgb=np.zeros(3)
  for k in range(a[0].shape[1]):
   remaining=math.exp(-a[0][r,k]*a[1][r,k]);rgb+=trans*(1-remaining)*a[2][r,k];trans*=remaining
  rows.append(rgb+trans*a[3])
 rgb=f(rows);return float(np.mean((rgb-a[4])**2)),rgb
def oracle(m):
 rng=np.random.default_rng(1007);a=[rng.uniform(.2,1,(2,4)),rng.uniform(.1,.6,(2,4)),rng.uniform(.2,.8,(2,4,3)),rng.uniform(.2,.8,3),rng.uniform(.2,.8,(2,3))];out=checked(m.render_color_gradients,a);l,rgb=loss(a);eq(out['loss'],l);eq(out['rgb'],rgb)
 for parameter,key in [(0,'density_gradient'),(2,'color_gradient')]:
  for index in np.ndindex(a[parameter].shape):
   plus=copy.deepcopy(a);minus=copy.deepcopy(a);plus[parameter][index]+=1e-5;minus[parameter][index]-=1e-5
   assert_allclose(out[key][index],(loss(plus)[0]-loss(minus)[0])/2e-5,rtol=1e-5,atol=1e-8)
 a=[np.full((32,128),1000.),np.full((32,128),10.),np.ones((32,128,3)),np.zeros(3),np.ones((32,3))];out=checked(m.render_color_gradients,a);eq(out['rgb'],np.ones((32,3)));eq(out['density_gradient'],np.zeros((32,128)))
def invalid(m):
 a=args();generic_invalid(m.render_color_gradients,a)
 for index,value in [(0,f([[-1]])),(1,f([[0]])),(2,f([[[1.01,0,0]]])),(3,f([[0,0,0]]))]:
  q=a.copy();q[index]=value;rejected(lambda:m.render_color_gradients(*q))

TESTS=[('Worked example 1','public',example1),('Worked example 2','public',example2),('Independent mechanism, boundaries, scale and preservation','hidden',oracle),('Documented invalid inputs','hidden',invalid)]
