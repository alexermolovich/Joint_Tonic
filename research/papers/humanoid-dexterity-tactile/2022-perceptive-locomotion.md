---
schema_version: 1
paper_id: "2022-perceptive-locomotion"
title: "Learning robust perceptive locomotion for quadrupedal robots in the wild"
authors: ["Miki, Takahiro","Lee, Joonho","Hwangbo, Jemin","Wellhausen, Lorenz","Koltun, Vladlen","Hutter, Marco"]
year: 2022
venue_or_status: "Author-deposited arXiv manuscript; final venue not asserted by this acquisition card."
primary_url: "https://arxiv.org/abs/2201.08117"
pdf_url: "https://arxiv.org/pdf/2201.08117"
local_pdf: "./2022-perceptive-locomotion.pdf"
sha256: "f54ecada187bd0599dad0452d63f462399d1df64a7713f5d1ad744eada3710c9"
bytes: 38674018
pages: 22
topics: ["humanoid-dexterity-tactile","perceptive-locomotion"]
modalities: ["proprioception","contacts","tactile","motion"]
track_role: "supporting"
open_access_status: "open-access-preprint"
redistribution_note: "Research copy only; verify the source license before redistribution."
---

# Learning robust perceptive locomotion for quadrupedal robots in the wild

## Agent brief

Study perceptive locomotion through terrain sensing, state estimation, and control interfaces. This acquisition card verifies the primary paper identity and local PDF, and proposes components that can become independently testable Joint Tonic problems. Full-text technical review is required before promoting an idea into a reviewed problem blueprint.

## Contribution

Study perceptive locomotion through terrain sensing, state estimation, and control interfaces.

The proposed exercises below are original teaching decompositions. They do not assert a full reproduction of the paper or any published performance number.

## Prerequisite concepts

- Kinematics, contact state, reward decomposition, imitation learning, tactile reference images, and safe rollout metrics.

## Method map

| Component candidate | Input | Output | Core invariant | Good exercise boundary |
|---|---|---|---|---|
| Align Terrain Samples to the Robot Frame | Body/hand states, reference motions, contact or tactile observations, and task goals | Aligned motion features, reward terms, adaptation state, or robustness reports | Check phase alignment, contact masks, frame/units consistency, missing tactile frames, finite rewards, and per-object/terrain aggregation. | One bounded function or validation stage |
| Detect Stale Perception in a Control Window | Body/hand states, reference motions, contact or tactile observations, and task goals | Aligned motion features, reward terms, adaptation state, or robustness reports | Check phase alignment, contact masks, frame/units consistency, missing tactile frames, finite rewards, and per-object/terrain aggregation. | One bounded function or validation stage |
| Evaluate Foot Clearance Across Terrain Slices | Body/hand states, reference motions, contact or tactile observations, and task goals | Aligned motion features, reward terms, adaptation state, or robustness reports | Check phase alignment, contact masks, frame/units consistency, missing tactile frames, finite rewards, and per-object/terrain aggregation. | One bounded function or validation stage |

## Data and evaluation

A small teaching implementation should use synthetic or separately licensed fixtures. Check phase alignment, contact masks, frame/units consistency, missing tactile frames, finite rewards, and per-object/terrain aggregation. Dataset names, exact protocol details, published metrics, and hardware requirements must be checked in the source PDF during full-text review; they are not inferred from an awesome-list entry. Keep educational component tests distinct from the paper's end-to-end evaluation.

## Limitations and failure modes

- This is a concise acquisition card, not a full-text technical review. Confirm equations, architecture details, and paper-stated limitations in the PDF before authoring theory.
- Passing synthetic component tests does not establish real-robot performance, robustness, or safe deployment.
- Record actuator/sensor limits, morphology, contact settings, calibration, and motion-data provenance; monitor falls, slip, intervention rate, and distribution shifts.
- The paper, linked code, datasets, assets, and weights may carry different license conditions.

## Implementation decomposition

