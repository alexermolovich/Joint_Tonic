---
{
  "schema_version": 1,
  "generated_by": "scripts/generate-paper-tracks.ts",
  "slug": "paper-2021-rlds",
  "paper_id": "2021-rlds",
  "title": "RLDS: an Ecosystem to Generate, Share and Use Datasets in Reinforcement Learning",
  "status": "planned",
  "primary_url": "https://arxiv.org/abs/2111.02767",
  "source_cards": [
    "research/papers/mlops-data-deployment/2021-rlds.md"
  ],
  "paper_aliases": [],
  "category": "mlops-data-deployment",
  "topics": [
    "dataset schemas",
    "episode boundaries",
    "reproducibility",
    "data pipelines"
  ],
  "runnable_problem_slugs": [
    "validate-robot-episodes",
    "oxe-version-dataset-manifest",
    "interpolate-joint-state",
    "window-episode-without-crossing-boundaries",
    "act-sliding-action-chunks",
    "record-artifact-lineage"
  ],
  "proposed_component_count": 0,
  "source_flow_node_count": 3,
  "source_flow_nodes": [
    {
      "card": "2021-rlds",
      "node": "record"
    },
    {
      "card": "2021-rlds",
      "node": "align"
    },
    {
      "card": "2021-rlds",
      "node": "transform"
    }
  ],
  "integration_status": "proposed",
  "assessment_status": "proposed"
}
---

# RLDS: an Ecosystem to Generate, Share and Use Datasets in Reinforcement Learning — implementation track

## Orientation and scope

RLDS treats a dataset as episodes containing ordered steps, together with metadata. This preserves information that flat observation/action pairs can discard. The central engineering problem is semantic consistency across collection, transformation and consumption; RLDS is not a new policy architecture or loss function.

The implementation path follows **Record lossless episode structure → Align observations actions and rewards → Build reproducible training views**. Work through the original explanation and the atomic tasks below before composing the proposed integration. Published exercises are small, independently graded components; this plan is not a completed or full-paper reproduction.

