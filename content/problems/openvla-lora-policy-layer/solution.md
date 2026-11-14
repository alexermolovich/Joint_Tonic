## Approach

Validate tensor shapes and rank, then evaluate the base branch with only its weight detached. Compute the down/up projection and scale by alpha divided by rank. Keep zero-valued adapter contributions connected to autograd. Do not detach the input or mutate requires_grad flags.

See Theory for the mathematical derivation and worked gradient examples.
