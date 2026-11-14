---
{
  "schema_version": 1,
  "generated_by": "scripts/generate-paper-tracks.ts",
  "slug": "paper-2021-dexmv",
  "paper_id": "2021-dexmv",
  "title": "DexMV: Imitation Learning for Dexterous Manipulation from Human Videos",
  "status": "planned",
  "primary_url": "https://arxiv.org/abs/2108.05877",
  "source_cards": [
    "research/papers/humanoid-dexterity-tactile/2021-dexmv.md"
  ],
  "paper_aliases": [],
  "category": "humanoid-dexterity-tactile",
  "topics": [
    "humanoid-dexterity-tactile",
    "dexmv"
  ],
  "runnable_problem_slugs": [],
  "proposed_component_count": 5,
  "source_flow_node_count": 3,
  "source_flow_nodes": [
    {
      "card": "2021-dexmv",
      "node": "stage-1"
    },
    {
      "card": "2021-dexmv",
      "node": "stage-2"
    },
    {
      "card": "2021-dexmv",
      "node": "stage-3"
    }
  ],
  "integration_status": "proposed",
  "assessment_status": "proposed"
}
---

# DexMV: Imitation Learning for Dexterous Manipulation from Human Videos — implementation track

## Orientation and scope

DexMV converts human manipulation videos into robot demonstrations by estimating hand/object pose, retargeting hand motion, and inferring robot actions. The inferred demonstrations then support imitation-augmented reinforcement learning in paired simulation tasks.

The implementation path follows **Estimate human and object motion → Retarget to robot kinematics → Infer actions and learn**. Work through the original explanation and the atomic tasks below before composing the proposed integration. Published exercises are small, independently graded components; this plan is not a completed or full-paper reproduction.

[Primary source](https://arxiv.org/abs/2108.05877) · [Paper explanation and graph](/projects/2021-dexmv) · [All paper tracks](../../PAPER_TRACKS.md)

Source cards: [2021-dexmv](../../../research/papers/humanoid-dexterity-tactile/2021-dexmv.md).

**Available now:** 0 paper-associated runnable components; 0 supporting runnable components. **Proposed:** 5 distinct component ideas, plus integration and assessment. A planned title can be a reviewed blueprint or an unreviewed idea; its presence is not a publication promise.

## Prerequisites and diagnostic

Read the input contracts and locally defined mathematics in the source explanation. Before starting, trace one small input through **Estimate human and object motion** and identify the shapes, masks, units, coordinate frames and time conventions that apply. This is a robotics diagnostic, not a general Python or mathematics course.

There is no independently runnable prerequisite mapped for this source yet. Use the source-card notation and stage contracts as the diagnostic; prerequisite exercises must be authored and reviewed before being presented as runnable.

## Ordered mechanisms and component tasks

The sequence below is a learning order. The explicit connections retain branching, conditioning and feedback; adjacent entries are not assumed to have interchangeable tensor interfaces.

### 1. Estimate human and object motion

<!-- source-flow: 2021-dexmv#stage-1 -->

Recover temporally aligned hand and object geometry from video.

[Study the mechanism and math](/projects/2021-dexmv#paper-section-estimate-human-and-object-motion).

- **Proposed component, not runnable:** Map Human Demonstration Segments to Robot Time.
- **Proposed component, not runnable:** Validate a Hand-Object Pose Sequence.

**Step evidence:** retain a small input/output trace and the invariant described in the linked explanation. Before implementing a proposed task, write and review its blueprint with explicit shapes, units, frames, examples, tolerances and failure behavior.

### 2. Retarget to robot kinematics

<!-- source-flow: 2021-dexmv#stage-2 -->

Match geometric relationships despite different hand morphology.

[Study the mechanism and math](/projects/2021-dexmv#paper-section-retarget-to-robot-kinematics).

- **Proposed component, not runnable:** Compute a Hand-Retargeting Geometry Residual.
- **Proposed component, not runnable:** Evaluate Retargeted Motion Feasibility.

**Step evidence:** retain a small input/output trace and the invariant described in the linked explanation. Before implementing a proposed task, write and review its blueprint with explicit shapes, units, frames, examples, tolerances and failure behavior.

### 3. Infer actions and learn

<!-- source-flow: 2021-dexmv#stage-3 -->

Turn retargeted states into robot control supervision.

[Study the mechanism and math](/projects/2021-dexmv#paper-section-infer-actions-and-learn).

- **Proposed component, not runnable:** Validate Actions Inferred from Retargeted States.

**Step evidence:** retain a small input/output trace and the invariant described in the linked explanation. Before implementing a proposed task, write and review its blueprint with explicit shapes, units, frames, examples, tolerances and failure behavior.

| From | Signal or dependency | To |
|---|---|---|
| Estimate human and object motion | estimated poses | Retarget to robot kinematics |
| Retarget to robot kinematics | robot-state trajectory | Infer actions and learn |

## Integration exercise

**Proposed exercise — not runnable yet.** Construct short synthetic joint/object/contact traces with declared embodiment channels and reference motion; tactile exercises use original small contact-image arrays. Compose the selected mechanisms in the declared flow, beginning with **Estimate human and object motion** and ending with **Infer actions and learn**. Save each intermediate artifact so a learner can locate a mismatch at its originating stage.

The integration boundary is selected imitation, adaptation, contact or sensing calculations on recorded arrays; dynamic stability and transfer to real hardware remain untested. Treat any stubbed learned stage as a named fixture, never as measured model capability. Author original synthetic data and record its generation rules; external datasets or assets need a separate provenance and license review.

Deliver an executable fixture generator, the component wiring, a compact expected-output trace and a report of the remaining differences from [the paper](/projects/2021-dexmv). Proposed pieces must pass blueprint review and isolated evaluation before this integration becomes an available exercise.

## Evaluation and failure analysis

**Proposed assessment — not runnable yet.** For the **Estimate human and object motion → Infer actions and learn** fixture, compare reference alignment, contact/state features or reward terms with known synthetic values; separate kinematic correctness from dynamic feasibility.

Use one clean baseline and a separately recorded fault case: misalign reference phase, drop a tactile frame, or alter an actuator/noise parameter; report per-signal errors and any invalid control evidence. Identify the affected stage and report its intermediate evidence. Do not average away the failing case.

Before grading, define an independent oracle, exact-versus-tolerant comparisons, allowed dtypes/devices, empty/minimal cases, invalid-input behavior and resource bounds. Compare failure detection and mathematical correctness separately from timing. A synthetic result establishes only the declared component contract; paper benchmark scores and physical safety require their own protocol.

## Reproducibility deliverable

**Proposed final artifact:** an original implementation/model card for **DexMV: Imitation Learning for Dexterous Manipulation from Human Videos** containing the source revision, exercised and stubbed stages, and an explicit list of omitted paper experiments.

Record joint order, morphology mapping, reference phase, contact convention, sensor/actuator time bases and dynamics assumptions. Pin problem/content versions, code revision, Python/dependency versions, evaluator identity, deterministic seeds and fixture hashes. Include the baseline/fault report and runtime observations. If any component updates parameters, record the update count and trainable state; otherwise state that no model was trained.

Package the fixture and expected trace with a machine-readable manifest. Replaying the same manifest must recover the same evidence within declared tolerances. Record limitations and the next unimplemented mechanism; completion of this proposal must not be labeled full-paper reproduction. Research PDFs remain local reference inputs, with canonical sources linked rather than redistributed.
