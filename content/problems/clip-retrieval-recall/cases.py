import numpy as np


def directions(m):
    assert m.retrieval_recall(np.array([[.9,.8],[.95,.1]]),1)=={"image_to_text":.5,"text_to_image":0.}


def ties(m):
    r=m.retrieval_recall(np.zeros((3,3)),2)
    assert r=={"image_to_text":2/3,"text_to_image":2/3}


def all_candidates(m):
    assert m.retrieval_recall(np.array([[0.,9.],[8.,0.]]),2)=={"image_to_text":1.,"text_to_image":1.}


def oracle(m):
    rng=np.random.default_rng(20261113);s=rng.integers(-3,4,(61,61)).astype(np.float64);old=s.copy();k=7
    ir=sum(i in sorted(range(61),key=lambda j:(-s[i,j],j))[:k] for i in range(61))/61
    tr=sum(j in sorted(range(61),key=lambda i:(-s[i,j],i))[:k] for j in range(61))/61
    r=m.retrieval_recall(s,k)
    assert r=={"image_to_text":ir,"text_to_image":tr}
    np.testing.assert_array_equal(s,old)


def transpose(m):
    s=np.array([[3.,2.,1.],[4.,0.,8.],[2.,9.,1.]])
    a=m.retrieval_recall(s,1);b=m.retrieval_recall(s.T,1)
    assert a['image_to_text']==b['text_to_image'] and a['text_to_image']==b['image_to_text']


def invalid(m):
    with np.testing.assert_raises(TypeError):m.retrieval_recall([[1.]],1)
    for a,k in [(np.zeros((0,0)),1),(np.zeros((2,3)),1),(np.zeros((2,2),dtype=np.float32),1),(np.full((2,2),np.inf),1),(np.full((2,2),1e7),1),(np.eye(2),True),(np.eye(2),0),(np.eye(2),3)]:
        with np.testing.assert_raises(ValueError):m.retrieval_recall(a,k)


def scale(m):
    s=np.eye(512,dtype=np.float64)
    assert m.retrieval_recall(s,1)=={"image_to_text":1.,"text_to_image":1.}


TESTS=[("Different retrieval directions","public",directions),("Stable tied candidates","public",ties),("All candidates","public",all_candidates),
       ("Independent ranking oracle","hidden",oracle),("Transpose swaps directions","hidden",transpose),("Validation","hidden",invalid),
       ("Larger collection","hidden",scale)]
