# Hints

1. Build class terms for teacher 0 and 1 while skipping the matching student view index.
2. Detach teacher targets before multiplying by log probabilities; do not detach student tensors.
3. Average selected patch terms globally. Keep an explicit differentiable zero when no patch is selected.

