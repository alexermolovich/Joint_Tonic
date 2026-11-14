import torch


def close(a,b):torch.testing.assert_close(a,torch.as_tensor(b,dtype=a.dtype),rtol=1e-6,atol=1e-7)
def args():return [torch.tensor(x,dtype=torch.float64) for x in ([[[1,2],[3,4]]],[[1,0],[0,2]],[1,-1],[10,20],[[.1,.2],[.3,.4],[.5,.6]])]


def two_patches(m):close(m.build_vit_tokens(*args()),[[[10.1,20.2],[2.3,3.4],[4.5,7.6]]])


def scalar(m):
    a=[torch.tensor(x,dtype=torch.float32) for x in ([[[2]]],[[3]],[1],[-2],[[.5],[1]])]
    close(m.build_vit_tokens(*a),[[[-1.5],[8]]])


def empty(m):
    a=args();a[0]=torch.empty((0,2,2),dtype=torch.float64)
    assert m.build_vit_tokens(*a).shape==(0,3,2)


def gradients(m):
    a=args()
    for x in a:x.requires_grad_()
    y=m.build_vit_tokens(*a)
    grads=torch.autograd.grad(y.sum(),a)
    close(grads[0],[[[1,2],[1,2]]]);close(grads[1],[[4,4],[6,6]])
    close(grads[2],[2,2]);close(grads[3],[1,1]);close(grads[4],torch.ones((3,2)))


def batch_layout(m):
    a=args();a[0]=torch.tensor([[[1.,3.],[2.,4.]],[[5.,7.],[6.,8.]]],dtype=torch.float64).transpose(1,2)
    old=[x.clone() for x in a]
    y=m.build_vit_tokens(*a)
    close(y[1],[[10.1,20.2],[6.3,11.4],[8.5,15.6]])
    for x,z in zip(a,old):close(x,z)
    assert all(y.data_ptr()!=x.data_ptr() for x in a)


def invalid(m):
    def expect(kind,a):
        try:m.build_vit_tokens(*a)
        except kind:return
        raise AssertionError("Expected "+kind.__name__)
    a=args();a[0]=[[[1,2]]];expect(TypeError,a)
    for index,bad in [(0,torch.zeros((1,0,2),dtype=torch.float64)),(1,torch.ones((3,2),dtype=torch.float64)),(2,torch.zeros((1,2),dtype=torch.float64)),(3,torch.zeros(2,dtype=torch.float32)),(4,torch.full((3,2),float('nan'),dtype=torch.float64)),(3,torch.full((2,),101.,dtype=torch.float64))]:
        a=args();a[index]=bad;expect(ValueError,a)


def scale(m):
    p=torch.ones((8,128,16));w=torch.ones((16,32));z=torch.zeros(32);pos=torch.zeros((129,32))
    y=m.build_vit_tokens(p,w,z,z,pos)
    assert y.shape==(8,129,32)
    close(y[:,0],torch.zeros((8,32)));close(y[:,1:],torch.full((8,128,32),16.))


TESTS=[("Two patch sequence","public",two_patches),("One feature token","public",scalar),("Empty batch","public",empty),
       ("All gradient paths","hidden",gradients),("Independent batches and layout","hidden",batch_layout),
       ("Validation","hidden",invalid),("Realistic token batch","hidden",scale)]
