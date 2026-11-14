# Reproducibility note

Source: [SmoothQuant primary manuscript](https://arxiv.org/abs/2211.10438); library card `research/papers/mlops-data-deployment/2022-smoothquant.md`. All problem prose, code and synthetic fixtures are original; fixtures use CC0-1.0. No paper figures, model weights or research PDFs are product assets.

Runtime: Python3.12.3, NumPy2.2.4, CPU float64 arithmetic with explicit int8 logical codes and int64 accumulation. The local evaluator uses bubblewrap, no network,18s wall,10s CPU,4096MiB address space and64KiB output. Its OCI image digest is pending; do not claim this native-local exercise is qualified for the production data-only protocol.

Inputs define every numerical value; the learner function consumes no random stream. Independent synthetic validation fixtures use PCG64 seeds909 and6. Semantic problem version1.0.0 pins guards1e-6, clamps[1e-6,1e6], signed range[-127,127], ties-to-even rounding and computed-zero quantizer scale fallback1. The latter explicitly includes underflow from nonzero subnormal ranges. Per-problem metadata records the evaluator-source hash.

Calibration rows determine activation ranges; validation rows select the smoothing exponent. Since selection uses validation error, these metrics are not independent final-test estimates. This pipeline omits full-model calibration, layer fusion, packing, hardware benchmarking and downstream robotics evaluation. Document those deviations and any new data, runtime, guard or kernel choices before extending the project.
