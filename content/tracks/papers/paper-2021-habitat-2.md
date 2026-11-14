---
{
  "schema_version": 1,
  "generated_by": "scripts/generate-paper-tracks.ts",
  "slug": "paper-2021-habitat-2",
  "paper_id": "2021-habitat-2",
  "title": "Habitat 2.0: Training Home Assistants to Rearrange their Habitat",
  "status": "planned",
  "primary_url": "https://arxiv.org/abs/2106.14405",
  "source_cards": [
    "research/papers/simulation-sim2real/2021-habitat-2.md"
  ],
  "paper_aliases": [],
  "category": "simulation-sim2real",
  "topics": [
    "simulation-sim2real",
    "habitat-2"
  ],
  "runnable_problem_slugs": [
    "slice-infrastructure-release-gate",
    "sim-to-real-robustness-gate"
  ],
  "proposed_component_count": 4,
  "source_flow_node_count": 3,
  "source_flow_nodes": [
    {
      "card": "2021-habitat-2",
      "node": "stage-1"
    },
    {
      "card": "2021-habitat-2",
      "node": "stage-2"
    },
    {
      "card": "2021-habitat-2",
      "node": "stage-3"
    }
  ],
  "integration_status": "proposed",
  "assessment_status": "proposed"
}
---

# Habitat 2.0: Training Home Assistants to Rearrange their Habitat — implementation track

## Orientation and scope

Habitat 2.0 adds physics-enabled rearrangement, reconfigurable articulated indoor scenes, and long-horizon mobile-manipulation benchmarks. It evaluates both learned policies and classical sense-plan-act pipelines.

The implementation path follows **Configure a rearrangement task → Compose skills → Evaluate long-horizon outcomes**. Work through the original explanation and the atomic tasks below before composing the proposed integration. Published exercises are small, independently graded components; this plan is not a completed or full-paper reproduction.