1. Align Terrain Samples to the Robot Frame.
2. Detect Stale Perception in a Control Window.
3. Evaluate Foot Clearance Across Terrain Slices.
4. Integrate the components on a small fixed fixture and record all deviations from the paper.
5. Add failure slices and a reproducible artifact report.

## Problem blueprints

### Problem: Align Terrain Samples to the Robot Frame

- **Type:** component
- **Difficulty:** medium
- **Learning objective:** Implement and explain the align terrain samples to the robot frame component.
- **Inputs:** Body/hand states, reference motions, contact or tactile observations, and task goals; finalize exact shapes, dtypes, units, frames, masks, and valid ranges during blueprint review.
- **Outputs:** Aligned motion features, reward terms, adaptation state, or robustness reports; specify order and mutation semantics in the reviewed blueprint.
- **Fixture:** Original synthetic examples; any paper dataset requires separate license and split review.
- **Grading:** Check phase alignment, contact masks, frame/units consistency, missing tactile frames, finite rewards, and per-object/terrain aggregation. Add at least two public cases plus hidden tests for documented edge families.
- **Paper deviation:** Isolate one mechanism with bounded arrays or recorded trajectories; no claim of full-scale paper reproduction.

### Problem: Detect Stale Perception in a Control Window

- **Type:** component
- **Difficulty:** hard
- **Learning objective:** Implement and explain the detect stale perception in a control window component.
- **Inputs:** Body/hand states, reference motions, contact or tactile observations, and task goals; finalize exact shapes, dtypes, units, frames, masks, and valid ranges during blueprint review.
- **Outputs:** Aligned motion features, reward terms, adaptation state, or robustness reports; specify order and mutation semantics in the reviewed blueprint.
- **Fixture:** Original synthetic examples; any paper dataset requires separate license and split review.
- **Grading:** Check phase alignment, contact masks, frame/units consistency, missing tactile frames, finite rewards, and per-object/terrain aggregation. Add at least two public cases plus hidden tests for documented edge families.
- **Paper deviation:** Isolate one mechanism with bounded arrays or recorded trajectories; no claim of full-scale paper reproduction.

### Problem: Evaluate Foot Clearance Across Terrain Slices

- **Type:** pipeline
- **Difficulty:** hard
- **Learning objective:** Implement and explain the evaluate foot clearance across terrain slices component.
- **Inputs:** Body/hand states, reference motions, contact or tactile observations, and task goals; finalize exact shapes, dtypes, units, frames, masks, and valid ranges during blueprint review.
- **Outputs:** Aligned motion features, reward terms, adaptation state, or robustness reports; specify order and mutation semantics in the reviewed blueprint.
- **Fixture:** Original synthetic examples; any paper dataset requires separate license and split review.
- **Grading:** Check phase alignment, contact masks, frame/units consistency, missing tactile frames, finite rewards, and per-object/terrain aggregation. Add at least two public cases plus hidden tests for documented edge families.
- **Paper deviation:** Isolate one mechanism with bounded arrays or recorded trajectories; no claim of full-scale paper reproduction.

## Visual teaching plan

- Overlay terrain heights and desired footholds around the moving robot.
- Provide labeled axes, units, coordinate frames, and an equivalent table/text view. Use discrete steps when reduced motion is requested.
- Author diagrams independently; do not copy paper figures or captions.

## MLOps and deployment extensions

- Record actuator/sensor limits, morphology, contact settings, calibration, and motion-data provenance; monitor falls, slip, intervention rate, and distribution shifts.
- Store paper ID, fixture hash, evaluator version, dependency lock, runtime digest, seed, and resource class with every result.
- Use structured failure reasons and per-slice metrics to distinguish implementation mistakes, distribution shifts, and infrastructure failures.

## Canonical sources

- [Primary arXiv record](https://arxiv.org/abs/2201.08117)
- [Open-access author manuscript](https://arxiv.org/pdf/2201.08117)

Identity metadata was read from the primary arXiv record. Local file signature, byte count, page parsing, and SHA-256 were verified on acquisition.

