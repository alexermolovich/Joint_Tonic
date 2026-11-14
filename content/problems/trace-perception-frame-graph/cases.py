import numpy as np
from numpy.testing import assert_allclose, assert_array_equal

def fixture():
    A=np.eye(4); A[:3,3]=[1,0,0]; B=np.eye(4); B[:3,3]=[0,2,0]; return [('base','wrist',A),('wrist','camera',B)]
def forward(m):
    out=m.resolve_frame_transform(fixture(),'camera','base'); assert_allclose(out[:3,3],[1,2,0])
def reverse(m):
    out=m.resolve_frame_transform(fixture(),'base','camera'); assert_allclose(out[:3,3],[-1,-2,0])
def noncommuting(m):
    edges=fixture(); edges[0][2][:3,:3]=[[0,-1,0],[1,0,0],[0,0,1]]; old=edges[0][2].copy()
    expected=edges[0][2]@edges[1][2]; out=m.resolve_frame_transform(edges,'camera','base'); assert_allclose(out,expected)
    inv=m.resolve_frame_transform(edges,'base','camera'); assert_allclose(inv@out,np.eye(4),atol=1e-9); assert_array_equal(edges[0][2],old)
def identity(m):
    out=m.resolve_frame_transform(fixture(),'wrist','wrist'); assert_array_equal(out,np.eye(4)); assert out.dtype==np.float64
def invalid(m):
    for edges,s,t in [(fixture()+[('camera','base',np.eye(4))],'base','base'),(fixture()+[('other','camera',np.eye(4))],'base','wrist'),(fixture()+[('a','b',np.eye(4))],'base','a'),(fixture(),'missing','base'),([], 'base','base'),([('a','a',np.eye(4))],'a','a')]:
        with np.testing.assert_raises(ValueError): m.resolve_frame_transform(edges,s,t)
    bad=np.eye(4); bad[0,0]=-1
    with np.testing.assert_raises(ValueError): m.resolve_frame_transform(fixture()+[('a','b',bad)],'base','base')
TESTS=[('Forward path','public',forward),('Reverse path','public',reverse),('Noncommuting rotation and translation','hidden',noncommuting),('Known-frame identity','hidden',identity),('Whole-graph structural validation','hidden',invalid)]
