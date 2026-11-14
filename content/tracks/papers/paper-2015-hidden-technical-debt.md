---
{
  "schema_version": 1,
  "generated_by": "scripts/generate-paper-tracks.ts",
  "slug": "paper-2015-hidden-technical-debt",
  "paper_id": "2015-hidden-technical-debt",
  "title": "Hidden Technical Debt in Machine Learning Systems",
  "status": "planned",
  "primary_url": "https://proceedings.neurips.cc/paper/2015/hash/86df7dcfd896fcaf2674f757a2463eba-Abstract.html",
  "source_cards": [
    "research/papers/mlops-sim2real/2015-hidden-technical-debt.md"
  ],
  "paper_aliases": [],
  "category": "mlops-sim2real",
  "topics": [
    "mlops",
    "technical-debt",
    "dependency-management",
    "monitoring",
    "production-ml"
  ],
  "runnable_problem_slugs": [
    "dependency-graph-blast-radius",
    "detect-pipeline-feedback-loops",
    "slice-infrastructure-release-gate",
    "physical-ai-incident-triage"
  ],
  "proposed_component_count": 0,
  "source_flow_node_count": 3,
  "source_flow_nodes": [
    {
      "card": "2015-hidden-technical-debt",
      "node": "stage-1"
    },
    {
      "card": "2015-hidden-technical-debt",
      "node": "stage-2"
    },
    {
      "card": "2015-hidden-technical-debt",
      "node": "stage-3"
    }
  ],
  "integration_status": "proposed",
  "assessment_status": "proposed"
}
---

# Hidden Technical Debt in Machine Learning Systems — implementation track

## Orientation and scope

Hidden Technical Debt in Machine Learning Systems explains why a model’s surrounding data and software dependencies can dominate long-term maintenance cost. Changing one feature or dataset can affect many downstream consumers; feedback loops can change the data that future training receives. The paper is a systems analysis, not a new learning algorithm. The linked explanation’s equations are explicit teaching models for reasoning about its dependency risks.

The implementation path follows **Map system dependencies → Inspect coupling and feedback → Control and observe changes**. Work through the original explanation and the atomic tasks below before composing the proposed integration. Published exercises are small, independently graded components; this plan is not a completed or full-paper reproduction.

