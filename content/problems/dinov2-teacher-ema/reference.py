import math
import torch


def update_teacher_ema(teacher,student,momentum):
    if not isinstance(teacher,dict) or not isinstance(student,dict):
        raise TypeError("Expected parameter dictionaries")
    if type(momentum) not in (int,float) or not 0<=momentum<=1 or not math.isfinite(momentum):
        raise ValueError("Invalid momentum")
    if teacher.keys()!=student.keys() or any(not isinstance(k,str) or not k for k in teacher):
        raise ValueError("Parameter names must match")
    for parameters in (teacher,student):
        total=0
        for value in parameters.values():
            if not isinstance(value,torch.Tensor):
                raise TypeError("Expected tensor parameters")
            if value.device.type!="cpu" or value.dtype not in (torch.float32,torch.float64) or not torch.isfinite(value).all():
                raise ValueError("Invalid parameter tensor")
            total+=value.numel()
        if total>1_000_000:
            raise ValueError("Too many parameters")
    for name in teacher:
        if teacher[name].shape!=student[name].shape or teacher[name].dtype!=student[name].dtype:
            raise ValueError("Mismatched parameter")
    with torch.no_grad():
        return {name:momentum*t+(1-momentum)*student[name] for name,t in teacher.items()}
