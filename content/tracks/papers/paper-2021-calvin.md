---
{
  "schema_version": 1,
  "generated_by": "scripts/generate-paper-tracks.ts",
  "slug": "paper-2021-calvin",
  "paper_id": "2021-calvin",
  "title": "CALVIN: A Benchmark for Language-Conditioned Policy Learning for Long-Horizon Robot Manipulation Tasks",
  "status": "planned",
  "primary_url": "https://arxiv.org/abs/2112.03227",
  "source_cards": [
    "research/papers/mlops-data-deployment/2021-calvin.md"
  ],
  "paper_aliases": [],
  "category": "mlops-data-deployment",
  "topics": [
    "mlops-data-deployment",
    "calvin"
  ],
  "runnable_problem_slugs": [
    "validate-robot-episodes"
  ],
  "proposed_component_count": 3,
  "source_flow_node_count": 3,
  "source_flow_nodes": [
    {
      "card": "2021-calvin",
      "node": "stage-1"
    },
    {
      "card": "2021-calvin",
      "node": "stage-2"
    },
    {
      "card": "2021-calvin",
      "node": "stage-3"
    }
  ],
  "integration_status": "proposed",
  "assessment_status": "proposed"
}
---

# CALVIN: A Benchmark for Language-Conditioned Policy Learning for Long-Horizon Robot Manipulation Tasks — implementation track

## Orientation and scope

CALVIN evaluates language-conditioned manipulation over long sequences in multiple simulated environments. Play data supports learning reusable behaviors, while sequential instruction evaluation exposes error accumulation that isolated tasks can hide.

The implementation path follows **Prepare play and language → Execute instruction chains → Measure long-horizon generalization**. Work through the original explanation and the atomic tasks below before composing the proposed integration. Published exercises are small, independently graded components; this plan is not a completed or full-paper reproduction.

[Primary source](https://arxiv.org/abs/2112.03227) · [Paper explanation and graph](/projects/2021-calvin) · [All paper tracks](../../PAPER_TRACKS.md)

Source cards: [2021-calvin](../../../research/papers/mlops-data-deployment/2021-calvin.md).

**Available now:** 0 paper-associated runnable components; 1 supporting runnable component. **Proposed:** 3 distinct component ideas, plus integration and assessment. A planned title can be a reviewed blueprint or an unreviewed idea; its presence is not a publication promise.

## Prerequisites and diagnostic

Read the input contracts and locally defined mathematics in the source explanation. Before starting, trace one small input through **Prepare play and language** and identify the shapes, masks, units, coordinate frames and time conventions that apply. This is a robotics diagnostic, not a general Python or mathematics course.

- **Supporting prerequisite:** [Validate a Multimodal Robot Episode Schema](/problems/validate-robot-episodes). Its own contract remains authoritative; it does not implement the entire paper.

## Ordered mechanisms and component tasks

The sequence below is a learning order. The explicit connections retain branching, conditioning and feedback; adjacent entries are not assumed to have interchangeable tensor interfaces.

### 1. Prepare play and language

<!-- source-flow: 2021-calvin#stage-1 -->

Associate temporally grounded instructions with robot experience.

[Study the mechanism and math](/projects/2021-calvin#paper-section-prepare-play-and-language).

- **Runnable supporting prerequisite:** [Validate a Multimodal Robot Episode Schema](/problems/validate-robot-episodes). A signal's missing fraction is missing_rows / T. A timestamp must be finite numeric, and each valid adjacent pair must strictly increase.
- **Proposed component, not runnable:** Validate Language-to-Episode Annotations.

**Step evidence:** retain a small input/output trace and the invariant described in the linked explanation. Before implementing a proposed task, write and review its blueprint with explicit shapes, units, frames, examples, tolerances and failure behavior.

### 2. Execute instruction chains

<!-- source-flow: 2021-calvin#stage-2 -->

Continue from each achieved task state into the next instruction.

[Study the mechanism and math](/projects/2021-calvin#paper-section-execute-instruction-chains).

- **Proposed component, not runnable:** Segment a Long-Horizon Robot Rollout.

**Step evidence:** retain a small input/output trace and the invariant described in the linked explanation. Before implementing a proposed task, write and review its blueprint with explicit shapes, units, frames, examples, tolerances and failure behavior.

### 3. Measure long-horizon generalization

<!-- source-flow: 2021-calvin#stage-3 -->

Report chain performance on declared environment splits.

[Study the mechanism and math](/projects/2021-calvin#paper-section-measure-long-horizon-generalization).

- **Proposed component, not runnable:** Score Chained Task Success.

**Step evidence:** retain a small input/output trace and the invariant described in the linked explanation. Before implementing a proposed task, write and review its blueprint with explicit shapes, units, frames, examples, tolerances and failure behavior.

| From | Signal or dependency | To |
|---|---|---|
| Prepare play and language | language-conditioned policy | Execute instruction chains |
| Execute instruction chains | rollout outcomes | Measure long-horizon generalization |

## Integration exercise

**Proposed exercise — not runnable yet.** Construct a compact original set of artifact records, episode metadata, metrics and resource traces matched to the selected system; include one known inconsistent record. Compose the selected mechanisms in the declared flow, beginning with **Prepare play and language** and ending with **Measure long-horizon generalization**. Save each intermediate artifact so a learner can locate a mismatch at its originating stage.

The integration boundary is the named data/evaluation/deployment logic over synthetic records; no distributed cluster, hosted deployment or production-performance claim is required. Treat any stubbed learned stage as a named fixture, never as measured model capability. Author original synthetic data and record its generation rules; external datasets or assets need a separate provenance and license review.

Deliver an executable fixture generator, the component wiring, a compact expected-output trace and a report of the remaining differences from [the paper](/projects/2021-calvin). Proposed pieces must pass blueprint review and isolated evaluation before this integration becomes an available exercise.

## Evaluation and failure analysis

**Proposed assessment — not runnable yet.** For the **Prepare play and language → Measure long-horizon generalization** fixture, compare lineage, selected records, aggregate statistics or release decisions with a hand-audited expected report; count false acceptance and false rejection separately.

Use one clean baseline and a separately recorded fault case: change an artifact version, omit required evidence, or skew one scenario slice; make the failed invariant and affected artifact explicit. Identify the affected stage and report its intermediate evidence. Do not average away the failing case.

Before grading, define an independent oracle, exact-versus-tolerant comparisons, allowed dtypes/devices, empty/minimal cases, invalid-input behavior and resource bounds. Compare failure detection and mathematical correctness separately from timing. A synthetic result establishes only the declared component contract; paper benchmark scores and physical safety require their own protocol.

## Reproducibility deliverable

**Proposed final artifact:** an original implementation/model card for **CALVIN: A Benchmark for Language-Conditioned Policy Learning for Long-Horizon Robot Manipulation Tasks** containing the source revision, exercised and stubbed stages, and an explicit list of omitted paper experiments.

Record schema version, artifact hashes, split/grouping policy, units, metric aggregation rule and decision thresholds. Pin problem/content versions, code revision, Python/dependency versions, evaluator identity, deterministic seeds and fixture hashes. Include the baseline/fault report and runtime observations. If any component updates parameters, record the update count and trainable state; otherwise state that no model was trained.

Package the fixture and expected trace with a machine-readable manifest. Replaying the same manifest must recover the same evidence within declared tolerances. Record limitations and the next unimplemented mechanism; completion of this proposal must not be labeled full-paper reproduction. Research PDFs remain local reference inputs, with canonical sources linked rather than redistributed.
