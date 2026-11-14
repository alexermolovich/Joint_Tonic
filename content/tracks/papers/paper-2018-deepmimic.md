---
{
  "schema_version": 1,
  "generated_by": "scripts/generate-paper-tracks.ts",
  "slug": "paper-2018-deepmimic",
  "paper_id": "2018-deepmimic",
  "title": "DeepMimic: Example-Guided Deep Reinforcement Learning of Physics-Based Character Skills",
  "status": "planned",
  "primary_url": "https://arxiv.org/abs/1804.02717",
  "source_cards": [
    "research/papers/humanoid-dexterity-tactile/2018-deepmimic.md"
  ],
  "paper_aliases": [],
  "category": "humanoid-dexterity-tactile",
  "topics": [
    "humanoid-dexterity-tactile",
    "deepmimic"
  ],
  "runnable_problem_slugs": [],
  "proposed_component_count": 4,
  "source_flow_node_count": 3,
  "source_flow_nodes": [
    {
      "card": "2018-deepmimic",
      "node": "stage-1"
    },
    {
      "card": "2018-deepmimic",
      "node": "stage-2"
    },
    {
      "card": "2018-deepmimic",
      "node": "stage-3"
    }
  ],
  "integration_status": "proposed",
  "assessment_status": "proposed"
}
---

# DeepMimic: Example-Guided Deep Reinforcement Learning of Physics-Based Character Skills — implementation track

## Orientation and scope

DeepMimic trains physically simulated characters to imitate reference motion while satisfying task objectives. Motion clips specify style and coordination, while reinforcement learning finds feedback actions that realize those motions under simulated dynamics.

The implementation path follows **Condition on reference phase → Measure imitation quality → Optimize feedback control**. Work through the original explanation and the atomic tasks below before composing the proposed integration. Published exercises are small, independently graded components; this plan is not a completed or full-paper reproduction.

[Primary source](https://arxiv.org/abs/1804.02717) · [Paper explanation and graph](/projects/2018-deepmimic) · [All paper tracks](../../PAPER_TRACKS.md)

Source cards: [2018-deepmimic](../../../research/papers/humanoid-dexterity-tactile/2018-deepmimic.md).

**Available now:** 0 paper-associated runnable components; 0 supporting runnable components. **Proposed:** 4 distinct component ideas, plus integration and assessment. A planned title can be a reviewed blueprint or an unreviewed idea; its presence is not a publication promise.

## Prerequisites and diagnostic

Read the input contracts and locally defined mathematics in the source explanation. Before starting, trace one small input through **Condition on reference phase** and identify the shapes, masks, units, coordinate frames and time conventions that apply. This is a robotics diagnostic, not a general Python or mathematics course.

There is no independently runnable prerequisite mapped for this source yet. Use the source-card notation and stage contracts as the diagnostic; prerequisite exercises must be authored and reviewed before being presented as runnable.

## Ordered mechanisms and component tasks

The sequence below is a learning order. The explicit connections retain branching, conditioning and feedback; adjacent entries are not assumed to have interchangeable tensor interfaces.

### 1. Condition on reference phase

<!-- source-flow: 2018-deepmimic#stage-1 -->

Provide physical state and the current reference-motion phase.

[Study the mechanism and math](/projects/2018-deepmimic#paper-section-condition-on-reference-phase).

- **Proposed component, not runnable:** Interpolate a Reference Motion Pose.
- **Proposed component, not runnable:** Detect Phase Misalignment in a Motion Clip.

**Step evidence:** retain a small input/output trace and the invariant described in the linked explanation. Before implementing a proposed task, write and review its blueprint with explicit shapes, units, frames, examples, tolerances and failure behavior.

### 2. Measure imitation quality

<!-- source-flow: 2018-deepmimic#stage-2 -->

Compare joint rotations, velocities, endpoints, and center of mass.

[Study the mechanism and math](/projects/2018-deepmimic#paper-section-measure-imitation-quality).

- **Proposed component, not runnable:** Compute Pose and Velocity Imitation Rewards.

**Step evidence:** retain a small input/output trace and the invariant described in the linked explanation. Before implementing a proposed task, write and review its blueprint with explicit shapes, units, frames, examples, tolerances and failure behavior.

### 3. Optimize feedback control

<!-- source-flow: 2018-deepmimic#stage-3 -->

Balance imitation with the requested task.

[Study the mechanism and math](/projects/2018-deepmimic#paper-section-optimize-feedback-control).

- **Proposed component, not runnable:** Combine Imitation and Task Rewards for Motion Control.

**Step evidence:** retain a small input/output trace and the invariant described in the linked explanation. Before implementing a proposed task, write and review its blueprint with explicit shapes, units, frames, examples, tolerances and failure behavior.

| From | Signal or dependency | To |
|---|---|---|
| Condition on reference phase | simulated motion | Measure imitation quality |
| Measure imitation quality | imitation and task rewards | Optimize feedback control |

## Integration exercise

**Proposed exercise — not runnable yet.** Construct short synthetic joint/object/contact traces with declared embodiment channels and reference motion; tactile exercises use original small contact-image arrays. Compose the selected mechanisms in the declared flow, beginning with **Condition on reference phase** and ending with **Optimize feedback control**. Save each intermediate artifact so a learner can locate a mismatch at its originating stage.

The integration boundary is selected imitation, adaptation, contact or sensing calculations on recorded arrays; dynamic stability and transfer to real hardware remain untested. Treat any stubbed learned stage as a named fixture, never as measured model capability. Author original synthetic data and record its generation rules; external datasets or assets need a separate provenance and license review.

Deliver an executable fixture generator, the component wiring, a compact expected-output trace and a report of the remaining differences from [the paper](/projects/2018-deepmimic). Proposed pieces must pass blueprint review and isolated evaluation before this integration becomes an available exercise.

## Evaluation and failure analysis

**Proposed assessment — not runnable yet.** For the **Condition on reference phase → Optimize feedback control** fixture, compare reference alignment, contact/state features or reward terms with known synthetic values; separate kinematic correctness from dynamic feasibility.

Use one clean baseline and a separately recorded fault case: misalign reference phase, drop a tactile frame, or alter an actuator/noise parameter; report per-signal errors and any invalid control evidence. Identify the affected stage and report its intermediate evidence. Do not average away the failing case.

Before grading, define an independent oracle, exact-versus-tolerant comparisons, allowed dtypes/devices, empty/minimal cases, invalid-input behavior and resource bounds. Compare failure detection and mathematical correctness separately from timing. A synthetic result establishes only the declared component contract; paper benchmark scores and physical safety require their own protocol.

## Reproducibility deliverable

**Proposed final artifact:** an original implementation/model card for **DeepMimic: Example-Guided Deep Reinforcement Learning of Physics-Based Character Skills** containing the source revision, exercised and stubbed stages, and an explicit list of omitted paper experiments.

Record joint order, morphology mapping, reference phase, contact convention, sensor/actuator time bases and dynamics assumptions. Pin problem/content versions, code revision, Python/dependency versions, evaluator identity, deterministic seeds and fixture hashes. Include the baseline/fault report and runtime observations. If any component updates parameters, record the update count and trainable state; otherwise state that no model was trained.

Package the fixture and expected trace with a machine-readable manifest. Replaying the same manifest must recover the same evidence within declared tolerances. Record limitations and the next unimplemented mechanism; completion of this proposal must not be labeled full-paper reproduction. Research PDFs remain local reference inputs, with canonical sources linked rather than redistributed.
