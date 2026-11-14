import torch
import torch.nn.functional as F


def class_patch_loss(student_class,teacher_class,student_patch,teacher_patch,mask,temperature,class_weight,patch_weight):
    values=(student_class,teacher_class,student_patch,teacher_patch)
    if any(not isinstance(x,torch.Tensor) for x in (*values,mask)):
        raise TypeError("five tensor inputs required")
    if any(x.device.type!="cpu" or x.dtype not in (torch.float32,torch.float64) or x.ndim!=3 for x in values):
        raise ValueError("CPU floating three-axis values required")
    if any(x.dtype!=student_class.dtype for x in values):
        raise ValueError("common floating dtype required")
    if mask.device.type!="cpu" or mask.dtype!=torch.bool or mask.ndim!=2:
        raise ValueError("CPU Boolean patch mask required")
    batch,views,classes=student_class.shape
    patch_batch,patches,patch_classes=student_patch.shape
    if not 1<=batch<=32 or not 2<=views<=8 or not 2<=classes<=2048 or not 0<=patches<=1024:
        raise ValueError("dimension bounds")
    if (patch_batch,patch_classes)!=(batch,classes) or teacher_class.shape!=(batch,2,classes) or teacher_patch.shape!=(batch,patches,classes) or mask.shape!=(batch,patches):
        raise ValueError("shape alignment")
    if any(x.numel()>1000000 or not torch.isfinite(x).all() for x in values):
        raise ValueError("finite bounded tensor workload")
    if any((x.abs()>100).any() for x in (student_class,student_patch)):
        raise ValueError("student logit bounds")
    for target in (teacher_class,teacher_patch):
        if (target<0).any() or ((target.double().sum(dim=-1)-1).abs()>1e-6).any():
            raise ValueError("normalized nonnegative teacher rows required")
    if type(temperature) not in (int,float) or not .01<=temperature<=10:
        raise ValueError("student temperature")
    if any(type(w) not in (int,float) or not 0<=w<=10 for w in (class_weight,patch_weight)):
        raise ValueError("loss weights")
    log_class=F.log_softmax(student_class/temperature,dim=-1)
    target_class=teacher_class.detach()
    terms=[]
    for teacher_view in range(2):
        for student_view in range(views):
            if teacher_view!=student_view:
                terms.append(-(target_class[:,teacher_view,:]*log_class[:,student_view,:]).sum(dim=-1))
    class_loss=torch.stack(terms,dim=1).mean()
    if mask.any():
        log_patch=F.log_softmax(student_patch/temperature,dim=-1)
        patch_terms=-(teacher_patch.detach()*log_patch).sum(dim=-1)
        patch_loss=patch_terms[mask].mean()
    else:
        patch_loss=student_patch.sum()*0
    return class_weight*class_loss+patch_weight*patch_loss

