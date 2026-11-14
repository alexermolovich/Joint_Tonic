---
{
  "schema_version": 1,
  "generated_by": "scripts/generate-paper-tracks.ts",
  "slug": "paper-2020-igibson",
  "paper_id": "2020-igibson",
  "title": "iGibson 1.0: a Simulation Environment for Interactive Tasks in Large Realistic Scenes",
  "status": "planned",
  "primary_url": "https://arxiv.org/abs/2012.02924",
  "source_cards": [
    "research/papers/simulation-sim2real/2020-igibson.md"
  ],
  "paper_aliases": [],
  "category": "simulation-sim2real",
  "topics": [
    "simulation-sim2real",
    "igibson"
  ],
  "runnable_problem_slugs": [
    "validate-robot-episodes",
    "seeded-visual-randomization",
    "sample-dynamics-distributions"
  ],
  "proposed_component_count": 3,
  "source_flow_node_count": 3,
  "source_flow_nodes": [
    {
      "card": "2020-igibson",
      "node": "stage-1"
    },
    {
      "card": "2020-igibson",
      "node": "stage-2"
    },
    {
      "card": "2020-igibson",
      "node": "stage-3"
    }
  ],
  "integration_status": "proposed",
  "assessment_status": "proposed"
}
---

# iGibson 1.0: a Simulation Environment for Interactive Tasks in Large Realistic Scenes — implementation track

## Orientation and scope

iGibson 1.0 combines interactive indoor scenes, articulated objects, virtual sensors, domain randomization, and planning interfaces. It supports studying navigation and manipulation in environments whose objects can physically change state.

The implementation path follows **Build an interactive scene → Randomize and observe → Interact and evaluate transfer**. Work through the original explanation and the atomic tasks below before composing the proposed integration. Published exercises are small, independently graded components; this plan is not a completed or full-paper reproduction.

