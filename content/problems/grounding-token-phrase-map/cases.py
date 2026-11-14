import numpy as np
from numpy.testing import assert_array_equal
def example(m):assert_array_equal(m.phrase_token_map(np.array([[0,0],[0,3],[4,7],[8,11]],dtype=np.int64),np.array([[4,11]],dtype=np.int64),11),[[False,False,True,True]])
def touching(m):assert_array_equal(m.phrase_token_map(np.array([[2,5]],dtype=np.int64),np.array([[4,6],[5,6]],dtype=np.int64),6),[[True],[False]])
def oracle(m):
    t=np.array([[7,9],[0,4],[4,4],[3,8]],dtype=np.int64);p=np.array([[2,6],[0,1],[8,10]],dtype=np.int64);r=m.phrase_token_map(t,p,10)
    expected=[[bool(set(range(a,b))&set(range(c,d))) for c,d in t] for a,b in p];assert_array_equal(r,expected)
    assert m.phrase_token_map(np.empty((0,2),dtype=np.int64),p,10).shape==(3,0)
    assert m.phrase_token_map(t,np.empty((0,2),dtype=np.int64),10).shape==(0,4)
def invalid(m):
    for t,p,n in [(np.array([[0,2]],dtype=np.int64),np.array([[1,1]],dtype=np.int64),2),(np.array([[2,1]],dtype=np.int64),np.array([[0,1]],dtype=np.int64),2),(np.array([[0,3]],dtype=np.int64),np.array([[0,1]],dtype=np.int64),2),(np.zeros((1,2)),np.array([[0,1]],dtype=np.int64),2)]:
        with np.testing.assert_raises(ValueError):m.phrase_token_map(t,p,n)
TESTS=[('Phrase coverage','public',example),('Half-open boundaries','public',touching),('Set-intersection oracle and empty axes','hidden',oracle),('Validation','hidden',invalid)]

def scale_storage(m):
    raw=np.column_stack((np.arange(2048),np.zeros(2048,dtype=np.int64),np.arange(2048)+1,np.zeros(2048,dtype=np.int64)));tokens=raw[:,::2];phrases=np.array([[0,1024],[1024,2048]],dtype=np.int64);before=tokens.copy();out=m.phrase_token_map(tokens,phrases,2048)
    assert out.shape==(2,2048) and out.dtype==np.bool_;assert_array_equal(out.sum(1),[1024,1024]);assert_array_equal(tokens,before)
    assert not np.shares_memory(out,tokens) and not np.shares_memory(out,phrases)

TESTS.append(('Scale noncontiguous and noalias','hidden',scale_storage))
