---
{
  "schema_version": 1,
  "generated_by": "scripts/generate-paper-tracks.ts",
  "slug": "paper-2024-3d-diffusion-policy",
  "paper_id": "2024-3d-diffusion-policy",
  "title": "3D Diffusion Policy: Generalizable Visuomotor Policy Learning via Simple 3D Representations",
  "status": "planned",
  "primary_url": "https://arxiv.org/abs/2403.03954",
  "source_cards": [
    "research/papers/robot-learning-rl/2024-3d-diffusion-policy.md"
  ],
  "paper_aliases": [],
  "category": "robot-learning-rl",
  "topics": [
    "robot-learning-rl",
    "3d-diffusion-policy"
  ],
  "runnable_problem_slugs": [
    "pointnet-symmetric-pooling",
    "se3-transform-points",
    "diffusion-action-noising",
    "diffusion-conditional-noise-loss",
    "diffusion-receding-horizon-window"
  ],
  "proposed_component_count": 3,
  "source_flow_node_count": 3,
  "source_flow_nodes": [
    {
      "card": "2024-3d-diffusion-policy",
      "node": "stage-1"
    },
    {
      "card": "2024-3d-diffusion-policy",
      "node": "stage-2"
    },
    {
      "card": "2024-3d-diffusion-policy",
      "node": "stage-3"
    }
  ],
  "integration_status": "proposed",
  "assessment_status": "proposed"
}
---

# 3D Diffusion Policy: Generalizable Visuomotor Policy Learning via Simple 3D Representations — implementation track

## Orientation and scope

3D Diffusion Policy, or DP3, conditions action diffusion on a compact point-cloud representation and robot state. The central change is spatial observation encoding, not a replacement of the action diffusion principle.

The implementation path follows **Prepare sparse 3D observations → Train conditioned action diffusion → Sample and execute a chunk**. Work through the original explanation and the atomic tasks below before composing the proposed integration. Published exercises are small, independently graded components; this plan is not a completed or full-paper reproduction.

