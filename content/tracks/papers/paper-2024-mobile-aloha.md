---
{
  "schema_version": 1,
  "generated_by": "scripts/generate-paper-tracks.ts",
  "slug": "paper-2024-mobile-aloha",
  "paper_id": "2024-mobile-aloha",
  "title": "Mobile ALOHA: Learning Bimanual Mobile Manipulation with Low-Cost Whole-Body Teleoperation",
  "status": "planned",
  "primary_url": "https://arxiv.org/abs/2401.02117",
  "source_cards": [
    "research/papers/robot-learning-rl/2024-mobile-aloha.md"
  ],
  "paper_aliases": [],
  "category": "robot-learning-rl",
  "topics": [
    "mobile manipulation",
    "bimanual imitation learning",
    "whole-body teleoperation"
  ],
  "runnable_problem_slugs": [
    "interpolate-joint-state",
    "validate-robot-episodes",
    "act-sliding-action-chunks",
    "act-cvae-loss",
    "act-temporal-ensembling",
    "diffusion-receding-horizon-window"
  ],
  "proposed_component_count": 3,
  "source_flow_node_count": 3,
  "source_flow_nodes": [
    {
      "card": "2024-mobile-aloha",
      "node": "align"
    },
    {
      "card": "2024-mobile-aloha",
      "node": "learn"
    },
    {
      "card": "2024-mobile-aloha",
      "node": "control"
    }
  ],
  "integration_status": "proposed",
  "assessment_status": "proposed"
}
---

# Mobile ALOHA: Learning Bimanual Mobile Manipulation with Low-Cost Whole-Body Teleoperation — implementation track

## Orientation and scope

Mobile ALOHA extends bimanual demonstrations to tasks that require the base to move while the arms work. The learning problem includes coordinated observation/action records and transfer from existing stationary demonstrations. Its practical contribution combines hardware/data collection with imitation learning; an action-loss function alone is not a reproduction of the system.

The implementation path follows **Align whole-body demonstrations → Learn coordinated action chunks → Execute coordinated feedback**. Work through the original explanation and the atomic tasks below before composing the proposed integration. Published exercises are small, independently graded components; this plan is not a completed or full-paper reproduction.

