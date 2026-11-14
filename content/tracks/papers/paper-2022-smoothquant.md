---
{
  "schema_version": 1,
  "generated_by": "scripts/generate-paper-tracks.ts",
  "slug": "paper-2022-smoothquant",
  "paper_id": "2022-smoothquant",
  "title": "SmoothQuant: Accurate and Efficient Post-Training Quantization for Large Language Models",
  "status": "bounded-integration-available",
  "primary_url": "https://arxiv.org/abs/2211.10438",
  "source_cards": [
    "research/papers/mlops-data-deployment/2022-smoothquant.md"
  ],
  "paper_aliases": [],
  "category": "mlops-data-deployment",
  "topics": [
    "mlops-data-deployment",
    "smoothquant"
  ],
  "runnable_problem_slugs": [
    "smoothquant-channel-ranges",
    "smoothquant-equivalent-rescaling",
    "edge-inference-release-gate",
    "smoothquant-int8-linear-layer",
    "smoothquant-layer-error-report",
    "smoothquant-calibrated-layer-integration"
  ],
  "proposed_component_count": 0,
  "source_flow_node_count": 3,
  "source_flow_nodes": [
    {
      "card": "2022-smoothquant",
      "node": "stage-1"
    },
    {
      "card": "2022-smoothquant",
      "node": "stage-2"
    },
    {
      "card": "2022-smoothquant",
      "node": "stage-3"
    }
  ],
  "integration_status": "runnable",
  "assessment_status": "runnable",
  "integration_problem_slug": "smoothquant-calibrated-layer-integration"
}
---

# SmoothQuant: Accurate and Efficient Post-Training Quantization for Large Language Models — implementation track

## Orientation and scope

SmoothQuant makes activation quantization easier by moving channel-wise scale into weights through an equivalent linear-layer transformation. Calibration determines the rescaling before low-bit weight-and-activation inference.

The implementation path follows **Measure channel ranges → Apply equivalent rescaling → Quantize and validate**. Work through the original explanation and the atomic tasks below before composing the proposed integration. Published exercises are small, independently graded components; this plan is not a completed or full-paper reproduction.

