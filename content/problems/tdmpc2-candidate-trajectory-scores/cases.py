import numpy as np
from numpy.testing import assert_allclose,assert_array_equal

def bad(fn):
    try: fn()
    except ValueError: return
    raise AssertionError("expected ValueError")

def one(m):
    r=m.score_latent_trajectories([[1,2]],[[False,False]],[4],.5);assert_array_equal(r['contributions'],[[1,1]]);assert_array_equal(r['tail'],[1]);assert_array_equal(r['scores'],[3])
def terminal(m):
    r=m.score_latent_trajectories([[1,2]],[[True,False]],[4],.5);assert_array_equal(r['contributions'],[[1,0]]);assert_array_equal(r['tail'],[0]);assert_array_equal(r['scores'],[1])
def oracle(m):
    rng=np.random.default_rng(546);rewards=rng.normal(size=(1024,256))[:,::2];done=rng.random(rewards.shape)>.95;v=rng.normal(size=1024);before=rewards.copy();r=m.score_latent_trajectories(rewards,done,v,.95);expected=[]
    for i in range(1024):
        value=0.;weight=1.;alive=True
        for t in range(128):
            if alive:value+=weight*rewards[i,t]
            alive=alive and not done[i,t];weight*=.95
        expected.append(value+(weight*v[i] if alive else 0))
    assert_allclose(r['scores'],expected,atol=1e-12);assert r['best']==int(np.argmax(expected));assert_array_equal(rewards,before);assert not np.shares_memory(r['contributions'],rewards)
    r=m.score_latent_trajectories([[1,100]],[[False,False]],[100],0);assert_array_equal(r['scores'],[1])
    r=m.score_latent_trajectories(np.empty((2,0)),np.empty((2,0),bool),[2,2],0);assert_array_equal(r['scores'],[2,2]);assert r['best']==0
    r=m.score_latent_trajectories([[1,2]],[[False,True]],[100],1);assert_array_equal(r['scores'],[3])
def invalid(m):
    bad(lambda:m.score_latent_trajectories([[1,np.nan]],[[True,False]],[0],1));bad(lambda:m.score_latent_trajectories([[1]],[[False]],[0],10**1000));bad(lambda:m.score_latent_trajectories([[1]],[[0]],[0],1))
TESTS=[('Discounted rewards and critic tail','public',one),('Terminating transition reward retained','public',terminal),('Scalar survival oracle scale gamma0 and zero horizon','hidden',oracle),('Invalid even after termination','hidden',invalid)]
