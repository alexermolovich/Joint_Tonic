import numpy as np
from numpy.testing import assert_allclose, assert_array_equal

def example(m):
    assert_allclose(m.update_occupancy([[0]],[[0,0,.8],[0,0,.8]],.5,2),[[2]])
def neutral(m):
    assert_allclose(m.update_occupancy([[.3,-.2]],[[0,1,.7]],.7,4),[[.3,-.2]])
def sequential(m):
    p=1/(1+np.exp(-3)); out=m.update_occupancy([[0]],[[0,0,p],[0,0,1-p]],.5,2)
    assert_allclose(out,[[-1]],atol=1e-9)
def bayes_oracle(m):
    grid=np.zeros((2,3)); before=grid.copy(); out=m.update_occupancy(grid,[[1,2,.6],[1,2,.75]],.5,20)
    # Odds multiply: 1.5 * 3 = 4.5.
    assert_allclose(out[1,2],np.log(4.5)); assert_array_equal(grid,before); assert out.dtype==np.float64
    empty=m.update_occupancy(grid,np.empty((0,3)),.5,2); assert_array_equal(empty,grid); assert not np.shares_memory(empty,grid)
def invalid(m):
    for obs in [[[0,0,0]],[[0,0,1]],[[1,0,.5]],[[.5,0,.5]],[[0,-1,.5]],[[0,0,np.nan]],[]]:
        with np.testing.assert_raises(ValueError): m.update_occupancy([[0]],obs,.5,2)
    with np.testing.assert_raises(ValueError): m.update_occupancy([[3]],np.empty((0,3)),.5,2)
    with np.testing.assert_raises(ValueError): m.update_occupancy([[0]],np.empty((0,3)),1,2)
TESTS=[('Repeated evidence saturation','public',example),('Prior-neutral evidence','public',neutral),('Sequential clipping order','hidden',sequential),('Bayes odds and immutability','hidden',bayes_oracle),('Invalid probabilities and cells','hidden',invalid)]
