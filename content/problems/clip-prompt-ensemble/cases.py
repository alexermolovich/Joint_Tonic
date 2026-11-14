import math
import numpy as np


def invalid(call,error=ValueError):
    try:
        call()
    except error:
        return
    raise AssertionError("Expected "+error.__name__)


def checked(m,images,prompts,t,expected_logits,expected_prototypes):
    before=(images.copy(),prompts.copy())
    result=m.prompt_ensemble_classifier(images,prompts,t)
    assert type(result) is tuple and len(result)==2
    logits,prototypes=result
    for out,shape in ((logits,(images.shape[0],prompts.shape[0])),(prototypes,(prompts.shape[0],images.shape[1]))):
        assert isinstance(out,np.ndarray) and out.dtype==np.float64 and out.shape==shape
        assert not np.shares_memory(out,images) and not np.shares_memory(out,prompts)
    assert not np.shares_memory(logits,prototypes)
    np.testing.assert_allclose(logits,expected_logits,rtol=1e-6,atol=1e-7)
    np.testing.assert_allclose(prototypes,expected_prototypes,rtol=1e-6,atol=1e-7)
    assert np.array_equal(images,before[0]) and np.array_equal(prompts,before[1])
    return result


def equal_prompt_influence(m):
    checked(m,np.array([[1.,0.]]),np.array([[[2.,0.],[0.,20.]]]),1.,
            [[math.sqrt(.5)]],[[math.sqrt(.5),math.sqrt(.5)]])


def class_scores(m):
    checked(m,np.array([[3.,4.]]),np.array([[[2.,0.]],[[0.,3.]]]),.5,
            [[1.2,1.6]],[[1.,0.],[0.,1.]])


def minimum_shape(m):
    checked(m,np.array([[-2.]]),np.array([[[1.]]]),1e-4,[[-10000.]],[[1.]])


def independent_vector_oracle(m):
    rng=np.random.default_rng(20261113)
    images=rng.normal(size=(4,12))[:,::2]
    prompts=rng.normal(size=(3,5,12))[:,:,::2]
    prototypes=[]
    for group in prompts:
        unit=[[float(x)/math.sqrt(sum(float(z)**2 for z in row)) for x in row] for row in group]
        mean=[sum(row[d] for row in unit)/len(unit) for d in range(images.shape[1])]
        norm=math.sqrt(sum(x*x for x in mean))
        prototypes.append([x/norm for x in mean])
    expected=[]
    for image in images:
        norm=math.sqrt(sum(float(x)**2 for x in image))
        expected.append([sum(float(x)*y for x,y in zip(image,prototype))/norm/.3 for prototype in prototypes])
    checked(m,images,prompts,.3,expected,prototypes)


def invalid_contract(m):
    a=np.array([[1.,0.]]);p=np.array([[[1.,0.]]])
    invalid(lambda:m.prompt_ensemble_classifier(a.tolist(),p,1.),TypeError)
    invalid(lambda:m.prompt_ensemble_classifier(a,p.tolist(),1.),TypeError)
    for bad in [a.astype(np.float32),a[0],np.zeros((0,2)),np.ones((257,2)),np.ones((1,513)),
                np.zeros((1,2)),np.array([[np.nan,0.]]),np.array([[np.inf,0.]]),
                np.array([[1e6,1e6]]),np.array([[1e-7,0.]])]:
        invalid(lambda:m.prompt_ensemble_classifier(bad,p,1.))
    for bad in [p.astype(np.float32),p[0],np.zeros((1,0,2)),np.ones((1001,1,2)),np.ones((1,65,2)),
                np.ones((1,1,3)),np.zeros_like(p),np.full_like(p,np.nan),
                np.array([[[1.,0.],[-1.,0.]]]),np.ones((1000,64,16))]:
        invalid(lambda:m.prompt_ensemble_classifier(a,bad,1.))
    for t in [True,0.,1e-5,10001.,10**1000,np.float64(1.),np.nan,np.inf]:
        invalid(lambda:m.prompt_ensemble_classifier(a,p,t))


def near_cancellation(m):
    a=np.array([[1.,0.]])
    invalid(lambda:m.prompt_ensemble_classifier(a,np.array([[[1.,0.],[-1.,1e-7]]]),1.))
    p=np.array([[[1.,0.],[-1.,1e-4]]])
    logits,prototypes=m.prompt_ensemble_classifier(a,p,1.)
    assert np.isfinite(logits).all() and np.isfinite(prototypes).all()
    np.testing.assert_allclose(np.linalg.norm(prototypes,axis=1),1.,rtol=1e-12,atol=1e-12)


def scale_invariance(m):
    images=np.tile(np.array([[3.,4.]]),(128,1))
    prompts=np.tile(np.array([[[1.,0.],[0.,2.]]]),(500,1,1))
    expected=np.full((128,500),1.4*math.sqrt(.5))
    checked(m,images,prompts,1.,expected,np.full((500,2),math.sqrt(.5)))


TESTS=[
 ("Normalize before ensembling","public",equal_prompt_influence),
 ("Class order and temperature","public",class_scores),
 ("Minimal dimension and temperature bound","public",minimum_shape),
 ("Independent vector oracle and noncontiguous axes","hidden",independent_vector_oracle),
 ("Typed shape norm and parameter contract","hidden",invalid_contract),
 ("Near-cancelling prompt directions","hidden",near_cancellation),
 ("Many images and classes","hidden",scale_invariance),
]