[Primary source](https://arxiv.org/abs/2211.10438) · [Paper explanation and graph](/projects/2022-smoothquant) · [All paper tracks](../../PAPER_TRACKS.md)

Source cards: [2022-smoothquant](../../../research/papers/mlops-data-deployment/2022-smoothquant.md).

**Available now:** 5 paper-associated runnable components; 1 supporting runnable component. **Proposed:** 0 distinct component ideas, plus integration and assessment. A planned title can be a reviewed blueprint or an unreviewed idea; its presence is not a publication promise.

## Prerequisites and diagnostic

Read the input contracts and locally defined mathematics in the source explanation. Before starting, trace one small input through **Measure channel ranges** and identify the shapes, masks, units, coordinate frames and time conventions that apply. This is a robotics diagnostic, not a general Python or mathematics course.

- **Supporting prerequisite:** [Gate an Edge Model with Accuracy and Latency](/problems/edge-inference-release-gate). Its own contract remains authoritative; it does not implement the entire paper.
- **Supporting prerequisite:** [Measure Per-Channel Activation and Weight Ranges](/problems/smoothquant-channel-ranges). Its own contract remains authoritative; it does not implement the entire paper.
- **Supporting prerequisite:** [Apply an Equivalent Channel Rescaling](/problems/smoothquant-equivalent-rescaling). Its own contract remains authoritative; it does not implement the entire paper.
- **Supporting prerequisite:** [Quantize Weights and Activations to Int8](/problems/smoothquant-int8-linear-layer). Its own contract remains authoritative; it does not implement the entire paper.
- **Supporting prerequisite:** [Validate Layer Output Error After Smoothing](/problems/smoothquant-layer-error-report). Its own contract remains authoritative; it does not implement the entire paper.

## Ordered mechanisms and component tasks

The sequence below is a learning order. The explicit connections retain branching, conditioning and feedback; adjacent entries are not assumed to have interchangeable tensor interfaces.

### 1. Measure channel ranges

<!-- source-flow: 2022-smoothquant#stage-1 -->

Collect activation and weight magnitudes on calibration data.

[Study the mechanism and math](/projects/2022-smoothquant#paper-section-measure-channel-ranges).

- **Runnable paper-associated component:** [Measure Per-Channel Activation and Weight Ranges](/problems/smoothquant-channel-ranges). Measure Per-Channel Activation and Weight Ranges

**Step evidence:** retain a small input/output trace and the invariant described in the linked explanation. Before implementing a proposed task, write and review its blueprint with explicit shapes, units, frames, examples, tolerances and failure behavior.

### 2. Apply equivalent rescaling

<!-- source-flow: 2022-smoothquant#stage-2 -->

Divide activation channels and multiply corresponding weight rows.

[Study the mechanism and math](/projects/2022-smoothquant#paper-section-apply-equivalent-rescaling).

- **Runnable paper-associated component:** [Apply an Equivalent Channel Rescaling](/problems/smoothquant-equivalent-rescaling). Apply an Equivalent Channel Rescaling

**Step evidence:** retain a small input/output trace and the invariant described in the linked explanation. Before implementing a proposed task, write and review its blueprint with explicit shapes, units, frames, examples, tolerances and failure behavior.

### 3. Quantize and validate

<!-- source-flow: 2022-smoothquant#stage-3 -->

Use integer kernels and measure end-to-end accuracy and latency.

[Study the mechanism and math](/projects/2022-smoothquant#paper-section-quantize-and-validate).

- **Runnable supporting prerequisite:** [Gate an Edge Model with Accuracy and Latency](/problems/edge-inference-release-gate). Linear interpolated latency quantiles; accuracy=correct/N; sequential throughput=1000*N/sum(latency_ms). Gate each hardware independently; compare baseline-current slice accuracy to max_slice_drop.
- **Runnable paper-associated component:** [Quantize Weights and Activations to Int8](/problems/smoothquant-int8-linear-layer). Quantize Weights and Activations to Int8
- **Runnable paper-associated component:** [Validate Layer Output Error After Smoothing](/problems/smoothquant-layer-error-report). Validate Layer Output Error After Smoothing
- **Runnable paper-associated component:** [Calibrate and Evaluate a Smoothed Int8 Layer](/problems/smoothquant-calibrated-layer-integration). Compose held-out layer evaluation with calibration-only channel statistics, equivalent smoothing and int8 simulation.

**Step evidence:** retain a small input/output trace and the invariant described in the linked explanation. Before implementing a proposed task, write and review its blueprint with explicit shapes, units, frames, examples, tolerances and failure behavior.

| From | Signal or dependency | To |
|---|---|---|
| Measure channel ranges | channel scales | Apply equivalent rescaling |
| Apply equivalent rescaling | smoothed layers | Quantize and validate |

## Integration exercise

**Runnable bounded integration:** [Calibrate and Evaluate a Smoothed Int8 Layer](/problems/smoothquant-calibrated-layer-integration). This exercises its declared synthetic contract, not the full paper benchmark.

Start with the atomic channel-range, equivalent-scaling, integer-simulation and error-reporting exercises. Then implement one function that consumes calibration observations, separate validation observations, linear weights, candidate exponents and an explicit absolute tolerance.

```text
calibration + original weights -> per-channel maxima
  + candidate smoothing exponents -> guarded equivalent scales
validation features -> scaled layer -> simulated int8 output
  -> fixed float64 reference comparison -> MSE choice + per-row gate
```

Each arrow is a data dependency; this textual pipeline is also the accessible diagram alternative. For $X\in\mathbb R^{N\times C}$, $W\in\mathbb R^{C\times D}$ and positive diagonal $S$, the starting identity is
$$XW=(XS^{-1})(SW).$$
Rounding makes the quantized output different. This project measures that difference using a precisely declared per-token/per-output symmetric recipe. It is original executable numerical work inspired by [SmoothQuant](https://arxiv.org/abs/2211.10438), with synthetic arrays and no pretrained checkpoint.

Out of scope: full transformer conversion, production packing and integer kernels, model training, task-accuracy reproduction, device latency, closed-loop robot safety and headline paper speedups. Calibration-derived scales and validation-based configuration selection are implemented; an untouched final test set is still needed after selecting a configuration.

## Evaluation and failure analysis

**Runnable assessment:** public/hidden cases for the linked integration.

[Open the integration problem](/problems/smoothquant-calibrated-layer-integration). Run exposes the two documented scalar/zero-channel examples. Submit also checks an independent scalar pipeline oracle, calibration-only range statistics, float32 promotion, zero guards, nonzero-subnormal quantizer underflow, repeated-alpha tie behavior, preservation, invalid contracts and a case where minimum MSE disagrees with the absolute-error gate.

The outputs answer distinct questions: output_mse ranks supplied configurations; row_max_abs locates token regressions; accepted applies the explicit tolerance; selected_output preserves the actual quantized prediction. The selected index minimizes MSE across all candidates, even when another candidate alone passes the gate. A failed gate is evidence to inspect, not a reason to silently change the selection policy.

Failure-analysis exercise: introduce a large validation-only activation channel and explain why calibration scales must remain unchanged. Then compare two candidates whose average errors and worst-token errors rank differently. A layer-level pass cannot establish downstream VLM accuracy or safe robot actions.

The reference is tested in the local isolated worker. Starter code, a calibration-leak mutant and a gate-filter mutant are rejected. These tests establish the documented synthetic contract, not performance on the paper's model/data suite.

## Reproducibility deliverable

**Runnable project deliverable:** save the following report in the integration exercise’s Notes. The report is learner-authored, not automatically certified.

Source: [SmoothQuant primary manuscript](https://arxiv.org/abs/2211.10438); library card `research/papers/mlops-data-deployment/2022-smoothquant.md`. All problem prose, code and synthetic fixtures are original; fixtures use CC0-1.0. No paper figures, model weights or research PDFs are product assets.

Runtime: Python3.12.3, NumPy2.2.4, CPU float64 arithmetic with explicit int8 logical codes and int64 accumulation. The local evaluator uses bubblewrap, no network,18s wall,10s CPU,4096MiB address space and64KiB output. Its OCI image digest is pending; do not claim this native-local exercise is qualified for the production data-only protocol.

Inputs define every numerical value; the learner function consumes no random stream. Independent synthetic validation fixtures use PCG64 seeds909 and6. Semantic problem version1.0.0 pins guards1e-6, clamps[1e-6,1e6], signed range[-127,127], ties-to-even rounding and computed-zero quantizer scale fallback1. The latter explicitly includes underflow from nonzero subnormal ranges. Per-problem metadata records the evaluator-source hash.

Calibration rows determine activation ranges; validation rows select the smoothing exponent. Since selection uses validation error, these metrics are not independent final-test estimates. This pipeline omits full-model calibration, layer fusion, packing, hardware benchmarking and downstream robotics evaluation. Document those deviations and any new data, runtime, guard or kernel choices before extending the project.
