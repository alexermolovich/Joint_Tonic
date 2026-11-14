import math
import numpy as np
from numpy.testing import assert_allclose, assert_array_equal


def right_angle(m):
    result=m.planar_ik(1,1,[1,1])
    assert result["reachable"] is True and result["singular"] is False
    assert_allclose(result["angles"],[0,math.pi/2],atol=1e-7)


def extension(m):
    result=m.planar_ik(2,1,[3,0])
    assert result["reachable"] is True and result["singular"] is True
    assert_allclose(result["angles"],[0,0],atol=1e-7)
    assert m.planar_ik(2,1,[4,0]) == dict(reachable=False,angles=None,singular=False)


def folded_and_inner_boundary(m):
    result=m.planar_ik(1,1,[0,0])
    assert_allclose(result["angles"],[0,math.pi],atol=1e-7)
    assert result["singular"] is True
    result=m.planar_ik(1,2,[1,0])
    assert_allclose(result["angles"],[-math.pi,math.pi],atol=1e-7)
    assert result["singular"] is True
    assert m.planar_ik(3,1,[1,0])["reachable"] is False


def tolerance(m):
    assert m.planar_ik(1,1,[2+5e-10,0])["reachable"] is True
    assert m.planar_ik(1,1,[2+2e-9,0])["reachable"] is False
    assert m.planar_ik(2,1,[1-5e-10,0])["reachable"] is True
    assert m.planar_ik(2,1,[1-2e-9,0])["reachable"] is False


def invalid(m):
    for bad in [0,-1,1e-4,1001,True,np.bool_(True),np.nan,np.inf,1j,"1",[],10**1000]:
        with np.testing.assert_raises(ValueError): m.planar_ik(bad,1,[1,1])
        with np.testing.assert_raises(ValueError): m.planar_ik(1,bad,[1,1])
    with np.testing.assert_raises(ValueError): m.planar_ik(.001,1000,[1000,0])
    for target in [[],[1],[[1,1]],[1,np.nan],[np.inf,1],[True,False],["1","1"],[1j,0],[1000001,0]]:
        with np.testing.assert_raises(ValueError): m.planar_ik(1,1,target)


def forward_check(m):
    rng=np.random.default_rng(20261113)
    for _ in range(100):
        L1,L2=rng.uniform(.2,3,2)
        q1,q2=rng.uniform(-math.pi,math.pi),rng.uniform(.05,math.pi-.05)
        target=np.array([L1*math.cos(q1)+L2*math.cos(q1+q2),L1*math.sin(q1)+L2*math.sin(q1+q2)])
        saved=target.copy()
        result=m.planar_ik(L1,L2,target)
        assert set(result)=={"reachable","angles","singular"} and result["reachable"] is True
        out=result["angles"]
        assert out.shape==(2,) and out.dtype==np.float64
        assert -math.pi<=out[0]<math.pi and 0<=out[1]<=math.pi
        endpoint=[L1*np.cos(out[0])+L2*np.cos(out.sum()),L1*np.sin(out[0])+L2*np.sin(out.sum())]
        assert_allclose(endpoint,target,atol=1e-7,rtol=1e-7)
        assert_array_equal(target,saved); assert not np.shares_memory(out,target)


TESTS=[("Right-angle elbow","public",right_angle),("Extension and unreachable target","public",extension),
       ("Folded geometry and inner hole","hidden",folded_and_inner_boundary),("Reachability tolerance","hidden",tolerance),
       ("Invalid lengths and targets","hidden",invalid),("Independent forward-kinematics check","hidden",forward_check)]
