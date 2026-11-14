# Build a complete bounded pipeline

Train a bounded policy adapter, generate action tokens, and evaluate held-out robot episodes before a synthetic release.

Work through the linked atomic exercises, then implement the integration in the ordinary coding workspace. The integration accepts original synthetic fixtures and returns an inspectable evidence report.

- [2024-openvla](https://arxiv.org/abs/2406.09246)
- [2022-rt-1](https://arxiv.org/abs/2212.06817)

## Scope

This is an original engineering integration inspired by these sources. It does not download trained weights, train a large model, run a simulator, sign production artifacts, or control hardware. The release verdict evaluates the declared synthetic contract only.
