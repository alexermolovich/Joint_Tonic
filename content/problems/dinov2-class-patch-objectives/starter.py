import torch
import torch.nn.functional as F


def class_patch_loss(student_class, teacher_class, student_patch, teacher_patch, mask, temperature, class_weight, patch_weight):
    """Return the weighted cross-view class and selected-patch objective."""
    pass

