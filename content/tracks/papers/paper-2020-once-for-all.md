---
{
  "schema_version": 1,
  "generated_by": "scripts/generate-paper-tracks.ts",
  "slug": "paper-2020-once-for-all",
  "paper_id": "2020-once-for-all",
  "title": "Once-for-All: Train One Network and Specialize it for Efficient Deployment",
  "status": "planned",
  "primary_url": "https://arxiv.org/abs/1908.09791",
  "source_cards": [
    "research/papers/mlops-sim2real/2020-once-for-all.md"
  ],
  "paper_aliases": [],
  "category": "mlops-sim2real",
  "topics": [
    "efficient-inference",
    "neural-architecture-search",
    "weight-sharing",
    "edge-deployment",
    "pareto-optimization"
  ],
  "runnable_problem_slugs": [
    "progressive-shrinking-curriculum",
    "extract-elastic-subnetwork",
    "edge-inference-release-gate",
    "pareto-edge-model-selection",
    "package-edge-model-artifact"
  ],
  "proposed_component_count": 0,
  "source_flow_node_count": 3,
  "source_flow_nodes": [
    {
      "card": "2020-once-for-all",
      "node": "stage-1"
    },
    {
      "card": "2020-once-for-all",
      "node": "stage-2"
    },
    {
      "card": "2020-once-for-all",
      "node": "stage-3"
    }
  ],
  "integration_status": "proposed",
  "assessment_status": "proposed"
}
---

# Once-for-All: Train One Network and Specialize it for Efficient Deployment — implementation track

## Orientation and scope

Once-for-All trains an elastic network that contains many candidate subnetworks, then specializes a suitable subnetwork for a hardware target. Progressive shrinking introduces smaller depth, width, kernel, and resolution choices after larger configurations have learned useful weights. This separates expensive shared training from cheaper device-specific architecture selection.

The implementation path follows **Train elastic weights → Extract a valid subnetwork → Specialize for hardware**. Work through the original explanation and the atomic tasks below before composing the proposed integration. Published exercises are small, independently graded components; this plan is not a completed or full-paper reproduction.

