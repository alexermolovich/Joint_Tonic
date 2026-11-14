# Combine Class-Token and Masked-Patch Objectives

Implement class_patch_loss(student_class, teacher_class, student_patch, teacher_patch, mask, temperature, class_weight, patch_weight).

The four value tensors are CPU torch.float32 or torch.float64 with a common dtype. Shapes are student_class(B,V,K), teacher_class(B,2,K), student_patch(B,P,K), teacher_patch(B,P,K), with 1<=B<=32, 2<=V<=8, 2<=K<=2048, 0<=P<=1024 and at most 1,000,000 elements per tensor. mask is CPU torch.bool (B,P). Noncontiguous tensors are valid.

All entries are finite. Student logits have absolute value <=100. Each teacher row is nonnegative and sums to one with rtol=0, atol=1e-6; teachers are already prepared probability targets, not logits. Validate all teacher rows, including unmasked patches. Empty P is allowed.

temperature, class_weight and patch_weight are built-in non-bool int/float; temperature is finite in [0.01,10], weights finite in [0,10]. The first two student views correspond to teacher views 0 and 1; any remaining student views are local crops.

Compute class cross-entropy for each teacher view t in {0,1} against every student view v except v=t, and average over B*2*(V-1) pairs. Compute patch cross-entropy only for mask=True entries in the single supplied aligned patch-view batch, averaging over all selected entries across B and P. If no patches are selected, patch loss is a differentiable zero connected to student_patch. Return class_weight*class_loss + patch_weight*patch_loss as a new zero-dimensional tensor with the input dtype/device.

Student probabilities use log_softmax(student_logits/temperature). Detach teacher targets: gradients flow to both student tensors, never to either teacher. In a grad-enabled call, the output supports backward when a student requires gradients, including empty/all-false masks and zero weights. Preserve input values and masks; no mutation or aliasing.

Non-tensor inputs among the five tensors raise TypeError. All other violations raise ValueError. Scores and losses are dimensionless, views refer to the same underlying image, and patch targets are already aligned to student positions. This specified two-term reduction isolates DINO/iBOT mechanisms; crop generation, Sinkhorn/centering, teacher EMA, KoLeo, distributed reduction, and the complete DINOv2 training recipe are outside the task.

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


## Hints

1. Build class terms for teacher 0 and 1 while skipping the matching student view index.
2. Detach teacher targets before multiplying by log probabilities; do not detach student tensors.
3. Average selected patch terms globally. Keep an explicit differentiable zero when no patch is selected.

