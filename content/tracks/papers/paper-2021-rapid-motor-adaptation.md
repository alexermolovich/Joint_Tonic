---
{
  "schema_version": 1,
  "generated_by": "scripts/generate-paper-tracks.ts",
  "slug": "paper-2021-rapid-motor-adaptation",
  "paper_id": "2021-rapid-motor-adaptation",
  "title": "RMA: Rapid Motor Adaptation for Legged Robots",
  "status": "planned",
  "primary_url": "https://arxiv.org/abs/2107.04034",
  "source_cards": [
    "research/papers/humanoid-dexterity-tactile/2021-rapid-motor-adaptation.md"
  ],
  "paper_aliases": [],
  "category": "humanoid-dexterity-tactile",
  "topics": [
    "humanoid-dexterity-tactile",
    "rapid-motor-adaptation"
  ],
  "runnable_problem_slugs": [],
  "proposed_component_count": 5,
  "source_flow_node_count": 3,
  "source_flow_nodes": [
    {
      "card": "2021-rapid-motor-adaptation",
      "node": "stage-1"
    },
    {
      "card": "2021-rapid-motor-adaptation",
      "node": "stage-2"
    },
    {
      "card": "2021-rapid-motor-adaptation",
      "node": "stage-3"
    }
  ],
  "integration_status": "proposed",
  "assessment_status": "proposed"
}
---

# RMA: Rapid Motor Adaptation for Legged Robots — implementation track

## Orientation and scope

RMA learns a locomotion policy conditioned on a latent description of environmental factors, then trains an adaptation module to infer that latent from recent state/action history. Deployment uses the inferred latent rather than privileged simulator parameters.

The implementation path follows **Train with privileged extrinsics → Infer extrinsics from history → Run asynchronous adaptation**. Work through the original explanation and the atomic tasks below before composing the proposed integration. Published exercises are small, independently graded components; this plan is not a completed or full-paper reproduction.

