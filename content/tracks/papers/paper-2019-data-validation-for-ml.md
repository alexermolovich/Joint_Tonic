---
{
  "schema_version": 1,
  "generated_by": "scripts/generate-paper-tracks.ts",
  "slug": "paper-2019-data-validation-for-ml",
  "paper_id": "2019-data-validation-for-ml",
  "title": "Data Validation for Machine Learning",
  "status": "planned",
  "primary_url": "https://research.google/pubs/data-validation-for-machine-learning",
  "source_cards": [
    "research/papers/mlops-sim2real/2019-data-validation-for-ml.md"
  ],
  "paper_aliases": [],
  "category": "mlops-sim2real",
  "topics": [
    "data-quality",
    "schema-inference",
    "anomaly-detection",
    "training-serving-skew",
    "monitoring"
  ],
  "runnable_problem_slugs": [
    "validate-robot-episodes",
    "infer-robot-episode-schema",
    "robot-feature-anomalies",
    "compare-training-serving-distributions",
    "sensor-timestamp-calibration-skew",
    "critical-data-anomaly-gate"
  ],
  "proposed_component_count": 0,
  "source_flow_node_count": 3,
  "source_flow_nodes": [
    {
      "card": "2019-data-validation-for-ml",
      "node": "stage-1"
    },
    {
      "card": "2019-data-validation-for-ml",
      "node": "stage-2"
    },
    {
      "card": "2019-data-validation-for-ml",
      "node": "stage-3"
    }
  ],
  "integration_status": "proposed",
  "assessment_status": "proposed"
}
---

# Data Validation for Machine Learning — implementation track

## Orientation and scope

Data Validation for Machine Learning treats data checks as a first-class stage of the ML pipeline. It combines schemas, descriptive statistics, and comparisons across data slices or time to detect errors before they propagate into models. The implementation goal is actionable violations with feature identity and context, rather than an unexplained global anomaly score.

The implementation path follows **Define feature contracts → Compare statistics and slices → Review and version anomalies**. Work through the original explanation and the atomic tasks below before composing the proposed integration. Published exercises are small, independently graded components; this plan is not a completed or full-paper reproduction.

