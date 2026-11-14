# Worked examples

## Example 1: two global views and one selected patch

~~~python
student_class = torch.zeros((1,2,2), dtype=torch.float64)
teacher_class = torch.tensor([[[1.,0.],[0.,1.]]], dtype=torch.float64)
student_patch = torch.tensor([[[math.log(3.),0.]]], dtype=torch.float64)
teacher_patch = torch.tensor([[[1.,0.]]], dtype=torch.float64)
mask = torch.tensor([[True]])
class_patch_loss(student_class,teacher_class,student_patch,teacher_patch,mask,1.,1.,2.)
# tensor(1.268511325463507, dtype=torch.float64)
~~~

The two cross-view class terms each equal log(2). The patch probability of its target is 3/4, so the total is log(2)+2*log(4/3).

## Example 2: local view and no masked patches

~~~python
student_class = torch.zeros((1,3,2), dtype=torch.float64, requires_grad=True)
teacher_class = torch.tensor([[[1.,0.],[0.,1.]]], dtype=torch.float64)
student_patch = torch.zeros((1,1,2), dtype=torch.float64, requires_grad=True)
teacher_patch = torch.tensor([[[0.25,0.75]]], dtype=torch.float64)
mask = torch.tensor([[False]])
class_patch_loss(student_class,teacher_class,student_patch,teacher_patch,mask,1.,2.,5.)
# tensor(1.3862943611198906, dtype=torch.float64, grad_fn=...)
~~~

There are four class pairs: (teacher,student)=(0,1),(0,2),(1,0),(1,2). Their mean is log(2), not four times log(2). The unselected patch branch contributes zero and has a zero gradient.

