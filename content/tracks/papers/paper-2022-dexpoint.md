---
{
  "schema_version": 1,
  "generated_by": "scripts/generate-paper-tracks.ts",
  "slug": "paper-2022-dexpoint",
  "paper_id": "2022-dexpoint",
  "title": "DexPoint: Generalizable Point Cloud Reinforcement Learning for Sim-to-Real Dexterous Manipulation",
  "status": "planned",
  "primary_url": "https://arxiv.org/abs/2211.09423",
  "source_cards": [
    "research/papers/humanoid-dexterity-tactile/2022-dexpoint.md"
  ],
  "paper_aliases": [],
  "category": "humanoid-dexterity-tactile",
  "topics": [
    "humanoid-dexterity-tactile",
    "dexpoint"
  ],
  "runnable_problem_slugs": [
    "se3-transform-points",
    "pointnet-symmetric-pooling"
  ],
  "proposed_component_count": 3,
  "source_flow_node_count": 3,
  "source_flow_nodes": [
    {
      "card": "2022-dexpoint",
      "node": "stage-1"
    },
    {
      "card": "2022-dexpoint",
      "node": "stage-2"
    },
    {
      "card": "2022-dexpoint",
      "node": "stage-3"
    }
  ],
  "integration_status": "proposed",
  "assessment_status": "proposed"
}
---

# DexPoint: Generalizable Point Cloud Reinforcement Learning for Sim-to-Real Dexterous Manipulation — implementation track

## Orientation and scope

DexPoint learns dexterous manipulation from point clouds and augments observations with imagined hand geometry from robot kinematics. Contact-aware rewards and geometric observations support transfer to unseen objects and real hardware.

The implementation path follows **Construct observed and imagined points → Learn contact-aware behavior → Transfer to new objects**. Work through the original explanation and the atomic tasks below before composing the proposed integration. Published exercises are small, independently graded components; this plan is not a completed or full-paper reproduction.

