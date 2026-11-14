---
{
  "schema_version": 1,
  "generated_by": "scripts/generate-paper-tracks.ts",
  "slug": "paper-2020-sapien",
  "paper_id": "2020-sapien",
  "title": "SAPIEN: A SimulAted Part-based Interactive ENvironment",
  "status": "planned",
  "primary_url": "https://arxiv.org/abs/2003.08515",
  "source_cards": [
    "research/papers/simulation-sim2real/2020-sapien.md"
  ],
  "paper_aliases": [],
  "category": "simulation-sim2real",
  "topics": [
    "simulation-sim2real",
    "sapien"
  ],
  "runnable_problem_slugs": [
    "se3-transform-points",
    "project-camera-points",
    "unproject-depth-map",
    "trace-perception-frame-graph",
    "geometric-jacobian-joint-axes"
  ],
  "proposed_component_count": 4,
  "source_flow_node_count": 3,
  "source_flow_nodes": [
    {
      "card": "2020-sapien",
      "node": "stage-1"
    },
    {
      "card": "2020-sapien",
      "node": "stage-2"
    },
    {
      "card": "2020-sapien",
      "node": "stage-3"
    }
  ],
  "integration_status": "proposed",
  "assessment_status": "proposed"
}
---

# SAPIEN: A SimulAted Part-based Interactive ENvironment — implementation track

## Orientation and scope

SAPIEN focuses on physically interactive articulated objects and part-level understanding. It connects visual perception of object structure to manipulation of joints, links, and contact-rich mechanisms.

The implementation path follows **Represent articulated assets → Render part-level observations → Test interactive behavior**. Work through the original explanation and the atomic tasks below before composing the proposed integration. Published exercises are small, independently graded components; this plan is not a completed or full-paper reproduction.