[Primary source](https://arxiv.org/abs/2106.14405) · [Paper explanation and graph](/projects/2021-habitat-2) · [All paper tracks](../../PAPER_TRACKS.md)

Source cards: [2021-habitat-2](../../../research/papers/simulation-sim2real/2021-habitat-2.md).

**Available now:** 0 paper-associated runnable components; 2 supporting runnable components. **Proposed:** 4 distinct component ideas, plus integration and assessment. A planned title can be a reviewed blueprint or an unreviewed idea; its presence is not a publication promise.

## Prerequisites and diagnostic

Read the input contracts and locally defined mathematics in the source explanation. Before starting, trace one small input through **Configure a rearrangement task** and identify the shapes, masks, units, coordinate frames and time conventions that apply. This is a robotics diagnostic, not a general Python or mathematics course.

- **Supporting prerequisite:** [Gate a Release on Slice and Infrastructure Tests](/problems/slice-infrastructure-release-gate). Its own contract remains authoritative; it does not implement the entire paper.
- **Supporting prerequisite:** [Gate Sim-to-Real Release with Robustness Evidence](/problems/sim-to-real-robustness-gate). Its own contract remains authoritative; it does not implement the entire paper.

## Ordered mechanisms and component tasks

The sequence below is a learning order. The explicit connections retain branching, conditioning and feedback; adjacent entries are not assumed to have interchangeable tensor interfaces.

### 1. Configure a rearrangement task

<!-- source-flow: 2021-habitat-2#stage-1 -->

Set object, receptacle, articulation, and robot states.

[Study the mechanism and math](/projects/2021-habitat-2#paper-section-configure-a-rearrangement-task).

- **Proposed component, not runnable:** Construct a Rearrangement Goal Graph.
- **Proposed component, not runnable:** Validate Object Reset States.

**Step evidence:** retain a small input/output trace and the invariant described in the linked explanation. Before implementing a proposed task, write and review its blueprint with explicit shapes, units, frames, examples, tolerances and failure behavior.

### 2. Compose skills

<!-- source-flow: 2021-habitat-2#stage-2 -->

Transfer control between navigation, grasping, and placement.

[Study the mechanism and math](/projects/2021-habitat-2#paper-section-compose-skills).

- **Runnable supporting prerequisite:** [Gate a Release on Slice and Infrastructure Tests](/problems/slice-infrastructure-release-gate). Reject a candidate when any required scenario or infrastructure check lacks current passing evidence.
- **Runnable supporting prerequisite:** [Gate Sim-to-Real Release with Robustness Evidence](/problems/sim-to-real-robustness-gate). Gate Sim-to-Real Release with Robustness Evidence
- **Proposed component, not runnable:** Validate Skill Preconditions in a Rearrangement Plan.

**Step evidence:** retain a small input/output trace and the invariant described in the linked explanation. Before implementing a proposed task, write and review its blueprint with explicit shapes, units, frames, examples, tolerances and failure behavior.

### 3. Evaluate long-horizon outcomes

<!-- source-flow: 2021-habitat-2#stage-3 -->

Measure task completion and diagnose handoff failures.

[Study the mechanism and math](/projects/2021-habitat-2#paper-section-evaluate-long-horizon-outcomes).

- **Proposed component, not runnable:** Score Chained Task Success.

**Step evidence:** retain a small input/output trace and the invariant described in the linked explanation. Before implementing a proposed task, write and review its blueprint with explicit shapes, units, frames, examples, tolerances and failure behavior.

| From | Signal or dependency | To |
|---|---|---|
| Configure a rearrangement task | task state | Compose skills |
| Compose skills | skill sequence | Evaluate long-horizon outcomes |

## Integration exercise

**Proposed exercise — not runnable yet.** Construct a few original scenario/rollout records with bounded physical parameters, seeds and explicit success labels; use analytic dynamics for any required state transition. Compose the selected mechanisms in the declared flow, beginning with **Configure a rearrangement task** and ending with **Evaluate long-horizon outcomes**. Save each intermediate artifact so a learner can locate a mismatch at its originating stage.

The integration boundary is the selected simulation data, metric or transfer mechanism; running the original simulator assets or reproducing reported real-world transfer requires separate reviewed work. Treat any stubbed learned stage as a named fixture, never as measured model capability. Author original synthetic data and record its generation rules; external datasets or assets need a separate provenance and license review.

Deliver an executable fixture generator, the component wiring, a compact expected-output trace and a report of the remaining differences from [the paper](/projects/2021-habitat-2). Proposed pieces must pass blueprint review and isolated evaluation before this integration becomes an available exercise.

## Evaluation and failure analysis

**Proposed assessment — not runnable yet.** For the **Configure a rearrangement task → Evaluate long-horizon outcomes** fixture, compare scenario coverage, rollout statistics or sampled parameter constraints with a deterministic expected report; keep success, failure and censoring distinct.

Use one clean baseline and a separately recorded fault case: remove a scenario family, violate a parameter bound, or change a reset/termination condition; measure the resulting coverage or metric discrepancy. Identify the affected stage and report its intermediate evidence. Do not average away the failing case.

Before grading, define an independent oracle, exact-versus-tolerant comparisons, allowed dtypes/devices, empty/minimal cases, invalid-input behavior and resource bounds. Compare failure detection and mathematical correctness separately from timing. A synthetic result establishes only the declared component contract; paper benchmark scores and physical safety require their own protocol.

## Reproducibility deliverable

**Proposed final artifact:** an original implementation/model card for **Habitat 2.0: Training Home Assistants to Rearrange their Habitat** containing the source revision, exercised and stubbed stages, and an explicit list of omitted paper experiments.

Record scenario IDs, reset and termination rules, physical units, parameter distributions, seeds and simulator/backend version if one is later introduced. Pin problem/content versions, code revision, Python/dependency versions, evaluator identity, deterministic seeds and fixture hashes. Include the baseline/fault report and runtime observations. If any component updates parameters, record the update count and trainable state; otherwise state that no model was trained.

Package the fixture and expected trace with a machine-readable manifest. Replaying the same manifest must recover the same evidence within declared tolerances. Record limitations and the next unimplemented mechanism; completion of this proposal must not be labeled full-paper reproduction. Research PDFs remain local reference inputs, with canonical sources linked rather than redistributed.