[Primary source](https://arxiv.org/abs/2211.09423) · [Paper explanation and graph](/projects/2022-dexpoint) · [All paper tracks](../../PAPER_TRACKS.md)

Source cards: [2022-dexpoint](../../../research/papers/humanoid-dexterity-tactile/2022-dexpoint.md).

**Available now:** 0 paper-associated runnable components; 2 supporting runnable components. **Proposed:** 3 distinct component ideas, plus integration and assessment. A planned title can be a reviewed blueprint or an unreviewed idea; its presence is not a publication promise.

## Prerequisites and diagnostic

Read the input contracts and locally defined mathematics in the source explanation. Before starting, trace one small input through **Construct observed and imagined points** and identify the shapes, masks, units, coordinate frames and time conventions that apply. This is a robotics diagnostic, not a general Python or mathematics course.

- **Supporting prerequisite:** [Apply an SE(3) Transform to Batched Points](/problems/se3-transform-points). Its own contract remains authoritative; it does not implement the entire paper.
- **Supporting prerequisite:** [Prove Permutation Invariance with Symmetric Pooling](/problems/pointnet-symmetric-pooling). Its own contract remains authoritative; it does not implement the entire paper.

## Ordered mechanisms and component tasks

The sequence below is a learning order. The explicit connections retain branching, conditioning and feedback; adjacent entries are not assumed to have interchangeable tensor interfaces.

### 1. Construct observed and imagined points

<!-- source-flow: 2022-dexpoint#stage-1 -->

Combine object sensing with a kinematic hand representation.

[Study the mechanism and math](/projects/2022-dexpoint#paper-section-construct-observed-and-imagined-points).

- **Runnable supporting prerequisite:** [Apply an SE(3) Transform to Batched Points](/problems/se3-transform-points). Move camera-frame points into the world frame using a rigid transform.
- **Proposed component, not runnable:** Merge Observed and Imagined Hand Point Clouds.

**Step evidence:** retain a small input/output trace and the invariant described in the linked explanation. Before implementing a proposed task, write and review its blueprint with explicit shapes, units, frames, examples, tolerances and failure behavior.

### 2. Learn contact-aware behavior

<!-- source-flow: 2022-dexpoint#stage-2 -->

Use geometric features and contact-related reward shaping.

[Study the mechanism and math](/projects/2022-dexpoint#paper-section-learn-contact-aware-behavior).

- **Runnable supporting prerequisite:** [Prove Permutation Invariance with Symmetric Pooling](/problems/pointnet-symmetric-pooling). Pool valid point features channel by channel and demonstrate that point order cannot change the result.
- **Proposed component, not runnable:** Compute a Contact-Based Manipulation Reward.

**Step evidence:** retain a small input/output trace and the invariant described in the linked explanation. Before implementing a proposed task, write and review its blueprint with explicit shapes, units, frames, examples, tolerances and failure behavior.

### 3. Transfer to new objects

<!-- source-flow: 2022-dexpoint#stage-3 -->

Evaluate held-out geometry and real sensor observations.

[Study the mechanism and math](/projects/2022-dexpoint#paper-section-transfer-to-new-objects).

- **Proposed component, not runnable:** Evaluate Novel-Object Generalization.

**Step evidence:** retain a small input/output trace and the invariant described in the linked explanation. Before implementing a proposed task, write and review its blueprint with explicit shapes, units, frames, examples, tolerances and failure behavior.

| From | Signal or dependency | To |
|---|---|---|
| Construct observed and imagined points | combined point cloud | Learn contact-aware behavior |
| Learn contact-aware behavior | trained policy | Transfer to new objects |

## Integration exercise

**Proposed exercise — not runnable yet.** Construct short synthetic joint/object/contact traces with declared embodiment channels and reference motion; tactile exercises use original small contact-image arrays. Compose the selected mechanisms in the declared flow, beginning with **Construct observed and imagined points** and ending with **Transfer to new objects**. Save each intermediate artifact so a learner can locate a mismatch at its originating stage.

The integration boundary is selected imitation, adaptation, contact or sensing calculations on recorded arrays; dynamic stability and transfer to real hardware remain untested. Treat any stubbed learned stage as a named fixture, never as measured model capability. Author original synthetic data and record its generation rules; external datasets or assets need a separate provenance and license review.

Deliver an executable fixture generator, the component wiring, a compact expected-output trace and a report of the remaining differences from [the paper](/projects/2022-dexpoint). Proposed pieces must pass blueprint review and isolated evaluation before this integration becomes an available exercise.

## Evaluation and failure analysis

**Proposed assessment — not runnable yet.** For the **Construct observed and imagined points → Transfer to new objects** fixture, compare reference alignment, contact/state features or reward terms with known synthetic values; separate kinematic correctness from dynamic feasibility.

Use one clean baseline and a separately recorded fault case: misalign reference phase, drop a tactile frame, or alter an actuator/noise parameter; report per-signal errors and any invalid control evidence. Identify the affected stage and report its intermediate evidence. Do not average away the failing case.

Before grading, define an independent oracle, exact-versus-tolerant comparisons, allowed dtypes/devices, empty/minimal cases, invalid-input behavior and resource bounds. Compare failure detection and mathematical correctness separately from timing. A synthetic result establishes only the declared component contract; paper benchmark scores and physical safety require their own protocol.

## Reproducibility deliverable

**Proposed final artifact:** an original implementation/model card for **DexPoint: Generalizable Point Cloud Reinforcement Learning for Sim-to-Real Dexterous Manipulation** containing the source revision, exercised and stubbed stages, and an explicit list of omitted paper experiments.

Record joint order, morphology mapping, reference phase, contact convention, sensor/actuator time bases and dynamics assumptions. Pin problem/content versions, code revision, Python/dependency versions, evaluator identity, deterministic seeds and fixture hashes. Include the baseline/fault report and runtime observations. If any component updates parameters, record the update count and trainable state; otherwise state that no model was trained.

Package the fixture and expected trace with a machine-readable manifest. Replaying the same manifest must recover the same evidence within declared tolerances. Record limitations and the next unimplemented mechanism; completion of this proposal must not be labeled full-paper reproduction. Research PDFs remain local reference inputs, with canonical sources linked rather than redistributed.
