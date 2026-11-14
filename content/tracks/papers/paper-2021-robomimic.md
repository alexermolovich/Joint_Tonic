---
{
  "schema_version": 1,
  "generated_by": "scripts/generate-paper-tracks.ts",
  "slug": "paper-2021-robomimic",
  "paper_id": "2021-robomimic",
  "title": "What Matters in Learning from Offline Human Demonstrations for Robot Manipulation",
  "status": "planned",
  "primary_url": "https://arxiv.org/abs/2108.03298",
  "source_cards": [
    "research/papers/mlops-sim2real/2021-robomimic.md"
  ],
  "paper_aliases": [],
  "category": "mlops-sim2real",
  "topics": [
    "imitation-learning",
    "offline-rl",
    "robot-demonstrations",
    "reproducibility",
    "evaluation"
  ],
  "runnable_problem_slugs": [
    "act-sliding-action-chunks",
    "validate-robot-episodes",
    "scene-safe-trajectory-split",
    "batch-variable-robot-episodes",
    "demonstration-quality-performance",
    "validation-loss-rollout-ranking",
    "offline-rollout-checkpoint-gate"
  ],
  "proposed_component_count": 1,
  "source_flow_node_count": 3,
  "source_flow_nodes": [
    {
      "card": "2021-robomimic",
      "node": "stage-1"
    },
    {
      "card": "2021-robomimic",
      "node": "stage-2"
    },
    {
      "card": "2021-robomimic",
      "node": "stage-3"
    }
  ],
  "integration_status": "proposed",
  "assessment_status": "proposed"
}
---

# What Matters in Learning from Offline Human Demonstrations for Robot Manipulation — implementation track

## Orientation and scope

robomimic studies offline robot learning from human demonstrations of different quality and provides reproducible data and learning tools. Its experiments show that dataset composition, observation/action interfaces, temporal modeling, and policy selection materially affect success. A low supervised loss does not necessarily identify the policy that performs best when its own actions change future observations.

The implementation path follows **Construct episode windows → Fit an offline policy → Select with rollout evidence**. Work through the original explanation and the atomic tasks below before composing the proposed integration. Published exercises are small, independently graded components; this plan is not a completed or full-paper reproduction.