[Primary source](https://arxiv.org/abs/2401.02117) · [Paper explanation and graph](/projects/2024-mobile-aloha) · [All paper tracks](../../PAPER_TRACKS.md)

Source cards: [2024-mobile-aloha](../../../research/papers/robot-learning-rl/2024-mobile-aloha.md).

**Available now:** 0 paper-associated runnable components; 6 supporting runnable components. **Proposed:** 3 distinct component ideas, plus integration and assessment. A planned title can be a reviewed blueprint or an unreviewed idea; its presence is not a publication promise.

## Prerequisites and diagnostic

Read the input contracts and locally defined mathematics in the source explanation. Before starting, trace one small input through **Align whole-body demonstrations** and identify the shapes, masks, units, coordinate frames and time conventions that apply. This is a robotics diagnostic, not a general Python or mathematics course.

- **Supporting prerequisite:** [Interpolate Joint State at Camera Time](/problems/interpolate-joint-state). Its own contract remains authoritative; it does not implement the entire paper.
- **Supporting prerequisite:** [Validate a Multimodal Robot Episode Schema](/problems/validate-robot-episodes). Its own contract remains authoritative; it does not implement the entire paper.
- **Supporting prerequisite:** [Build Sliding Action Chunks with Padding Masks](/problems/act-sliding-action-chunks). Its own contract remains authoritative; it does not implement the entire paper.
- **Supporting prerequisite:** [Compute a Masked CVAE Reconstruction and KL Loss](/problems/act-cvae-loss). Its own contract remains authoritative; it does not implement the entire paper.
- **Supporting prerequisite:** [Blend Overlapping Action Chunks with Temporal Ensembling](/problems/act-temporal-ensembling). Its own contract remains authoritative; it does not implement the entire paper.
- **Supporting prerequisite:** [Execute a Receding-Horizon Action Window](/problems/diffusion-receding-horizon-window). Its own contract remains authoritative; it does not implement the entire paper.

## Ordered mechanisms and component tasks

The sequence below is a learning order. The explicit connections retain branching, conditioning and feedback; adjacent entries are not assumed to have interchangeable tensor interfaces.

### 1. Align whole-body demonstrations

<!-- source-flow: 2024-mobile-aloha#align -->

Align whole-body demonstrations. See the original explanation and component status below.

[Study the mechanism and math](/projects/2024-mobile-aloha#paper-section-align-whole-body-demonstrations).

- **Runnable supporting prerequisite:** [Interpolate Joint State at Camera Time](/problems/interpolate-joint-state). Align unwrapped encoder angles to camera timestamps without crossing sensor dropouts.
- **Runnable supporting prerequisite:** [Validate a Multimodal Robot Episode Schema](/problems/validate-robot-episodes). A signal's missing fraction is missing_rows / T. A timestamp must be finite numeric, and each valid adjacent pair must strictly increase.
- **Proposed component, not runnable:** Normalize Heterogeneous Robot Observation Schemas.

**Step evidence:** retain a small input/output trace and the invariant described in the linked explanation. Before implementing a proposed task, write and review its blueprint with explicit shapes, units, frames, examples, tolerances and failure behavior.

### 2. Learn coordinated action chunks

<!-- source-flow: 2024-mobile-aloha#learn -->

Learn coordinated action chunks. See the original explanation and component status below.

[Study the mechanism and math](/projects/2024-mobile-aloha#paper-section-learn-coordinated-action-chunks).

- **Runnable supporting prerequisite:** [Build Sliding Action Chunks with Padding Masks](/problems/act-sliding-action-chunks). Extract fixed-horizon action windows from one episode while marking right-padding and preserving requested start order.
- **Runnable supporting prerequisite:** [Compute a Masked CVAE Reconstruction and KL Loss](/problems/act-cvae-loss). Isolate ACT's L1 reconstruction plus diagonal-Gaussian KL objective.
- **Proposed component, not runnable:** Mix Static and Mobile Demonstration Batches.

**Step evidence:** retain a small input/output trace and the invariant described in the linked explanation. Before implementing a proposed task, write and review its blueprint with explicit shapes, units, frames, examples, tolerances and failure behavior.

### 3. Execute coordinated feedback

<!-- source-flow: 2024-mobile-aloha#control -->

Execute coordinated feedback. See the original explanation and component status below.

[Study the mechanism and math](/projects/2024-mobile-aloha#paper-section-execute-coordinated-feedback).

- **Runnable supporting prerequisite:** [Blend Overlapping Action Chunks with Temporal Ensembling](/problems/act-temporal-ensembling). Align predictions to one target control tick and combine eligible chunks with ACT’s oldest-first exponential weighting.
- **Runnable supporting prerequisite:** [Execute a Receding-Horizon Action Window](/problems/diffusion-receding-horizon-window). Extract the controller-supported prefix of a predicted future trajectory after a specified alignment offset.
- **Proposed component, not runnable:** Measure Closed-Loop Latency and Action Dropouts.

**Step evidence:** retain a small input/output trace and the invariant described in the linked explanation. Before implementing a proposed task, write and review its blueprint with explicit shapes, units, frames, examples, tolerances and failure behavior.

| From | Signal or dependency | To |
|---|---|---|
| Align whole-body demonstrations | validated component output | Learn coordinated action chunks |
| Learn coordinated action chunks | validated component output | Execute coordinated feedback |

## Integration exercise

**Proposed exercise — not runnable yet.** Create paired synthetic stationary and mobile demonstrations with separate arm and base channels. Normalize their observation/action schemas, mix labeled episodes and build ACT-style chunks before temporal-ensemble replay. Missing mobile-base channels require an explicit mask rather than an invented demonstration command.

The integration boundary is the selected data, objective and update/evaluation calculations; the tiny fixture is not evidence of successful policy learning on the paper benchmark. Treat any stubbed learned stage as a named fixture, never as measured model capability. Author original synthetic data and record its generation rules; external datasets or assets need a separate provenance and license review.

Deliver an executable fixture generator, the component wiring, a compact expected-output trace and a report of the remaining differences from [the paper](/projects/2024-mobile-aloha). Proposed pieces must pass blueprint review and isolated evaluation before this integration becomes an available exercise.

## Evaluation and failure analysis

**Proposed assessment — not runnable yet.** Verify source-mixture counts, embodiment channel alignment and action-window timing. Measure arm and base errors separately; the fixture cannot establish that stationary-data co-training improves real mobile manipulation.

Use one clean baseline and a separately recorded fault case: cross an episode boundary, shift an action relative to its observation, or alter one reward/goal label; attribute the resulting metric change. Identify the affected stage and report its intermediate evidence. Do not average away the failing case.

Before grading, define an independent oracle, exact-versus-tolerant comparisons, allowed dtypes/devices, empty/minimal cases, invalid-input behavior and resource bounds. Compare failure detection and mathematical correctness separately from timing. A synthetic result establishes only the declared component contract; paper benchmark scores and physical safety require their own protocol.

## Reproducibility deliverable

**Proposed final artifact:** an original implementation/model card for **Mobile ALOHA: Learning Bimanual Mobile Manipulation with Low-Cost Whole-Body Teleoperation** containing the source revision, exercised and stubbed stages, and an explicit list of omitted paper experiments.

Record episode alignment, discount/termination rules, action units, train/evaluation split, update order and policy version. Pin problem/content versions, code revision, Python/dependency versions, evaluator identity, deterministic seeds and fixture hashes. Include the baseline/fault report and runtime observations. If any component updates parameters, record the update count and trainable state; otherwise state that no model was trained.

Package the fixture and expected trace with a machine-readable manifest. Replaying the same manifest must recover the same evidence within declared tolerances. Record limitations and the next unimplemented mechanism; completion of this proposal must not be labeled full-paper reproduction. Research PDFs remain local reference inputs, with canonical sources linked rather than redistributed.