[Primary source](https://arxiv.org/abs/2003.08515) · [Paper explanation and graph](/projects/2020-sapien) · [All paper tracks](../../PAPER_TRACKS.md)

Source cards: [2020-sapien](../../../research/papers/simulation-sim2real/2020-sapien.md).

**Available now:** 0 paper-associated runnable components; 5 supporting runnable components. **Proposed:** 4 distinct component ideas, plus integration and assessment. A planned title can be a reviewed blueprint or an unreviewed idea; its presence is not a publication promise.

## Prerequisites and diagnostic

Read the input contracts and locally defined mathematics in the source explanation. Before starting, trace one small input through **Represent articulated assets** and identify the shapes, masks, units, coordinate frames and time conventions that apply. This is a robotics diagnostic, not a general Python or mathematics course.

- **Supporting prerequisite:** [Apply an SE(3) Transform to Batched Points](/problems/se3-transform-points). Its own contract remains authoritative; it does not implement the entire paper.
- **Supporting prerequisite:** [Project Camera Points into Pixels](/problems/project-camera-points). Its own contract remains authoritative; it does not implement the entire paper.
- **Supporting prerequisite:** [Unproject a Depth Map into a Point Cloud](/problems/unproject-depth-map). Its own contract remains authoritative; it does not implement the entire paper.
- **Supporting prerequisite:** [Trace Frames Through a Robot Perception Graph](/problems/trace-perception-frame-graph). Its own contract remains authoritative; it does not implement the entire paper.
- **Supporting prerequisite:** [Compute a Geometric Jacobian from Joint Axes](/problems/geometric-jacobian-joint-axes). Its own contract remains authoritative; it does not implement the entire paper.

## Ordered mechanisms and component tasks

The sequence below is a learning order. The explicit connections retain branching, conditioning and feedback; adjacent entries are not assumed to have interchangeable tensor interfaces.

### 1. Represent articulated assets

<!-- source-flow: 2020-sapien#stage-1 -->

Describe links, joints, and motion constraints.

[Study the mechanism and math](/projects/2020-sapien#paper-section-represent-articulated-assets).

- **Runnable supporting prerequisite:** [Apply an SE(3) Transform to Batched Points](/problems/se3-transform-points). Move camera-frame points into the world frame using a rigid transform.
- **Proposed component, not runnable:** Validate an Articulated Object Schema.
- **Proposed component, not runnable:** Compute Joint-Conditioned Object State.

**Step evidence:** retain a small input/output trace and the invariant described in the linked explanation. Before implementing a proposed task, write and review its blueprint with explicit shapes, units, frames, examples, tolerances and failure behavior.

### 2. Render part-level observations

<!-- source-flow: 2020-sapien#stage-2 -->

Generate visual evidence for parts and articulation.

[Study the mechanism and math](/projects/2020-sapien#paper-section-render-part-level-observations).

- **Runnable supporting prerequisite:** [Project Camera Points into Pixels](/problems/project-camera-points). Project camera-frame points and separate depth validity from image bounds.
- **Runnable supporting prerequisite:** [Unproject a Depth Map into a Point Cloud](/problems/unproject-depth-map). Turn optical-axis depth into an organized camera-frame point cloud while preserving missing-pixel masks.
- **Runnable supporting prerequisite:** [Trace Frames Through a Robot Perception Graph](/problems/trace-perception-frame-graph). Resolve a rigid transform between two frames in a validated acyclic frame forest.
- **Runnable supporting prerequisite:** [Compute a Geometric Jacobian from Joint Axes](/problems/geometric-jacobian-joint-axes). Convert base-frame joint axes and origins into a linear-first tool geometric Jacobian.
- **Proposed component, not runnable:** Project a Tracked Point Across Views.

**Step evidence:** retain a small input/output trace and the invariant described in the linked explanation. Before implementing a proposed task, write and review its blueprint with explicit shapes, units, frames, examples, tolerances and failure behavior.

### 3. Test interactive behavior

<!-- source-flow: 2020-sapien#stage-3 -->

Evaluate whether perception supports the intended object motion.

[Study the mechanism and math](/projects/2020-sapien#paper-section-test-interactive-behavior).

- **Proposed component, not runnable:** Build a Reproducible Interaction Scenario.

**Step evidence:** retain a small input/output trace and the invariant described in the linked explanation. Before implementing a proposed task, write and review its blueprint with explicit shapes, units, frames, examples, tolerances and failure behavior.

| From | Signal or dependency | To |
|---|---|---|
| Represent articulated assets | articulated state | Render part-level observations |
| Render part-level observations | estimated parts and actions | Test interactive behavior |

## Integration exercise

**Proposed exercise — not runnable yet.** Construct a few original scenario/rollout records with bounded physical parameters, seeds and explicit success labels; use analytic dynamics for any required state transition. Compose the selected mechanisms in the declared flow, beginning with **Represent articulated assets** and ending with **Test interactive behavior**. Save each intermediate artifact so a learner can locate a mismatch at its originating stage.

The integration boundary is the selected simulation data, metric or transfer mechanism; running the original simulator assets or reproducing reported real-world transfer requires separate reviewed work. Treat any stubbed learned stage as a named fixture, never as measured model capability. Author original synthetic data and record its generation rules; external datasets or assets need a separate provenance and license review.

Deliver an executable fixture generator, the component wiring, a compact expected-output trace and a report of the remaining differences from [the paper](/projects/2020-sapien). Proposed pieces must pass blueprint review and isolated evaluation before this integration becomes an available exercise.

## Evaluation and failure analysis

**Proposed assessment — not runnable yet.** For the **Represent articulated assets → Test interactive behavior** fixture, compare scenario coverage, rollout statistics or sampled parameter constraints with a deterministic expected report; keep success, failure and censoring distinct.

Use one clean baseline and a separately recorded fault case: remove a scenario family, violate a parameter bound, or change a reset/termination condition; measure the resulting coverage or metric discrepancy. Identify the affected stage and report its intermediate evidence. Do not average away the failing case.

Before grading, define an independent oracle, exact-versus-tolerant comparisons, allowed dtypes/devices, empty/minimal cases, invalid-input behavior and resource bounds. Compare failure detection and mathematical correctness separately from timing. A synthetic result establishes only the declared component contract; paper benchmark scores and physical safety require their own protocol.

## Reproducibility deliverable

**Proposed final artifact:** an original implementation/model card for **SAPIEN: A SimulAted Part-based Interactive ENvironment** containing the source revision, exercised and stubbed stages, and an explicit list of omitted paper experiments.

Record scenario IDs, reset and termination rules, physical units, parameter distributions, seeds and simulator/backend version if one is later introduced. Pin problem/content versions, code revision, Python/dependency versions, evaluator identity, deterministic seeds and fixture hashes. Include the baseline/fault report and runtime observations. If any component updates parameters, record the update count and trainable state; otherwise state that no model was trained.

Package the fixture and expected trace with a machine-readable manifest. Replaying the same manifest must recover the same evidence within declared tolerances. Record limitations and the next unimplemented mechanism; completion of this proposal must not be labeled full-paper reproduction. Research PDFs remain local reference inputs, with canonical sources linked rather than redistributed.