[Primary source](https://proceedings.neurips.cc/paper/2015/hash/86df7dcfd896fcaf2674f757a2463eba-Abstract.html) · [Paper explanation and graph](/projects/2015-hidden-technical-debt) · [All paper tracks](../../PAPER_TRACKS.md)

Source cards: [2015-hidden-technical-debt](../../../research/papers/mlops-sim2real/2015-hidden-technical-debt.md).

**Available now:** 2 paper-associated runnable components; 2 supporting runnable components. **Proposed:** 0 distinct component ideas, plus integration and assessment. A planned title can be a reviewed blueprint or an unreviewed idea; its presence is not a publication promise.

## Prerequisites and diagnostic

Read the input contracts and locally defined mathematics in the source explanation. Before starting, trace one small input through **Map system dependencies** and identify the shapes, masks, units, coordinate frames and time conventions that apply. This is a robotics diagnostic, not a general Python or mathematics course.

- **Supporting prerequisite:** [Gate a Release on Slice and Infrastructure Tests](/problems/slice-infrastructure-release-gate). Its own contract remains authoritative; it does not implement the entire paper.
- **Supporting prerequisite:** [Triage a Physical-AI Deployment Incident](/problems/physical-ai-incident-triage). Its own contract remains authoritative; it does not implement the entire paper.
- **Supporting prerequisite:** [Compute Dependency-Graph Blast Radius](/problems/dependency-graph-blast-radius). Its own contract remains authoritative; it does not implement the entire paper.

## Ordered mechanisms and component tasks

The sequence below is a learning order. The explicit connections retain branching, conditioning and feedback; adjacent entries are not assumed to have interchangeable tensor interfaces.

### 1. Map system dependencies

<!-- source-flow: 2015-hidden-technical-debt#stage-1 -->

Record data sources, transforms, models, and downstream consumers as a directed graph.

[Study the mechanism and math](/projects/2015-hidden-technical-debt#paper-section-map-system-dependencies).

- **Runnable paper-associated component:** [Compute Dependency-Graph Blast Radius](/problems/dependency-graph-blast-radius). Identify declared downstream consumers affected by a component change.

**Step evidence:** retain a small input/output trace and the invariant described in the linked explanation. Before implementing a proposed task, write and review its blueprint with explicit shapes, units, frames, examples, tolerances and failure behavior.

### 2. Inspect coupling and feedback

<!-- source-flow: 2015-hidden-technical-debt#stage-2 -->

Find changes that can alter both predictions and future training inputs.

[Study the mechanism and math](/projects/2015-hidden-technical-debt#paper-section-inspect-coupling-and-feedback).

- **Runnable paper-associated component:** [Detect Feedback Loops in an ML Pipeline](/problems/detect-pipeline-feedback-loops). Group declared pipeline components that participate in the same directed feedback cycle.

**Step evidence:** retain a small input/output trace and the invariant described in the linked explanation. Before implementing a proposed task, write and review its blueprint with explicit shapes, units, frames, examples, tolerances and failure behavior.

### 3. Control and observe changes

<!-- source-flow: 2015-hidden-technical-debt#stage-3 -->

Make ownership, validation, rollback, and consumer contracts explicit.

[Study the mechanism and math](/projects/2015-hidden-technical-debt#paper-section-control-and-observe-changes).

- **Runnable supporting prerequisite:** [Gate a Release on Slice and Infrastructure Tests](/problems/slice-infrastructure-release-gate). Reject a candidate when any required scenario or infrastructure check lacks current passing evidence.
- **Runnable supporting prerequisite:** [Triage a Physical-AI Deployment Incident](/problems/physical-ai-incident-triage). Reduce a bounded event window into a deterministic operator queue without confusing duplicates, stale events or severity.

**Step evidence:** retain a small input/output trace and the invariant described in the linked explanation. Before implementing a proposed task, write and review its blueprint with explicit shapes, units, frames, examples, tolerances and failure behavior.

| From | Signal or dependency | To |
|---|---|---|
| Map system dependencies | dependency graph | Inspect coupling and feedback |
| Inspect coupling and feedback | impact analysis | Control and observe changes |

## Integration exercise

**Proposed exercise — not runnable yet.** Construct a small directed dependency graph containing a dataset, a transform, a model and declared consumers. Keep a separate synthetic observation log that reveals one undeclared consumer. Add a model-output-to-training-data feedback cycle, change one upstream artifact and compose downstream blast-radius and feedback-cycle analysis. Produce an impact report that distinguishes declared reachability from dependencies discovered through the log.

The integration boundary is dependency discovery, change-impact propagation and feedback analysis over synthetic graphs and event records; organizational debt and operational risk are not reduced to a single graph score. Treat any stubbed learned stage as a named fixture, never as measured model capability. Author original synthetic data and record its generation rules; external datasets or assets need a separate provenance and license review.

Deliver an executable fixture generator, the component wiring, a compact expected-output trace and a report of the remaining differences from [the paper](/projects/2015-hidden-technical-debt). Proposed pieces must pass blueprint review and isolated evaluation before this integration becomes an available exercise.

## Evaluation and failure analysis

**Proposed assessment — not runnable yet.** Compare downstream reachability and strongly connected feedback groups with independently enumerated tiny-graph expectations. Include a disconnected consumer, a cycle and a changed upstream dataset. Inject the missing consumer only into the observation log and verify that the declared graph alone does not claim to discover it; report the discrepancy and the effect of adding the missing edge.

Use one clean baseline and a separately recorded fault case: omit one observed consumer from the declared graph, then compare the graph-derived impact set with the synthetic observation log; retain the missing edge as explicit evidence. Identify the affected stage and report its intermediate evidence. Do not average away the failing case.

Before grading, define an independent oracle, exact-versus-tolerant comparisons, allowed dtypes/devices, empty/minimal cases, invalid-input behavior and resource bounds. Compare failure detection and mathematical correctness separately from timing. A synthetic result establishes only the declared component contract; paper benchmark scores and physical safety require their own protocol.

## Reproducibility deliverable

**Proposed final artifact:** an original implementation/model card for **Hidden Technical Debt in Machine Learning Systems** containing the source revision, exercised and stubbed stages, and an explicit list of omitted paper experiments.

Record node identities and owners, edge meaning and direction, graph snapshot hash, upstream artifact version, observation-log coverage, change event and reachability/cycle-reporting conventions. Pin problem/content versions, code revision, Python/dependency versions, evaluator identity, deterministic seeds and fixture hashes. Include the baseline/fault report and runtime observations. If any component updates parameters, record the update count and trainable state; otherwise state that no model was trained.

Package the fixture and expected trace with a machine-readable manifest. Replaying the same manifest must recover the same evidence within declared tolerances. Record limitations and the next unimplemented mechanism; completion of this proposal must not be labeled full-paper reproduction. Research PDFs remain local reference inputs, with canonical sources linked rather than redistributed.
