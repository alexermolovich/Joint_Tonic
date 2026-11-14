---
{
  "schema_version": 1,
  "generated_by": "scripts/generate-paper-tracks.ts",
  "slug": "paper-2023-robocat",
  "paper_id": "2023-robocat",
  "title": "RoboCat: A Self-Improving Generalist Agent for Robotic Manipulation",
  "status": "planned",
  "primary_url": "https://arxiv.org/abs/2306.11706",
  "source_cards": [
    "research/papers/vla-generalist/2023-robocat.md"
  ],
  "paper_aliases": [],
  "category": "vla-generalist",
  "topics": [
    "vla-generalist",
    "robocat"
  ],
  "runnable_problem_slugs": [
    "validate-robot-episodes"
  ],
  "proposed_component_count": 3,
  "source_flow_node_count": 3,
  "source_flow_nodes": [
    {
      "card": "2023-robocat",
      "node": "stage-1"
    },
    {
      "card": "2023-robocat",
      "node": "stage-2"
    },
    {
      "card": "2023-robocat",
      "node": "stage-3"
    }
  ],
  "integration_status": "proposed",
  "assessment_status": "proposed"
}
---

# RoboCat: A Self-Improving Generalist Agent for Robotic Manipulation — implementation track

## Orientation and scope

RoboCat trains a goal-image-conditioned generalist manipulation policy and improves it through repeated adaptation and data collection. A VQ-GAN image tokenizer supports action prediction plus a future-image prediction auxiliary task.

The implementation path follows **Encode visual goals → Learn actions and future images → Adapt and collect data**. Work through the original explanation and the atomic tasks below before composing the proposed integration. Published exercises are small, independently graded components; this plan is not a completed or full-paper reproduction.

[Primary source](https://arxiv.org/abs/2306.11706) · [Paper explanation and graph](/projects/2023-robocat) · [All paper tracks](../../PAPER_TRACKS.md)

Source cards: [2023-robocat](../../../research/papers/vla-generalist/2023-robocat.md).

**Available now:** 0 paper-associated runnable components; 1 supporting runnable component. **Proposed:** 3 distinct component ideas, plus integration and assessment. A planned title can be a reviewed blueprint or an unreviewed idea; its presence is not a publication promise.

## Prerequisites and diagnostic

Read the input contracts and locally defined mathematics in the source explanation. Before starting, trace one small input through **Encode visual goals** and identify the shapes, masks, units, coordinate frames and time conventions that apply. This is a robotics diagnostic, not a general Python or mathematics course.

- **Supporting prerequisite:** [Validate a Multimodal Robot Episode Schema](/problems/validate-robot-episodes). Its own contract remains authoritative; it does not implement the entire paper.

## Ordered mechanisms and component tasks

The sequence below is a learning order. The explicit connections retain branching, conditioning and feedback; adjacent entries are not assumed to have interchangeable tensor interfaces.

### 1. Encode visual goals

<!-- source-flow: 2023-robocat#stage-1 -->

Tokenize observations and a desired future image.

[Study the mechanism and math](/projects/2023-robocat#paper-section-encode-visual-goals).

- **Proposed component, not runnable:** Construct Goal-Conditioned Policy Batches.

**Step evidence:** retain a small input/output trace and the invariant described in the linked explanation. Before implementing a proposed task, write and review its blueprint with explicit shapes, units, frames, examples, tolerances and failure behavior.

### 2. Learn actions and future images

<!-- source-flow: 2023-robocat#stage-2 -->

Jointly predict behavior and future visual tokens.

[Study the mechanism and math](/projects/2023-robocat#paper-section-learn-actions-and-future-images).

- **Proposed component, not runnable:** Balance Robot-Task Training Mixtures.

**Step evidence:** retain a small input/output trace and the invariant described in the linked explanation. Before implementing a proposed task, write and review its blueprint with explicit shapes, units, frames, examples, tolerances and failure behavior.

### 3. Adapt and collect data

<!-- source-flow: 2023-robocat#stage-3 -->

Fine-tune on a task, collect trajectories, then retrain the generalist.

[Study the mechanism and math](/projects/2023-robocat#paper-section-adapt-and-collect-data).

- **Runnable supporting prerequisite:** [Validate a Multimodal Robot Episode Schema](/problems/validate-robot-episodes). A signal's missing fraction is missing_rows / T. A timestamp must be finite numeric, and each valid adjacent pair must strictly increase.
- **Proposed component, not runnable:** Track Adaptation Data Lineage.

**Step evidence:** retain a small input/output trace and the invariant described in the linked explanation. Before implementing a proposed task, write and review its blueprint with explicit shapes, units, frames, examples, tolerances and failure behavior.

| From | Signal or dependency | To |
|---|---|---|
| Encode visual goals | goal and observation tokens | Learn actions and future images |
| Learn actions and future images | generalist checkpoint | Adapt and collect data |

## Integration exercise

**Proposed exercise — not runnable yet.** Construct a small synthetic instruction/observation stream and structured action or skill records for two task contexts; use fixed model scores or deterministic callbacks. Compose the selected mechanisms in the declared flow, beginning with **Encode visual goals** and ending with **Adapt and collect data**. Save each intermediate artifact so a learner can locate a mismatch at its originating stage.

The integration boundary is the named representation, conditioning and output/control interface; language reasoning quality, large-model training and physical task completion are outside scope. Treat any stubbed learned stage as a named fixture, never as measured model capability. Author original synthetic data and record its generation rules; external datasets or assets need a separate provenance and license review.

Deliver an executable fixture generator, the component wiring, a compact expected-output trace and a report of the remaining differences from [the paper](/projects/2023-robocat). Proposed pieces must pass blueprint review and isolated evaluation before this integration becomes an available exercise.

## Evaluation and failure analysis

**Proposed assessment — not runnable yet.** For the **Encode visual goals → Adapt and collect data** fixture, verify each decision against explicit token, skill or action targets and record intermediate conditioning state; evaluate grammar, ordering and latency independently.

Use one clean baseline and a separately recorded fault case: change a task identifier, deliver stale context, or supply an invalid output field; ensure the control interface never silently shifts semantics. Identify the affected stage and report its intermediate evidence. Do not average away the failing case.

Before grading, define an independent oracle, exact-versus-tolerant comparisons, allowed dtypes/devices, empty/minimal cases, invalid-input behavior and resource bounds. Compare failure detection and mathematical correctness separately from timing. A synthetic result establishes only the declared component contract; paper benchmark scores and physical safety require their own protocol.

## Reproducibility deliverable

**Proposed final artifact:** an original implementation/model card for **RoboCat: A Self-Improving Generalist Agent for Robotic Manipulation** containing the source revision, exercised and stubbed stages, and an explicit list of omitted paper experiments.

Record task/skill vocabulary, action schema, model callback behavior, context freshness policy, chunk schedule and decoder version. Pin problem/content versions, code revision, Python/dependency versions, evaluator identity, deterministic seeds and fixture hashes. Include the baseline/fault report and runtime observations. If any component updates parameters, record the update count and trainable state; otherwise state that no model was trained.

Package the fixture and expected trace with a machine-readable manifest. Replaying the same manifest must recover the same evidence within declared tolerances. Record limitations and the next unimplemented mechanism; completion of this proposal must not be labeled full-paper reproduction. Research PDFs remain local reference inputs, with canonical sources linked rather than redistributed.