[Primary source](https://arxiv.org/abs/2012.02924) · [Paper explanation and graph](/projects/2020-igibson) · [All paper tracks](../../PAPER_TRACKS.md)

Source cards: [2020-igibson](../../../research/papers/simulation-sim2real/2020-igibson.md).

**Available now:** 0 paper-associated runnable components; 3 supporting runnable components. **Proposed:** 3 distinct component ideas, plus integration and assessment. A planned title can be a reviewed blueprint or an unreviewed idea; its presence is not a publication promise.

## Prerequisites and diagnostic

Read the input contracts and locally defined mathematics in the source explanation. Before starting, trace one small input through **Build an interactive scene** and identify the shapes, masks, units, coordinate frames and time conventions that apply. This is a robotics diagnostic, not a general Python or mathematics course.

- **Supporting prerequisite:** [Validate a Multimodal Robot Episode Schema](/problems/validate-robot-episodes). Its own contract remains authoritative; it does not implement the entire paper.
- **Supporting prerequisite:** [Build a Seeded Visual Randomization Sampler](/problems/seeded-visual-randomization). Its own contract remains authoritative; it does not implement the entire paper.
- **Supporting prerequisite:** [Sample Mass, Friction, Delay, and Gain Distributions](/problems/sample-dynamics-distributions). Its own contract remains authoritative; it does not implement the entire paper.

## Ordered mechanisms and component tasks

The sequence below is a learning order. The explicit connections retain branching, conditioning and feedback; adjacent entries are not assumed to have interchangeable tensor interfaces.

### 1. Build an interactive scene

<!-- source-flow: 2020-igibson#stage-1 -->

Load rigid and articulated assets with physical properties.

[Study the mechanism and math](/projects/2020-igibson#paper-section-build-an-interactive-scene).

- **Proposed component, not runnable:** Validate a Scene Interaction Graph.

**Step evidence:** retain a small input/output trace and the invariant described in the linked explanation. Before implementing a proposed task, write and review its blueprint with explicit shapes, units, frames, examples, tolerances and failure behavior.

### 2. Randomize and observe

<!-- source-flow: 2020-igibson#stage-2 -->

Vary visual and physical conditions while generating sensor data.

[Study the mechanism and math](/projects/2020-igibson#paper-section-randomize-and-observe).

- **Runnable supporting prerequisite:** [Validate a Multimodal Robot Episode Schema](/problems/validate-robot-episodes). A signal's missing fraction is missing_rows / T. A timestamp must be finite numeric, and each valid adjacent pair must strictly increase.
- **Runnable supporting prerequisite:** [Build a Seeded Visual Randomization Sampler](/problems/seeded-visual-randomization). Build a Seeded Visual Randomization Sampler
- **Runnable supporting prerequisite:** [Sample Mass, Friction, Delay, and Gain Distributions](/problems/sample-dynamics-distributions). Convert reproducible unit draws into valid, explicitly typed per-episode physical parameter configurations.
- **Proposed component, not runnable:** Replay Sensor Streams from a Fixed Seed.

**Step evidence:** retain a small input/output trace and the invariant described in the linked explanation. Before implementing a proposed task, write and review its blueprint with explicit shapes, units, frames, examples, tolerances and failure behavior.

### 3. Interact and evaluate transfer

<!-- source-flow: 2020-igibson#stage-3 -->

Test tasks on declared scene and parameter holdouts.

[Study the mechanism and math](/projects/2020-igibson#paper-section-interact-and-evaluate-transfer).

- **Proposed component, not runnable:** Measure Domain Shift Between Simulated Scenes.

**Step evidence:** retain a small input/output trace and the invariant described in the linked explanation. Before implementing a proposed task, write and review its blueprint with explicit shapes, units, frames, examples, tolerances and failure behavior.

| From | Signal or dependency | To |
|---|---|---|
| Build an interactive scene | scene state | Randomize and observe |
| Randomize and observe | policy actions | Interact and evaluate transfer |

## Integration exercise

**Proposed exercise — not runnable yet.** Construct a few original scenario/rollout records with bounded physical parameters, seeds and explicit success labels; use analytic dynamics for any required state transition. Compose the selected mechanisms in the declared flow, beginning with **Build an interactive scene** and ending with **Interact and evaluate transfer**. Save each intermediate artifact so a learner can locate a mismatch at its originating stage.

The integration boundary is the selected simulation data, metric or transfer mechanism; running the original simulator assets or reproducing reported real-world transfer requires separate reviewed work. Treat any stubbed learned stage as a named fixture, never as measured model capability. Author original synthetic data and record its generation rules; external datasets or assets need a separate provenance and license review.

Deliver an executable fixture generator, the component wiring, a compact expected-output trace and a report of the remaining differences from [the paper](/projects/2020-igibson). Proposed pieces must pass blueprint review and isolated evaluation before this integration becomes an available exercise.

## Evaluation and failure analysis

**Proposed assessment — not runnable yet.** For the **Build an interactive scene → Interact and evaluate transfer** fixture, compare scenario coverage, rollout statistics or sampled parameter constraints with a deterministic expected report; keep success, failure and censoring distinct.

Use one clean baseline and a separately recorded fault case: remove a scenario family, violate a parameter bound, or change a reset/termination condition; measure the resulting coverage or metric discrepancy. Identify the affected stage and report its intermediate evidence. Do not average away the failing case.

Before grading, define an independent oracle, exact-versus-tolerant comparisons, allowed dtypes/devices, empty/minimal cases, invalid-input behavior and resource bounds. Compare failure detection and mathematical correctness separately from timing. A synthetic result establishes only the declared component contract; paper benchmark scores and physical safety require their own protocol.

## Reproducibility deliverable

**Proposed final artifact:** an original implementation/model card for **iGibson 1.0: a Simulation Environment for Interactive Tasks in Large Realistic Scenes** containing the source revision, exercised and stubbed stages, and an explicit list of omitted paper experiments.

Record scenario IDs, reset and termination rules, physical units, parameter distributions, seeds and simulator/backend version if one is later introduced. Pin problem/content versions, code revision, Python/dependency versions, evaluator identity, deterministic seeds and fixture hashes. Include the baseline/fault report and runtime observations. If any component updates parameters, record the update count and trainable state; otherwise state that no model was trained.

Package the fixture and expected trace with a machine-readable manifest. Replaying the same manifest must recover the same evidence within declared tolerances. Record limitations and the next unimplemented mechanism; completion of this proposal must not be labeled full-paper reproduction. Research PDFs remain local reference inputs, with canonical sources linked rather than redistributed.