[Primary source](https://research.google/pubs/data-validation-for-machine-learning) · [Paper explanation and graph](/projects/2019-data-validation-for-ml) · [All paper tracks](../../PAPER_TRACKS.md)

Source cards: [2019-data-validation-for-ml](../../../research/papers/mlops-sim2real/2019-data-validation-for-ml.md).

**Available now:** 6 paper-associated runnable components; 0 supporting runnable components. **Proposed:** 0 distinct component ideas, plus integration and assessment. A planned title can be a reviewed blueprint or an unreviewed idea; its presence is not a publication promise.

## Prerequisites and diagnostic

Read the input contracts and locally defined mathematics in the source explanation. Before starting, trace one small input through **Define feature contracts** and identify the shapes, masks, units, coordinate frames and time conventions that apply. This is a robotics diagnostic, not a general Python or mathematics course.

There is no independently runnable prerequisite mapped for this source yet. Use the source-card notation and stage contracts as the diagnostic; prerequisite exercises must be authored and reviewed before being presented as runnable.

## Ordered mechanisms and component tasks

The sequence below is a learning order. The explicit connections retain branching, conditioning and feedback; adjacent entries are not assumed to have interchangeable tensor interfaces.

### 1. Define feature contracts

<!-- source-flow: 2019-data-validation-for-ml#stage-1 -->

Declare presence, type, shape, domain, and range requirements.

[Study the mechanism and math](/projects/2019-data-validation-for-ml#paper-section-define-feature-contracts).

- **Runnable paper-associated component:** [Validate a Multimodal Robot Episode Schema](/problems/validate-robot-episodes). A signal's missing fraction is missing_rows / T. A timestamp must be finite numeric, and each valid adjacent pair must strictly increase.
- **Runnable paper-associated component:** [Infer a Schema from Robot Episodes](/problems/infer-robot-episode-schema). Propose signal shapes, metadata and per-channel observed ranges from a bounded collection of robot episodes.
- **Runnable paper-associated component:** [Detect Missing, Range, Domain, and Shape Anomalies](/problems/robot-feature-anomalies). Return located schema violations from robot feature records without treating malformed data as valid zero values.

**Step evidence:** retain a small input/output trace and the invariant described in the linked explanation. Before implementing a proposed task, write and review its blueprint with explicit shapes, units, frames, examples, tolerances and failure behavior.

### 2. Compare statistics and slices

<!-- source-flow: 2019-data-validation-for-ml#stage-2 -->

Identify distribution changes and training-serving differences.

[Study the mechanism and math](/projects/2019-data-validation-for-ml#paper-section-compare-statistics-and-slices).

- **Runnable paper-associated component:** [Compare Training and Serving Distributions](/problems/compare-training-serving-distributions). Compare aligned categorical frequencies while distinguishing distribution shift from dataset size.
- **Runnable paper-associated component:** [Detect Sensor Timestamp and Calibration Skew](/problems/sensor-timestamp-calibration-skew). Compare aligned sensor metadata snapshots and expose timing and calibration mismatches with exact integer arithmetic.

**Step evidence:** retain a small input/output trace and the invariant described in the linked explanation. Before implementing a proposed task, write and review its blueprint with explicit shapes, units, frames, examples, tolerances and failure behavior.

### 3. Review and version anomalies

<!-- source-flow: 2019-data-validation-for-ml#stage-3 -->

Distinguish bad data from an intentional schema change and preserve the decision.

[Study the mechanism and math](/projects/2019-data-validation-for-ml#paper-section-review-and-version-anomalies).

- **Runnable paper-associated component:** [Block a Pipeline on Critical Data Anomalies](/problems/critical-data-anomaly-gate). Gate a pipeline using explicit anomaly severity and required-source coverage while retaining warnings for inspection.

**Step evidence:** retain a small input/output trace and the invariant described in the linked explanation. Before implementing a proposed task, write and review its blueprint with explicit shapes, units, frames, examples, tolerances and failure behavior.

| From | Signal or dependency | To |
|---|---|---|
| Define feature contracts | validated examples | Compare statistics and slices |
| Compare statistics and slices | named anomalies | Review and version anomalies |

## Integration exercise

**Proposed exercise — not runnable yet.** Construct a small synthetic pipeline/configuration graph and scenario metric records, or bounded randomization samples where the selected mechanism requires them. Compose the selected mechanisms in the declared flow, beginning with **Define feature contracts** and ending with **Review and version anomalies**. Save each intermediate artifact so a learner can locate a mismatch at its originating stage.

The integration boundary is data, dependency, evaluation and transfer-check calculations; synthetic acceptance is not evidence of safe deployment or sim-to-real success. Treat any stubbed learned stage as a named fixture, never as measured model capability. Author original synthetic data and record its generation rules; external datasets or assets need a separate provenance and license review.

Deliver an executable fixture generator, the component wiring, a compact expected-output trace and a report of the remaining differences from [the paper](/projects/2019-data-validation-for-ml). Proposed pieces must pass blueprint review and isolated evaluation before this integration becomes an available exercise.

## Evaluation and failure analysis

**Proposed assessment — not runnable yet.** For the **Define feature contracts → Review and version anomalies** fixture, compare dependency and release decisions with known graph/record fixtures and report scenario-level metrics before aggregate conclusions.

Use one clean baseline and a separately recorded fault case: invalidate a dependency, remove one hardware/scenario slice, or perturb a physical parameter outside the declared envelope; expose the precise failure. Identify the affected stage and report its intermediate evidence. Do not average away the failing case.

Before grading, define an independent oracle, exact-versus-tolerant comparisons, allowed dtypes/devices, empty/minimal cases, invalid-input behavior and resource bounds. Compare failure detection and mathematical correctness separately from timing. A synthetic result establishes only the declared component contract; paper benchmark scores and physical safety require their own protocol.

## Reproducibility deliverable

**Proposed final artifact:** an original implementation/model card for **Data Validation for Machine Learning** containing the source revision, exercised and stubbed stages, and an explicit list of omitted paper experiments.

Record pipeline/configuration digest, simulator or hardware label, randomization bounds, timing units, scenario definitions and release criteria. Pin problem/content versions, code revision, Python/dependency versions, evaluator identity, deterministic seeds and fixture hashes. Include the baseline/fault report and runtime observations. If any component updates parameters, record the update count and trainable state; otherwise state that no model was trained.

Package the fixture and expected trace with a machine-readable manifest. Replaying the same manifest must recover the same evidence within declared tolerances. Record limitations and the next unimplemented mechanism; completion of this proposal must not be labeled full-paper reproduction. Research PDFs remain local reference inputs, with canonical sources linked rather than redistributed.
