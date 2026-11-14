import math
import numpy as np


def invalid(call,error=ValueError):
    try: call()
    except error: return
    raise AssertionError("Expected "+error.__name__)


def checked(m,grid,transform,resolution,origin,wanted):
    saved=[x.copy() for x in (grid,transform,origin)]
    out=m.warp_previous_bev(grid,transform,resolution,origin)
    assert isinstance(out,np.ndarray) and out.dtype==np.float64 and out.shape==grid.shape
    np.testing.assert_allclose(out,wanted,rtol=1e-6,atol=1e-7)
    for x,before in zip((grid,transform,origin),saved):
        assert np.array_equal(x,before) and not np.shares_memory(out,x)
    return out


def translation(m):
    grid=np.arange(1.,7.).reshape(2,3,1)
    transform=np.eye(3);transform[0,2]=1
    checked(m,grid,transform,1.,np.zeros(2),np.array([[[2.],[3.],[0.]],[[5.],[6.],[0.]]]))


def partial_border(m):
    grid=np.arange(1.,7.).reshape(2,3,1)
    transform=np.eye(3);transform[0,2]=.5
    checked(m,grid,transform,1.,np.zeros(2),np.array([[[1.5],[2.5],[1.5]],[[4.5],[5.5],[3.]]]))


def identity_large_origin(m):
    grid=np.arange(24,dtype=np.float64).reshape(3,4,2)
    out=checked(m,grid,np.eye(3),.001,np.array([1e6,-1e6]),grid)
    np.testing.assert_array_equal(out,grid)


def rotation_and_near_valid(m):
    grid=np.arange(1.,5.).reshape(2,2,1)
    rotation=np.array([[0.,-1.,0.],[1.,0.,0.],[0.,0.,1.]])
    checked(m,grid,rotation,1.,np.array([-1.,-1.]),np.array([[[2.],[4.]],[[1.],[3.]]]))
    transform=np.eye(3);transform[0,0]+=2e-8
    out=m.warp_previous_bev(np.array([[[0.],[1e6]]]),transform,1.,np.zeros(2))
    np.testing.assert_allclose(out[0,0,0],.01,rtol=1e-6,atol=1e-7)


def scalar_oracle(grid,transform,resolution,origin):
    h,w,c=grid.shape;result=np.zeros_like(grid)
    for r in range(h):
        for col in range(w):
            point=np.array([origin[0]+(col+.5)*resolution,origin[1]+(r+.5)*resolution,1.])
            prior=transform@point
            u=(prior[0]-origin[0])/resolution-.5
            v=(prior[1]-origin[1])/resolution-.5
            i,j=math.floor(u),math.floor(v)
            for yy in (j,j+1):
                for xx in (i,i+1):
                    if 0<=yy<h and 0<=xx<w:
                        result[r,col]+=grid[yy,xx]*(1-abs(u-xx))*(1-abs(v-yy))
    return result


def independent_rotated_noncontiguous(m):
    grid=np.arange(48,dtype=np.float64).reshape(4,3,4)[:,:,::2]
    angle=.3
    transform=np.array([[math.cos(angle),-math.sin(angle),.2],[math.sin(angle),math.cos(angle),-.3],[0.,0.,1.]])
    origin=np.array([.25,-.5])
    checked(m,grid,transform,.4,origin,scalar_oracle(grid,transform,.4,origin))
    transform=np.eye(3);transform[0,2]=-1000
    checked(m,grid,transform,1.,origin,np.zeros_like(grid))


def malformed(m):
    grid=np.ones((1,1,1));t=np.eye(3);o=np.zeros(2)
    invalid(lambda:m.warp_previous_bev(grid.tolist(),t,1,o),TypeError)
    invalid(lambda:m.warp_previous_bev(grid,t.tolist(),1,o),TypeError)
    invalid(lambda:m.warp_previous_bev(grid,t,1,o.tolist()),TypeError)
    for bad in [grid.astype(np.float32),grid[0],np.empty((0,1,1)),np.ones((257,1,1)),np.ones((1,1,65)),
                np.ones((256,256,64)),np.full_like(grid,np.nan),np.full_like(grid,np.inf),np.full_like(grid,1e6+1)]:
        invalid(lambda:m.warp_previous_bev(bad,t,1,o))
    for bad in [t.astype(np.float32),np.eye(2),np.diag([-1.,1.,1.]),np.diag([2.,1.,1.]),
                np.diag([1.,1.,2.]),np.full((3,3),np.nan)]:
        invalid(lambda:m.warp_previous_bev(grid,bad,1,o))
    for bad in [o.astype(np.float32),np.zeros((1,2)),np.array([np.inf,0.]),np.array([1e6+1,0.])]:
        invalid(lambda:m.warp_previous_bev(grid,t,1,bad))
    for res in [True,0,.0001,1001,10**1000,np.nan,np.inf,np.float64(1)]:
        invalid(lambda:m.warp_previous_bev(grid,t,res,o))


def realistic(m):
    grid=np.ones((64,128,64),dtype=np.float64)
    out=checked(m,grid,np.eye(3),.125,np.array([1e6,1e6]),grid)
    np.testing.assert_array_equal(out,grid)


TESTS=[
 ("Current-to-previous translation direction","public",translation),
 ("Fractional zero-padding border","public",partial_border),
 ("Large-origin identity without cancellation","public",identity_large_origin),
 ("Rotation and near-valid transform semantics","hidden",rotation_and_near_valid),
 ("Independent scalar sampling and noncontiguous features","hidden",independent_rotated_noncontiguous),
 ("Malformed metric frame and tensor contract","hidden",malformed),
 ("Large feature grid identity","hidden",realistic),
]

