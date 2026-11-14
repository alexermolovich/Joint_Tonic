import numpy as np


def rt1_attention_mask(steps, visual_tokens, action_tokens):
    if any(type(x) is not int for x in (steps, visual_tokens, action_tokens)):
        raise TypeError("arguments must be built-in non-bool integers")
    if any(not 1 <= x <= 1024 for x in (steps, visual_tokens, action_tokens)):
        raise ValueError("token dimensions outside bounds")
    length = steps * (visual_tokens + action_tokens)
    if length > 1024:
        raise ValueError("combined sequence exceeds 1024 tokens")
    indices = np.arange(length)
    is_action = indices % (visual_tokens + action_tokens) >= visual_tokens
    return (indices[None, :] <= indices[:, None]) & ~(is_action[:, None] & is_action[None, :])