[Primary source](https://arxiv.org/abs/2111.02767) · [Paper explanation and graph](/projects/2021-rlds) · [All paper tracks](../../PAPER_TRACKS.md)

Source cards: [2021-rlds](../../../research/papers/mlops-data-deployment/2021-rlds.md).

**Available now:** 0 paper-associated runnable components; 6 supporting runnable components. **Proposed:** 0 distinct component ideas, plus integration and assessment. A planned title can be a reviewed blueprint or an unreviewed idea; its presence is not a publication promise.

## Prerequisites and diagnostic

Read the input contracts and locally defined mathematics in the source explanation. Before starting, trace one small input through **Record lossless episode structure** and identify the shapes, masks, units, coordinate frames and time conventions that apply. This is a robotics diagnostic, not a general Python or mathematics course.

- **Supporting prerequisite:** [Validate a Multimodal Robot Episode Schema](/problems/validate-robot-episodes). Its own contract remains authoritative; it does not implement the entire paper.
- **Supporting prerequisite:** [Version a Cross-Robot Dataset Manifest](/problems/oxe-version-dataset-manifest). Its own contract remains authoritative; it does not implement the entire paper.
- **Supporting prerequisite:** [Interpolate Joint State at Camera Time](/problems/interpolate-joint-state). Its own contract remains authoritative; it does not implement the entire paper.
- **Supporting prerequisite:** [Window an Episode Without Crossing Boundaries](/problems/window-episode-without-crossing-boundaries). Its own contract remains authoritative; it does not implement the entire paper.
- **Supporting prerequisite:** [Build Sliding Action Chunks with Padding Masks](/problems/act-sliding-action-chunks). Its own contract remains authoritative; it does not implement the entire paper.
- **Supporting prerequisite:** [Record Dataset, Transform, Model, and Evaluator Lineage](/problems/record-artifact-lineage). Its own contract remains authoritative; it does not implement the entire paper.

## Ordered mechanisms and component tasks

The sequence below is a learning order. The explicit connections retain branching, conditioning and feedback; adjacent entries are not assumed to have interchangeable tensor interfaces.

### 1. Record lossless episode structure

<!-- source-flow: 2021-rlds#record -->

Record lossless episode structure. See the original explanation and component status below.

[Study the mechanism and math](/projects/2021-rlds#paper-section-record-lossless-episode-structure).

- **Runnable supporting prerequisite:** [Validate a Multimodal Robot Episode Schema](/problems/validate-robot-episodes). A signal's missing fraction is missing_rows / T. A timestamp must be finite numeric, and each valid adjacent pair must strictly increase.
- **Runnable supporting prerequisite:** [Version a Cross-Robot Dataset Manifest](/problems/oxe-version-dataset-manifest). A mixed dataset needs an identity that includes its versions, embodiments and calibration.

**Step evidence:** retain a small input/output trace and the invariant described in the linked explanation. Before implementing a proposed task, write and review its blueprint with explicit shapes, units, frames, examples, tolerances and failure behavior.

### 2. Align observations actions and rewards

<!-- source-flow: 2021-rlds#align -->

Align observations actions and rewards. See the original explanation and component status below.

[Study the mechanism and math](/projects/2021-rlds#paper-section-align-observations-actions-and-rewards).

- **Runnable supporting prerequisite:** [Interpolate Joint State at Camera Time](/problems/interpolate-joint-state). Align unwrapped encoder angles to camera timestamps without crossing sensor dropouts.
- **Runnable supporting prerequisite:** [Window an Episode Without Crossing Boundaries](/problems/window-episode-without-crossing-boundaries). Generate fixed-length row-index windows wholly contained in individual contiguous episodes.

**Step evidence:** retain a small input/output trace and the invariant described in the linked explanation. Before implementing a proposed task, write and review its blueprint with explicit shapes, units, frames, examples, tolerances and failure behavior.

### 3. Build reproducible training views

<!-- source-flow: 2021-rlds#transform -->

Build reproducible training views. See the original explanation and component status below.

[Study the mechanism and math](/projects/2021-rlds#paper-section-build-reproducible-training-views).

- **Runnable supporting prerequisite:** [Build Sliding Action Chunks with Padding Masks](/problems/act-sliding-action-chunks). Extract fixed-horizon action windows from one episode while marking right-padding and preserving requested start order.
- **Runnable supporting prerequisite:** [Record Dataset, Transform, Model, and Evaluator Lineage](/problems/record-artifact-lineage). Build a dependency-complete provenance record for one artifact while preserving the identity of every upstream input.

**Step evidence:** retain a small input/output trace and the invariant described in the linked explanation. Before implementing a proposed task, write and review its blueprint with explicit shapes, units, frames, examples, tolerances and failure behavior.

| From | Signal or dependency | To |
|---|---|---|
| Record lossless episode structure | validated component output | Align observations actions and rewards |
| Align observations actions and rewards | validated component output | Build reproducible training views |

## Integration exercise

**Proposed exercise — not runnable yet.** Create two original three-step episodes with distinct recording-end and terminal flags. Preserve step metadata, convert a declared observation/action/reward alignment, then construct windows and a lineage record without crossing episode boundaries. The existing teaching schema is a prerequisite; full RLDS compatibility is not implied.

The integration boundary is the named data/evaluation/deployment logic over synthetic records; no distributed cluster, hosted deployment or production-performance claim is required. Treat any stubbed learned stage as a named fixture, never as measured model capability. Author original synthetic data and record its generation rules; external datasets or assets need a separate provenance and license review.

Deliver an executable fixture generator, the component wiring, a compact expected-output trace and a report of the remaining differences from [the paper](/projects/2021-rlds). Proposed pieces must pass blueprint review and isolated evaluation before this integration becomes an available exercise.

## Evaluation and failure analysis

**Proposed assessment — not runnable yet.** Use a time-limit ending and a true terminal ending to test that is_last and is_terminal remain distinct. Verify that the final SAR observation has no invented outgoing action/reward and that transformations retain provenance.

Use one clean baseline and a separately recorded fault case: change an artifact version, omit required evidence, or skew one scenario slice; make the failed invariant and affected artifact explicit. Identify the affected stage and report its intermediate evidence. Do not average away the failing case.

Before grading, define an independent oracle, exact-versus-tolerant comparisons, allowed dtypes/devices, empty/minimal cases, invalid-input behavior and resource bounds. Compare failure detection and mathematical correctness separately from timing. A synthetic result establishes only the declared component contract; paper benchmark scores and physical safety require their own protocol.

## Reproducibility deliverable

**Proposed final artifact:** an original implementation/model card for **RLDS: an Ecosystem to Generate, Share and Use Datasets in Reinforcement Learning** containing the source revision, exercised and stubbed stages, and an explicit list of omitted paper experiments.

Record schema version, artifact hashes, split/grouping policy, units, metric aggregation rule and decision thresholds. Pin problem/content versions, code revision, Python/dependency versions, evaluator identity, deterministic seeds and fixture hashes. Include the baseline/fault report and runtime observations. If any component updates parameters, record the update count and trainable state; otherwise state that no model was trained.

Package the fixture and expected trace with a machine-readable manifest. Replaying the same manifest must recover the same evidence within declared tolerances. Record limitations and the next unimplemented mechanism; completion of this proposal must not be labeled full-paper reproduction. Research PDFs remain local reference inputs, with canonical sources linked rather than redistributed.