[Primary source](https://arxiv.org/abs/2403.03954) · [Paper explanation and graph](/projects/2024-3d-diffusion-policy) · [All paper tracks](../../PAPER_TRACKS.md)

Source cards: [2024-3d-diffusion-policy](../../../research/papers/robot-learning-rl/2024-3d-diffusion-policy.md).

**Available now:** 0 paper-associated runnable components; 5 supporting runnable components. **Proposed:** 3 distinct component ideas, plus integration and assessment. A planned title can be a reviewed blueprint or an unreviewed idea; its presence is not a publication promise.

## Prerequisites and diagnostic

Read the input contracts and locally defined mathematics in the source explanation. Before starting, trace one small input through **Prepare sparse 3D observations** and identify the shapes, masks, units, coordinate frames and time conventions that apply. This is a robotics diagnostic, not a general Python or mathematics course.

- **Supporting prerequisite:** [Prove Permutation Invariance with Symmetric Pooling](/problems/pointnet-symmetric-pooling). Its own contract remains authoritative; it does not implement the entire paper.
- **Supporting prerequisite:** [Apply an SE(3) Transform to Batched Points](/problems/se3-transform-points). Its own contract remains authoritative; it does not implement the entire paper.
- **Supporting prerequisite:** [Add Noise to an Action Sequence](/problems/diffusion-action-noising). Its own contract remains authoritative; it does not implement the entire paper.
- **Supporting prerequisite:** [Compute a Conditional Noise-Prediction Loss](/problems/diffusion-conditional-noise-loss). Its own contract remains authoritative; it does not implement the entire paper.
- **Supporting prerequisite:** [Execute a Receding-Horizon Action Window](/problems/diffusion-receding-horizon-window). Its own contract remains authoritative; it does not implement the entire paper.

## Ordered mechanisms and component tasks

The sequence below is a learning order. The explicit connections retain branching, conditioning and feedback; adjacent entries are not assumed to have interchangeable tensor interfaces.

### 1. Prepare sparse 3D observations

<!-- source-flow: 2024-3d-diffusion-policy#stage-1 -->

Crop and sample point clouds in a declared coordinate frame.

[Study the mechanism and math](/projects/2024-3d-diffusion-policy#paper-section-prepare-sparse-3d-observations).

- **Runnable supporting prerequisite:** [Prove Permutation Invariance with Symmetric Pooling](/problems/pointnet-symmetric-pooling). Pool valid point features channel by channel and demonstrate that point order cannot change the result.
- **Runnable supporting prerequisite:** [Apply an SE(3) Transform to Batched Points](/problems/se3-transform-points). Move camera-frame points into the world frame using a rigid transform.
- **Proposed component, not runnable:** Sample and Normalize Scene Points.

**Step evidence:** retain a small input/output trace and the invariant described in the linked explanation. Before implementing a proposed task, write and review its blueprint with explicit shapes, units, frames, examples, tolerances and failure behavior.

### 2. Train conditioned action diffusion

<!-- source-flow: 2024-3d-diffusion-policy#stage-2 -->

Predict corruption noise from point features and robot state.

[Study the mechanism and math](/projects/2024-3d-diffusion-policy#paper-section-train-conditioned-action-diffusion).

- **Runnable supporting prerequisite:** [Add Noise to an Action Sequence](/problems/diffusion-action-noising). Gather one cumulative signal coefficient per batch item and broadcast over horizon/action axes; mix clean actions and supplied noise with square-root weights.
- **Runnable supporting prerequisite:** [Compute a Conditional Noise-Prediction Loss](/problems/diffusion-conditional-noise-loss). Reduce predicted-versus-supplied diffusion noise errors over exactly the valid action scalars while preserving training gradients.
- **Proposed component, not runnable:** Condition an Action Denoiser on a Point Feature.

**Step evidence:** retain a small input/output trace and the invariant described in the linked explanation. Before implementing a proposed task, write and review its blueprint with explicit shapes, units, frames, examples, tolerances and failure behavior.

### 3. Sample and execute a chunk

<!-- source-flow: 2024-3d-diffusion-policy#stage-3 -->

Denoise actions and replan from new 3D observations.

[Study the mechanism and math](/projects/2024-3d-diffusion-policy#paper-section-sample-and-execute-a-chunk).

- **Runnable supporting prerequisite:** [Execute a Receding-Horizon Action Window](/problems/diffusion-receding-horizon-window). Extract the controller-supported prefix of a predicted future trajectory after a specified alignment offset.
- **Proposed component, not runnable:** Evaluate Viewpoint and Geometry Shift.

**Step evidence:** retain a small input/output trace and the invariant described in the linked explanation. Before implementing a proposed task, write and review its blueprint with explicit shapes, units, frames, examples, tolerances and failure behavior.

| From | Signal or dependency | To |
|---|---|---|
| Prepare sparse 3D observations | 3D context | Train conditioned action diffusion |
| Train conditioned action diffusion | trained denoiser | Sample and execute a chunk |

## Integration exercise

**Proposed exercise — not runnable yet.** Construct a few synthetic episodes containing observations, actions, rewards and termination flags, with known targets or an analytic low-dimensional transition function. Compose the selected mechanisms in the declared flow, beginning with **Prepare sparse 3D observations** and ending with **Sample and execute a chunk**. Save each intermediate artifact so a learner can locate a mismatch at its originating stage.

The integration boundary is the selected data, objective and update/evaluation calculations; the tiny fixture is not evidence of successful policy learning on the paper benchmark. Treat any stubbed learned stage as a named fixture, never as measured model capability. Author original synthetic data and record its generation rules; external datasets or assets need a separate provenance and license review.

Deliver an executable fixture generator, the component wiring, a compact expected-output trace and a report of the remaining differences from [the paper](/projects/2024-3d-diffusion-policy). Proposed pieces must pass blueprint review and isolated evaluation before this integration becomes an available exercise.

## Evaluation and failure analysis

**Proposed assessment — not runnable yet.** For the **Prepare sparse 3D observations → Sample and execute a chunk** fixture, compare returns, losses, action outputs or update targets with an independently computed episode trace; report termination/truncation and task slices explicitly.

Use one clean baseline and a separately recorded fault case: cross an episode boundary, shift an action relative to its observation, or alter one reward/goal label; attribute the resulting metric change. Identify the affected stage and report its intermediate evidence. Do not average away the failing case.

Before grading, define an independent oracle, exact-versus-tolerant comparisons, allowed dtypes/devices, empty/minimal cases, invalid-input behavior and resource bounds. Compare failure detection and mathematical correctness separately from timing. A synthetic result establishes only the declared component contract; paper benchmark scores and physical safety require their own protocol.

## Reproducibility deliverable

**Proposed final artifact:** an original implementation/model card for **3D Diffusion Policy: Generalizable Visuomotor Policy Learning via Simple 3D Representations** containing the source revision, exercised and stubbed stages, and an explicit list of omitted paper experiments.

Record episode alignment, discount/termination rules, action units, train/evaluation split, update order and policy version. Pin problem/content versions, code revision, Python/dependency versions, evaluator identity, deterministic seeds and fixture hashes. Include the baseline/fault report and runtime observations. If any component updates parameters, record the update count and trainable state; otherwise state that no model was trained.

Package the fixture and expected trace with a machine-readable manifest. Replaying the same manifest must recover the same evidence within declared tolerances. Record limitations and the next unimplemented mechanism; completion of this proposal must not be labeled full-paper reproduction. Research PDFs remain local reference inputs, with canonical sources linked rather than redistributed.
