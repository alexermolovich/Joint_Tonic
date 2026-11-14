# Reference solution

Create token indices and identify action slots using the index remainder within a timestep. A broadcast comparison gives the causal lower triangle. Remove only pairs whose query and key are both action slots. Visual rows may still see earlier action placeholders, matching the documented source behavior. Time and result memory are O(L²).

~~~python
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

~~~

This solves the declared component only; it does not reproduce a trained robot policy or a paper benchmark.
