import numpy as np


def prompt_ensemble_classifier(images, prompts, temperature):
    if not isinstance(images,np.ndarray) or not isinstance(prompts,np.ndarray):
        raise TypeError("images and prompts must be arrays")
    if images.dtype!=np.float64 or prompts.dtype!=np.float64 or images.ndim!=2 or prompts.ndim!=3:
        raise ValueError("float64 images(B,D) and prompts(C,P,D) required")
    batch,width=images.shape
    classes,count,prompt_width=prompts.shape
    if not 1<=batch<=256 or not 1<=classes<=1000 or not 1<=count<=64 or not 1<=width<=512 or prompt_width!=width:
        raise ValueError("feature dimensions")
    if images.size>1000000 or prompts.size>1000000:
        raise ValueError("feature budget")
    if type(temperature) not in (int,float) or not 1e-4<=temperature<=1e4:
        raise ValueError("positive bounded temperature")
    norms=[]
    for values in (images,prompts):
        if not np.isfinite(values).all() or (np.abs(values)>1e6).any():
            raise ValueError("finite bounded feature norms")
        norm=np.linalg.norm(values,axis=-1,keepdims=True)
        if (norm<1e-6).any() or (norm>1e6).any():
            raise ValueError("nonzero bounded feature norm")
        norms.append(norm)
    means=(prompts/norms[1]).mean(axis=1)
    mean_norm=np.linalg.norm(means,axis=-1,keepdims=True)
    if (mean_norm<1e-6).any():
        raise ValueError("prompt directions cancel")
    prototypes=means/mean_norm
    logits=(images/norms[0])@prototypes.T/temperature
    return logits,prototypes

