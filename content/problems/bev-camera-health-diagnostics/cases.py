import numpy as np
from numpy.testing import assert_allclose,assert_array_equal
def example(m):
    r=m.camera_health(np.array([[True,False]]),np.array([[[3.,4],[0,0]]]),np.array([[True,False]]),.25,4);assert_allclose(r['dropout_rate'],[.5]);assert_allclose(r['reprojection_rmse'],[5]);assert r['dropout_alert'][0] and r['calibration_alert'][0]
def absent(m):
    r=m.camera_health(np.zeros((1,2),bool),np.zeros((1,2,2)),np.zeros((1,2),bool),.5,0);assert r['dropout_rate'][0]==1 and not r['observed'][0] and not r['calibration_alert'][0]
def equality(m):
    r=m.camera_health(np.array([[True,False],[True,True]]),np.array([[[3.,4],[999,999]],[[0,0],[0,0]]]),np.array([[True,False],[False,False]]),.5,5);assert_array_equal(r['dropout_alert'],[False,False]);assert_array_equal(r['calibration_alert'],[False,False]);assert_array_equal(r['observed'],[True,False])
def invalid(m):
    for r,e,v,a,b in [(np.zeros((1,1),bool),np.zeros((1,1,2)),np.ones((1,1),bool),.1,1),(np.ones((1,1),bool),np.zeros((1,1,2)),np.ones((1,1),bool),np.nan,1),(np.ones((1,1),bool),np.zeros((1,1,2)),np.ones((1,1),bool),.1,True),(np.empty((1,0),bool),np.empty((1,0,2)),np.empty((1,0),bool),.1,1)]:
        with np.testing.assert_raises(ValueError):m.camera_health(r,e,v,a,b)
def scale(m):
    received=np.ones((16,4096),bool);received[:,::4]=False;valid=received.copy();e=np.ones((16,4096,2));r=m.camera_health(received,e,valid,.2,1);assert_allclose(r['dropout_rate'],.25);assert_allclose(r['reprojection_rmse'],2**.5)
TESTS=[('Two independent alerts','public',example),('Missing camera','public',absent),('Equality and absent landmarks','hidden',equality),('Validation','hidden',invalid),('Window scale','hidden',scale)]