[Primary source](https://arxiv.org/abs/2108.03298) · [Paper explanation and graph](/projects/2021-robomimic) · [All paper tracks](../../PAPER_TRACKS.md)

Source cards: [2021-robomimic](../../../research/papers/mlops-sim2real/2021-robomimic.md).

**Available now:** 5 paper-associated runnable components; 2 supporting runnable components. **Proposed:** 1 distinct component ideas, plus integration and assessment. A planned title can be a reviewed blueprint or an unreviewed idea; its presence is not a publication promise.

## Prerequisites and diagnostic

Read the input contracts and locally defined mathematics in the source explanation. Before starting, trace one small input through **Construct episode windows** and identify the shapes, masks, units, coordinate frames and time conventions that apply. This is a robotics diagnostic, not a general Python or mathematics course.

- **Supporting prerequisite:** [Build Sliding Action Chunks with Padding Masks](/problems/act-sliding-action-chunks). Its own contract remains authoritative; it does not implement the entire paper.
- **Supporting prerequisite:** [Validate a Multimodal Robot Episode Schema](/problems/validate-robot-episodes). Its own contract remains authoritative; it does not implement the entire paper.

## Ordered mechanisms and component tasks

The sequence below is a learning order. The explicit connections retain branching, conditioning and feedback; adjacent entries are not assumed to have interchangeable tensor interfaces.

### 1. Construct episode windows

<!-- source-flow: 2021-robomimic#stage-1 -->

Batch temporal data without crossing episode boundaries or leaking evaluation episodes.

[Study the mechanism and math](/projects/2021-robomimic#paper-section-construct-episode-windows).

- **Runnable supporting prerequisite:** [Build Sliding Action Chunks with Padding Masks](/problems/act-sliding-action-chunks). Extract fixed-horizon action windows from one episode while marking right-padding and preserving requested start order.
- **Runnable supporting prerequisite:** [Validate a Multimodal Robot Episode Schema](/problems/validate-robot-episodes). A signal's missing fraction is missing_rows / T. A timestamp must be finite numeric, and each valid adjacent pair must strictly increase.
- **Runnable paper-associated component:** [Split Robot Trajectories Without Scene Leakage](/problems/scene-safe-trajectory-split). Assign complete scenes to deterministic train or validation partitions while preserving trajectory order.
- **Runnable paper-associated component:** [Batch Variable-Length Episodes with Masks](/problems/batch-variable-robot-episodes). Pad complete robot episodes to a shared horizon without confusing valid zeros with padding.

**Step evidence:** retain a small input/output trace and the invariant described in the linked explanation. Before implementing a proposed task, write and review its blueprint with explicit shapes, units, frames, examples, tolerances and failure behavior.

### 2. Fit an offline policy

<!-- source-flow: 2021-robomimic#stage-2 -->

Optimize a chosen imitation or offline-learning objective on fixed demonstrations.

[Study the mechanism and math](/projects/2021-robomimic#paper-section-fit-an-offline-policy).

- **Proposed component, not runnable:** Compute a Masked Behavior-Cloning Log-Likelihood.

**Step evidence:** retain a small input/output trace and the invariant described in the linked explanation. Before implementing a proposed task, write and review its blueprint with explicit shapes, units, frames, examples, tolerances and failure behavior.

### 3. Select with rollout evidence

<!-- source-flow: 2021-robomimic#stage-3 -->

Measure actual task success and uncertainty on held-out evaluation conditions.

[Study the mechanism and math](/projects/2021-robomimic#paper-section-select-with-rollout-evidence).

- **Runnable paper-associated component:** [Report Performance by Demonstration Quality](/problems/demonstration-quality-performance). Report task-stratified rollout success without hiding difficult tasks behind more frequent easy tasks.
- **Runnable paper-associated component:** [Compare Validation Loss with Rollout Success](/problems/validation-loss-rollout-ranking). Expose when offline-loss ordering disagrees with the ordering of observed rollout success.
- **Runnable paper-associated component:** [Select a Checkpoint with Offline and Rollout Gates](/problems/offline-rollout-checkpoint-gate). Choose a candidate only when offline loss, rollout coverage and exact success-rate gates all pass.

**Step evidence:** retain a small input/output trace and the invariant described in the linked explanation. Before implementing a proposed task, write and review its blueprint with explicit shapes, units, frames, examples, tolerances and failure behavior.

| From | Signal or dependency | To |
|---|---|---|
| Construct episode windows | demonstration batches | Fit an offline policy |
| Fit an offline policy | candidate policies | Select with rollout evidence |

## Integration exercise

**Proposed exercise — not runnable yet.** Construct a small synthetic pipeline/configuration graph and scenario metric records, or bounded randomization samples where the selected mechanism requires them. Compose the selected mechanisms in the declared flow, beginning with **Construct episode windows** and ending with **Select with rollout evidence**. Save each intermediate artifact so a learner can locate a mismatch at its originating stage.

The integration boundary is data, dependency, evaluation and transfer-check calculations; synthetic acceptance is not evidence of safe deployment or sim-to-real success. Treat any stubbed learned stage as a named fixture, never as measured model capability. Author original synthetic data and record its generation rules; external datasets or assets need a separate provenance and license review.

Deliver an executable fixture generator, the component wiring, a compact expected-output trace and a report of the remaining differences from [the paper](/projects/2021-robomimic). Proposed pieces must pass blueprint review and isolated evaluation before this integration becomes an available exercise.

## Evaluation and failure analysis

**Proposed assessment — not runnable yet.** For the **Construct episode windows → Select with rollout evidence** fixture, compare dependency and release decisions with known graph/record fixtures and report scenario-level metrics before aggregate conclusions.

Use one clean baseline and a separately recorded fault case: invalidate a dependency, remove one hardware/scenario slice, or perturb a physical parameter outside the declared envelope; expose the precise failure. Identify the affected stage and report its intermediate evidence. Do not average away the failing case.

Before grading, define an independent oracle, exact-versus-tolerant comparisons, allowed dtypes/devices, empty/minimal cases, invalid-input behavior and resource bounds. Compare failure detection and mathematical correctness separately from timing. A synthetic result establishes only the declared component contract; paper benchmark scores and physical safety require their own protocol.

## Reproducibility deliverable

**Proposed final artifact:** an original implementation/model card for **What Matters in Learning from Offline Human Demonstrations for Robot Manipulation** containing the source revision, exercised and stubbed stages, and an explicit list of omitted paper experiments.

Record pipeline/configuration digest, simulator or hardware label, randomization bounds, timing units, scenario definitions and release criteria. Pin problem/content versions, code revision, Python/dependency versions, evaluator identity, deterministic seeds and fixture hashes. Include the baseline/fault report and runtime observations. If any component updates parameters, record the update count and trainable state; otherwise state that no model was trained.

Package the fixture and expected trace with a machine-readable manifest. Replaying the same manifest must recover the same evidence within declared tolerances. Record limitations and the next unimplemented mechanism; completion of this proposal must not be labeled full-paper reproduction. Research PDFs remain local reference inputs, with canonical sources linked rather than redistributed.
