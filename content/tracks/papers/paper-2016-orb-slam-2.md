---
{
  "schema_version": 1,
  "generated_by": "scripts/generate-paper-tracks.ts",
  "slug": "paper-2016-orb-slam-2",
  "paper_id": "2016-orb-slam-2",
  "title": "ORB-SLAM2: an Open-Source SLAM System for Monocular, Stereo and RGB-D Cameras",
  "status": "planned",
  "primary_url": "https://arxiv.org/abs/1610.06475",
  "source_cards": [
    "research/papers/geometry-calibration-slam/2016-orb-slam-2.md"
  ],
  "paper_aliases": [],
  "category": "geometry-calibration-slam",
  "topics": [
    "geometry-calibration-slam",
    "orb-slam-2"
  ],
  "runnable_problem_slugs": [],
  "proposed_component_count": 3,
  "source_flow_node_count": 3,
  "source_flow_nodes": [
    {
      "card": "2016-orb-slam-2",
      "node": "stage-1"
    },
    {
      "card": "2016-orb-slam-2",
      "node": "stage-2"
    },
    {
      "card": "2016-orb-slam-2",
      "node": "stage-3"
    }
  ],
  "integration_status": "proposed",
  "assessment_status": "proposed"
}
---

# ORB-SLAM2: an Open-Source SLAM System for Monocular, Stereo and RGB-D Cameras — implementation track

## Orientation and scope

ORB-SLAM2 combines ORB feature tracking, local mapping, relocalization, and loop closure for monocular, stereo, and RGB-D cameras. Its map consists of keyframes and 3D landmarks refined through bundle adjustment.

The implementation path follows **Track visual landmarks → Optimize local geometry → Close loops and relocalize**. Work through the original explanation and the atomic tasks below before composing the proposed integration. Published exercises are small, independently graded components; this plan is not a completed or full-paper reproduction.

[Primary source](https://arxiv.org/abs/1610.06475) · [Paper explanation and graph](/projects/2016-orb-slam-2) · [All paper tracks](../../PAPER_TRACKS.md)

Source cards: [2016-orb-slam-2](../../../research/papers/geometry-calibration-slam/2016-orb-slam-2.md).

**Available now:** 0 paper-associated runnable components; 0 supporting runnable components. **Proposed:** 3 distinct component ideas, plus integration and assessment. A planned title can be a reviewed blueprint or an unreviewed idea; its presence is not a publication promise.

## Prerequisites and diagnostic

Read the input contracts and locally defined mathematics in the source explanation. Before starting, trace one small input through **Track visual landmarks** and identify the shapes, masks, units, coordinate frames and time conventions that apply. This is a robotics diagnostic, not a general Python or mathematics course.

There is no independently runnable prerequisite mapped for this source yet. Use the source-card notation and stage contracts as the diagnostic; prerequisite exercises must be authored and reviewed before being presented as runnable.

## Ordered mechanisms and component tasks

The sequence below is a learning order. The explicit connections retain branching, conditioning and feedback; adjacent entries are not assumed to have interchangeable tensor interfaces.

### 1. Track visual landmarks

<!-- source-flow: 2016-orb-slam-2#stage-1 -->

Associate image keypoints with map points.

[Study the mechanism and math](/projects/2016-orb-slam-2#paper-section-track-visual-landmarks).

- **Proposed component, not runnable:** Associate Map Points with Image Features.

**Step evidence:** retain a small input/output trace and the invariant described in the linked explanation. Before implementing a proposed task, write and review its blueprint with explicit shapes, units, frames, examples, tolerances and failure behavior.

### 2. Optimize local geometry

<!-- source-flow: 2016-orb-slam-2#stage-2 -->

Refine keyframe poses and landmark positions.

[Study the mechanism and math](/projects/2016-orb-slam-2#paper-section-optimize-local-geometry).

- **Proposed component, not runnable:** Select Geometric Pose Inliers.

**Step evidence:** retain a small input/output trace and the invariant described in the linked explanation. Before implementing a proposed task, write and review its blueprint with explicit shapes, units, frames, examples, tolerances and failure behavior.

### 3. Close loops and relocalize

<!-- source-flow: 2016-orb-slam-2#stage-3 -->

Recognize previously mapped places and correct drift.

[Study the mechanism and math](/projects/2016-orb-slam-2#paper-section-close-loops-and-relocalize).

- **Proposed component, not runnable:** Evaluate a Relocalization Candidate.

**Step evidence:** retain a small input/output trace and the invariant described in the linked explanation. Before implementing a proposed task, write and review its blueprint with explicit shapes, units, frames, examples, tolerances and failure behavior.

| From | Signal or dependency | To |
|---|---|---|
| Track visual landmarks | feature correspondences | Optimize local geometry |
| Optimize local geometry | keyframe map | Close loops and relocalize |

## Integration exercise

**Proposed exercise — not runnable yet.** Construct a short synthetic calibrated sensor sequence with known camera poses, landmark coordinates and optional inertial samples; use a fixed seed and declare world/body/camera transforms, metres, radians and seconds. Compose the selected mechanisms in the declared flow, beginning with **Track visual landmarks** and ending with **Close loops and relocalize**. Save each intermediate artifact so a learner can locate a mismatch at its originating stage.

The integration boundary is a bounded estimation or reconstruction component with analytic geometry; learned correspondence outputs may be supplied as fixed synthetic arrays. Treat any stubbed learned stage as a named fixture, never as measured model capability. Author original synthetic data and record its generation rules; external datasets or assets need a separate provenance and license review.

Deliver an executable fixture generator, the component wiring, a compact expected-output trace and a report of the remaining differences from [the paper](/projects/2016-orb-slam-2). Proposed pieces must pass blueprint review and isolated evaluation before this integration becomes an available exercise.

## Evaluation and failure analysis

**Proposed assessment — not runnable yet.** For the **Track visual landmarks → Close loops and relocalize** fixture, compare geometric residuals with a direct scalar calculation and compare recovered coordinates with the known synthetic scene; report the chosen alignment and gauge freedoms before giving pose error.

Use one clean baseline and a separately recorded fault case: reverse one transform, perturb one calibration value, or shift one sensor timestamp; report which residual and validity check changes. Identify the affected stage and report its intermediate evidence. Do not average away the failing case.

Before grading, define an independent oracle, exact-versus-tolerant comparisons, allowed dtypes/devices, empty/minimal cases, invalid-input behavior and resource bounds. Compare failure detection and mathematical correctness separately from timing. A synthetic result establishes only the declared component contract; paper benchmark scores and physical safety require their own protocol.

## Reproducibility deliverable

**Proposed final artifact:** an original implementation/model card for **ORB-SLAM2: an Open-Source SLAM System for Monocular, Stereo and RGB-D Cameras** containing the source revision, exercised and stubbed stages, and an explicit list of omitted paper experiments.

Record calibration hash, coordinate-frame convention, sensor clock convention, gauge/alignment choice and residual weights. Pin problem/content versions, code revision, Python/dependency versions, evaluator identity, deterministic seeds and fixture hashes. Include the baseline/fault report and runtime observations. If any component updates parameters, record the update count and trainable state; otherwise state that no model was trained.

Package the fixture and expected trace with a machine-readable manifest. Replaying the same manifest must recover the same evidence within declared tolerances. Record limitations and the next unimplemented mechanism; completion of this proposal must not be labeled full-paper reproduction. Research PDFs remain local reference inputs, with canonical sources linked rather than redistributed.
