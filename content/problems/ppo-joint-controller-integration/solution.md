## Approach

Collect vectorized independent scalar rollouts, compute reverse discounted returns, then take explicitly clipped PPO gradients from the frozen samples. After each iteration evaluate deterministic actions on separate goals. Store every returned trace without aliasing source arrays.

O(I*B*T*epochs + I*M*T) work and O(B*T + I*M) storage, with policy width2.
