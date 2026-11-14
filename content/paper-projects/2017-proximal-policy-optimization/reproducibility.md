# Reproducibility record

Copy this template into the integration workspace Notes after running the project:

- Content version and worker runtime:
- Initial gain and bias:
- Training/evaluation goal arrays:
- Supplied noise seed or exact fixture identity:
- Iterations, horizon, PPO epochs, step size and clip width:
- Final parameter vector:
- Training return trace:
- Held-out final error per target:
- Clip-fraction trace:
- Failure case observed:
- Deliberate simplifications relative to the primary PPO paper:

Synthetic coordinates are normalized joint positions and normalized velocity commands at a fixed0.1-second interval. There are no external datasets, pretrained weights or robot safety claims. The exact fixture and content version are necessary to reproduce an update trace.