[Primary source](https://arxiv.org/abs/1908.09791) · [Paper explanation and graph](/projects/2020-once-for-all) · [All paper tracks](../../PAPER_TRACKS.md)

Source cards: [2020-once-for-all](../../../research/papers/mlops-sim2real/2020-once-for-all.md).

**Available now:** 4 paper-associated runnable components; 1 supporting runnable component. **Proposed:** 0 distinct component ideas, plus integration and assessment. A planned title can be a reviewed blueprint or an unreviewed idea; its presence is not a publication promise.

## Prerequisites and diagnostic

Read the input contracts and locally defined mathematics in the source explanation. Before starting, trace one small input through **Train elastic weights** and identify the shapes, masks, units, coordinate frames and time conventions that apply. This is a robotics diagnostic, not a general Python or mathematics course.

- **Supporting prerequisite:** [Gate an Edge Model with Accuracy and Latency](/problems/edge-inference-release-gate). Its own contract remains authoritative; it does not implement the entire paper.

## Ordered mechanisms and component tasks

The sequence below is a learning order. The explicit connections retain branching, conditioning and feedback; adjacent entries are not assumed to have interchangeable tensor interfaces.

### 1. Train elastic weights

<!-- source-flow: 2020-once-for-all#stage-1 -->

Support several architecture choices through staged shared training.

[Study the mechanism and math](/projects/2020-once-for-all#paper-section-train-elastic-weights).

- **Runnable paper-associated component:** [Sample a Progressive-Shrinking Curriculum](/problems/progressive-shrinking-curriculum). Sample a Progressive-Shrinking Curriculum

**Step evidence:** retain a small input/output trace and the invariant described in the linked explanation. Before implementing a proposed task, write and review its blueprint with explicit shapes, units, frames, examples, tolerances and failure behavior.

### 2. Extract a valid subnetwork

<!-- source-flow: 2020-once-for-all#stage-2 -->

Select coherent depths, widths, kernels, and resolution with appropriate statistics.

[Study the mechanism and math](/projects/2020-once-for-all#paper-section-extract-a-valid-subnetwork).

- **Runnable paper-associated component:** [Extract a Depth, Width, and Kernel Subnetwork](/problems/extract-elastic-subnetwork). Extract a Depth, Width, and Kernel Subnetwork

**Step evidence:** retain a small input/output trace and the invariant described in the linked explanation. Before implementing a proposed task, write and review its blueprint with explicit shapes, units, frames, examples, tolerances and failure behavior.

### 3. Specialize for hardware

<!-- source-flow: 2020-once-for-all#stage-3 -->

Search for a high-quality subnetwork under a measured device constraint.

[Study the mechanism and math](/projects/2020-once-for-all#paper-section-specialize-for-hardware).

- **Runnable supporting prerequisite:** [Gate an Edge Model with Accuracy and Latency](/problems/edge-inference-release-gate). Linear interpolated latency quantiles; accuracy=correct/N; sequential throughput=1000*N/sum(latency_ms). Gate each hardware independently; compare baseline-current slice accuracy to max_slice_drop.
- **Runnable paper-associated component:** [Select a Pareto Model Under Accuracy and Latency Limits](/problems/pareto-edge-model-selection). Select a Pareto Model Under Accuracy and Latency Limits
- **Runnable paper-associated component:** [Package and Verify an Edge Model Artifact](/problems/package-edge-model-artifact). Package and Verify an Edge Model Artifact

**Step evidence:** retain a small input/output trace and the invariant described in the linked explanation. Before implementing a proposed task, write and review its blueprint with explicit shapes, units, frames, examples, tolerances and failure behavior.

| From | Signal or dependency | To |
|---|---|---|
| Train elastic weights | elastic supernetwork | Extract a valid subnetwork |
| Extract a valid subnetwork | candidate subnetworks | Specialize for hardware |

## Integration exercise

**Proposed exercise — not runnable yet.** Construct a small synthetic pipeline/configuration graph and scenario metric records, or bounded randomization samples where the selected mechanism requires them. Compose the selected mechanisms in the declared flow, beginning with **Train elastic weights** and ending with **Specialize for hardware**. Save each intermediate artifact so a learner can locate a mismatch at its originating stage.

The integration boundary is data, dependency, evaluation and transfer-check calculations; synthetic acceptance is not evidence of safe deployment or sim-to-real success. Treat any stubbed learned stage as a named fixture, never as measured model capability. Author original synthetic data and record its generation rules; external datasets or assets need a separate provenance and license review.

Deliver an executable fixture generator, the component wiring, a compact expected-output trace and a report of the remaining differences from [the paper](/projects/2020-once-for-all). Proposed pieces must pass blueprint review and isolated evaluation before this integration becomes an available exercise.

## Evaluation and failure analysis

**Proposed assessment — not runnable yet.** For the **Train elastic weights → Specialize for hardware** fixture, compare dependency and release decisions with known graph/record fixtures and report scenario-level metrics before aggregate conclusions.

Use one clean baseline and a separately recorded fault case: invalidate a dependency, remove one hardware/scenario slice, or perturb a physical parameter outside the declared envelope; expose the precise failure. Identify the affected stage and report its intermediate evidence. Do not average away the failing case.

Before grading, define an independent oracle, exact-versus-tolerant comparisons, allowed dtypes/devices, empty/minimal cases, invalid-input behavior and resource bounds. Compare failure detection and mathematical correctness separately from timing. A synthetic result establishes only the declared component contract; paper benchmark scores and physical safety require their own protocol.

## Reproducibility deliverable

**Proposed final artifact:** an original implementation/model card for **Once-for-All: Train One Network and Specialize it for Efficient Deployment** containing the source revision, exercised and stubbed stages, and an explicit list of omitted paper experiments.

Record pipeline/configuration digest, simulator or hardware label, randomization bounds, timing units, scenario definitions and release criteria. Pin problem/content versions, code revision, Python/dependency versions, evaluator identity, deterministic seeds and fixture hashes. Include the baseline/fault report and runtime observations. If any component updates parameters, record the update count and trainable state; otherwise state that no model was trained.

Package the fixture and expected trace with a machine-readable manifest. Replaying the same manifest must recover the same evidence within declared tolerances. Record limitations and the next unimplemented mechanism; completion of this proposal must not be labeled full-paper reproduction. Research PDFs remain local reference inputs, with canonical sources linked rather than redistributed.
