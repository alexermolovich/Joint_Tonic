import numpy as np
from numpy.testing import assert_allclose,assert_array_equal

def bad(fn):
    try: fn()
    except ValueError: return
    raise AssertionError("expected ValueError")

def one(m):
    r=m.train_joint_controller([0,0],[1],np.zeros((1,1,1)),[1],1,.01,.2);assert_array_equal(r['theta_history'],[[0,0],[0,0]]);assert_array_equal(r['training_return'],[-1]);assert_array_equal(r['evaluation_final_error'],[[1]]);assert_array_equal(r['evaluation_return'],[-1]);assert_array_equal(r['clip_fraction'],[[0]])
def two(m):
    r=m.train_joint_controller([0,0],[1,1],[[[1],[-1]]],[0],1,0,.2);assert_allclose(r['training_return'],[-1.0008]);assert_array_equal(r['theta_history'],[[0,0],[0,0]]);assert_array_equal(r['evaluation_final_error'],[[0]])
def analytic_step(m):
    r=m.train_joint_controller([0,0],[1,1],[[[1],[-1]]],[0],1,.01,.2);theta=np.full(2,.01/np.sqrt(2));assert_allclose(r['theta_history'][1],theta);assert_allclose(r['evaluation_final_error'][0,0],.1*theta[1]);assert_allclose(r['evaluation_return'][0],-(.1*theta[1])**2-.01*theta[1]**2)
def independent_oracle(m):
    # Scalar rollout/gradient oracle deliberately loops samples and feature coordinates.
    z=np.array([[[1.,-1.,.5],[-.5,1.,-1.]],[[.2,.8,-.3],[-1.,.4,.7]]]);goals=np.array([1.,-.7]);theta=np.array([.2,.1]);wanted=[theta.copy()];train=[];held=[];scores=[];clipping=[]
    for it in range(2):
        rows=[];rewards=[]
        for bi,g in enumerate(goals):
            q=0.;record=[];rs=[]
            for t in range(3):
                x=np.array([g-q,1.]);mu=sum(x*theta);a=mu+.2*z[it,bi,t];q+=.1*a;rs.append(-(q-g)**2-.01*a*a);record.append((x,a,-.5*((a-mu)/.2)**2))
            rewards.append(rs);ret=0.;targets=[]
            for reward in rs[::-1]:ret=reward+.95*ret;targets.append(ret)
            rows.extend([(*item,target) for item,target in zip(record,targets[::-1])])
        train.append(np.mean([sum(rs) for rs in rewards]));rr=np.array([row[3] for row in rows]);advantages=(rr-rr.mean())/np.sqrt(rr.var()+1e-8);fractions=[]
        for epoch in range(4):
            grad=np.zeros(2);outside=0
            for (x,a,old,_),adv in zip(rows,advantages):
                mu=sum(x*theta);ratio=np.exp(-.5*((a-mu)/.2)**2-old);outside+=ratio<.95 or ratio>1.05
                if not ((adv>0 and ratio>1.05) or (adv<0 and ratio<.95)):
                    for j in range(2):grad[j]+=ratio*adv*(a-mu)/.04*x[j]/len(rows)
            fractions.append(outside/len(rows));norm=sum(grad*grad)**.5;theta+=.01*grad/max(1,norm);theta[0]=min(2,max(0,theta[0]));theta[1]=min(.5,max(-.5,theta[1]))
        wanted.append(theta.copy());clipping.append(fractions);errs=[];rets=[]
        for goal in [-1.,.3]:
            q=0.;score=0.
            for t in range(3):a=theta[0]*(goal-q)+theta[1];q+=.1*a;score+=-(q-goal)**2-.01*a*a
            errs.append(abs(q-goal));rets.append(score)
        held.append(errs);scores.append(np.mean(rets))
    r=m.train_joint_controller([.2,.1],goals,z,[-1,.3],4,.01,.05);assert_allclose(r['theta_history'],wanted,atol=1e-10);assert_allclose(r['training_return'],train);assert_allclose(r['clip_fraction'],clipping);assert_allclose(r['evaluation_final_error'],held);assert_allclose(r['evaluation_return'],scores)
def scale_and_holdout(m):
    rng=np.random.default_rng(20261114);z=rng.uniform(-3,3,(8,32,32))[:,:,::2];before=z.copy();goals=np.linspace(-1,1,32);r=m.train_joint_controller([.5,0],goals,z,goals,4,.01,.1);s=m.train_joint_controller([.5,0],goals,z,[1],4,.01,.1);assert_allclose(r['theta_history'],s['theta_history']);assert_allclose(r['training_return'],s['training_return']);assert_array_equal(z,before)
    for v in r.values():assert np.isfinite(v).all() and not np.shares_memory(v,z)
    assert (r['theta_history'][:,0]>=0).all() and (r['theta_history'][:,0]<=2).all();assert r['evaluation_final_error'].shape==(8,32)
def invalid(m):
    for theta,goals,z,evals,ep,lr,eps in [([-1,0],[1],[[[0]]],[1],1,.01,.2),([0,0],[2],[[[0]]],[1],1,.01,.2),([0,0],[1],[[[4]]],[1],1,.01,.2),([0,0],[1],[[[0]]],[1],True,.01,.2),([0,0],[1],[[[0]]],[1],1,.1,.2),([0,0],[1],[[[0]]],[],1,.01,.2)]:bad(lambda:m.train_joint_controller(theta,goals,z,evals,ep,lr,eps))
TESTS=[('Single-sample zero update','public',one),('Supplied exploration and no learning','public',two),('Analytical nonzero projected gradient step','hidden',analytic_step),('Independent scalar multi-epoch oracle','hidden',independent_oracle),('Scale holdout isolation and input preservation','hidden',scale_and_holdout),('Invalid integration configuration','hidden',invalid)]