[Primary source](https://arxiv.org/abs/2107.04034) · [Paper explanation and graph](/projects/2021-rapid-motor-adaptation) · [All paper tracks](../../PAPER_TRACKS.md)

Source cards: [2021-rapid-motor-adaptation](../../../research/papers/humanoid-dexterity-tactile/2021-rapid-motor-adaptation.md).

**Available now:** 0 paper-associated runnable components; 0 supporting runnable components. **Proposed:** 5 distinct component ideas, plus integration and assessment. A planned title can be a reviewed blueprint or an unreviewed idea; its presence is not a publication promise.

## Prerequisites and diagnostic

Read the input contracts and locally defined mathematics in the source explanation. Before starting, trace one small input through **Train with privileged extrinsics** and identify the shapes, masks, units, coordinate frames and time conventions that apply. This is a robotics diagnostic, not a general Python or mathematics course.

There is no independently runnable prerequisite mapped for this source yet. Use the source-card notation and stage contracts as the diagnostic; prerequisite exercises must be authored and reviewed before being presented as runnable.

## Ordered mechanisms and component tasks

The sequence below is a learning order. The explicit connections retain branching, conditioning and feedback; adjacent entries are not assumed to have interchangeable tensor interfaces.

### 1. Train with privileged extrinsics

<!-- source-flow: 2021-rapid-motor-adaptation#stage-1 -->

Encode simulated environment factors for the base policy.

[Study the mechanism and math](/projects/2021-rapid-motor-adaptation#paper-section-train-with-privileged-extrinsics).

- **Proposed component, not runnable:** Build Privileged Dynamics-Latent Supervision.

**Step evidence:** retain a small input/output trace and the invariant described in the linked explanation. Before implementing a proposed task, write and review its blueprint with explicit shapes, units, frames, examples, tolerances and failure behavior.

### 2. Infer extrinsics from history

<!-- source-flow: 2021-rapid-motor-adaptation#stage-2 -->

Train an adaptation module against the privileged latent.

[Study the mechanism and math](/projects/2021-rapid-motor-adaptation#paper-section-infer-extrinsics-from-history).

- **Proposed component, not runnable:** Window Proprioceptive History.
- **Proposed component, not runnable:** Estimate a Latent Dynamics Context.

**Step evidence:** retain a small input/output trace and the invariant described in the linked explanation. Before implementing a proposed task, write and review its blueprint with explicit shapes, units, frames, examples, tolerances and failure behavior.

### 3. Run asynchronous adaptation

<!-- source-flow: 2021-rapid-motor-adaptation#stage-3 -->

Use the latest inferred latent for high-rate control.

[Study the mechanism and math](/projects/2021-rapid-motor-adaptation#paper-section-run-asynchronous-adaptation).

- **Proposed component, not runnable:** Track the Age of an Asynchronous Adaptation Latent.
- **Proposed component, not runnable:** Evaluate Policy Recovery After a Parameter Change.

**Step evidence:** retain a small input/output trace and the invariant described in the linked explanation. Before implementing a proposed task, write and review its blueprint with explicit shapes, units, frames, examples, tolerances and failure behavior.

| From | Signal or dependency | To |
|---|---|---|
| Train with privileged extrinsics | state-action history | Infer extrinsics from history |
| Infer extrinsics from history | adapted latent | Run asynchronous adaptation |

## Integration exercise

**Proposed exercise — not runnable yet.** Construct short synthetic joint/object/contact traces with declared embodiment channels and reference motion; tactile exercises use original small contact-image arrays. Compose the selected mechanisms in the declared flow, beginning with **Train with privileged extrinsics** and ending with **Run asynchronous adaptation**. Save each intermediate artifact so a learner can locate a mismatch at its originating stage.

The integration boundary is selected imitation, adaptation, contact or sensing calculations on recorded arrays; dynamic stability and transfer to real hardware remain untested. Treat any stubbed learned stage as a named fixture, never as measured model capability. Author original synthetic data and record its generation rules; external datasets or assets need a separate provenance and license review.

Deliver an executable fixture generator, the component wiring, a compact expected-output trace and a report of the remaining differences from [the paper](/projects/2021-rapid-motor-adaptation). Proposed pieces must pass blueprint review and isolated evaluation before this integration becomes an available exercise.

## Evaluation and failure analysis

**Proposed assessment — not runnable yet.** For the **Train with privileged extrinsics → Run asynchronous adaptation** fixture, compare reference alignment, contact/state features or reward terms with known synthetic values; separate kinematic correctness from dynamic feasibility.

Use one clean baseline and a separately recorded fault case: misalign reference phase, drop a tactile frame, or alter an actuator/noise parameter; report per-signal errors and any invalid control evidence. Identify the affected stage and report its intermediate evidence. Do not average away the failing case.

Before grading, define an independent oracle, exact-versus-tolerant comparisons, allowed dtypes/devices, empty/minimal cases, invalid-input behavior and resource bounds. Compare failure detection and mathematical correctness separately from timing. A synthetic result establishes only the declared component contract; paper benchmark scores and physical safety require their own protocol.

## Reproducibility deliverable

**Proposed final artifact:** an original implementation/model card for **RMA: Rapid Motor Adaptation for Legged Robots** containing the source revision, exercised and stubbed stages, and an explicit list of omitted paper experiments.

Record joint order, morphology mapping, reference phase, contact convention, sensor/actuator time bases and dynamics assumptions. Pin problem/content versions, code revision, Python/dependency versions, evaluator identity, deterministic seeds and fixture hashes. Include the baseline/fault report and runtime observations. If any component updates parameters, record the update count and trainable state; otherwise state that no model was trained.

Package the fixture and expected trace with a machine-readable manifest. Replaying the same manifest must recover the same evidence within declared tolerances. Record limitations and the next unimplemented mechanism; completion of this proposal must not be labeled full-paper reproduction. Research PDFs remain local reference inputs, with canonical sources linked rather than redistributed.
