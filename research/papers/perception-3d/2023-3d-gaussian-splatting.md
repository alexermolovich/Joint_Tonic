---
schema_version: 1
paper_id: "2023-3d-gaussian-splatting"
title: "3D Gaussian Splatting for Real-Time Radiance Field Rendering"
authors: ["Kerbl, Bernhard","Kopanas, Georgios","Leimkühler, Thomas","Drettakis, George"]
year: 2023
venue_or_status: "Author-deposited arXiv manuscript; final venue not asserted by this acquisition card."
primary_url: "https://arxiv.org/abs/2308.04079"
pdf_url: "https://arxiv.org/pdf/2308.04079"
local_pdf: "./2023-3d-gaussian-splatting.pdf"
sha256: "f4c0c9f27e2d02b0265017f66049d471eb66cb50203bc918f51ba07d20cbbe11"
bytes: 35829709
pages: 14
topics: ["perception-3d","3d-gaussian-splatting"]
modalities: ["rgb","depth","point-clouds"]
track_role: "supporting"
open_access_status: "open-access-preprint"
redistribution_note: "Research copy only; verify the source license before redistribution."
execution_flow: {"title":"Core execution flow","description":"Parameterize valid 3D Gaussians, project their covariance into the camera, and composite ordered contributions to render pixels.","nodes":[{"id":"stage-1","title":"Parameterize scene primitives","detail":"Use positions, rotations, scales, opacity, and view-dependent color.","column":0,"row":0,"section":"Parameterize scene primitives","problem_slugs":[],"planned_problems":["Build Gaussian Covariances from Rotation and Scale"]},{"id":"stage-2","title":"Project Gaussian footprints","detail":"Approximate perspective projection locally with a Jacobian.","column":1,"row":0,"section":"Project Gaussian footprints","problem_slugs":[],"planned_problems":["Project anisotropic covariance into an image"]},{"id":"stage-3","title":"Composite visible contributions","detail":"Accumulate sorted opacity-weighted colors and optimize image agreement.","column":2,"row":0,"section":"Composite visible contributions","problem_slugs":[],"planned_problems":["Composite depth-ordered Gaussian contributions","Measure primitive contribution for density control"]}],"edges":[{"from":"stage-1","to":"stage-2","label":"3D primitives"},{"from":"stage-2","to":"stage-3","label":"image-space splats"}]}
---

## Core paper explanation

3D Gaussian Splatting represents a scene as explicit anisotropic Gaussian primitives with learnable position, covariance, opacity, and appearance. Rendering projects those primitives into image-space ellipses and composites their contributions in visibility order. Optimization changes both primitive parameters and their density, allowing a compact explicit scene to explain observed images.

## Execution flow

Parameterize valid 3D Gaussians, project their covariance into the camera, and composite ordered contributions to render pixels.

### Parameterize scene primitives

A Gaussian centered at $\mu\in\mathbb R^3$ with covariance $\Sigma$ has unnormalized density

$$
G(x)=\exp\left[-\tfrac12(x-\mu)^\top\Sigma^{-1}(x-\mu)\right],
\qquad\Sigma=RSS^\top R^\top.
$$

$R$ is a rotation and $S$ contains nonnegative scale parameters. This factorization keeps covariance positive semidefinite; inverse operations require nondegenerate scales. Coordinates and covariance must share the scene’s frame and length units.




**Planned component problem:** Build Gaussian Covariances from Rotation and Scale. This is an unreviewed implementation idea for the mechanism above, not a runnable exercise; its precise contract and evaluator must be reviewed before publication.

### Project Gaussian footprints

Let $R_{cw}$ rotate world coordinates into camera coordinates and let $J$ be the2×3Jacobian of perspective projection at the Gaussian center. The projected covariance is

$$
\Sigma_{2D}=J R_{cw}\Sigma R_{cw}^\top J^\top.
$$

Its units are squared pixels. [SE(3) transformation](/problems/se3-transform-points) and [camera projection](/problems/project-camera-points) are useful prerequisites. Near-zero or negative camera depth cannot be treated as an ordinary visible splat.


**Prerequisite practice:** [Apply an SE(3) Transform to Batched Points](/problems/se3-transform-points) · [Project Camera Points into Pixels](/problems/project-camera-points). These supporting skills do not complete this model stage.

**Planned component problems:** Project anisotropic covariance into an image. These are planned work, not runnable links; titles without a reviewed blueprint remain unreviewed ideas.

### Composite visible contributions

For primitives sorted front to back at a pixel, a standard compositing expression is

$$
C=\sum_i c_i\alpha_i\prod_{j<i}(1-\alpha_j).
$$

Here $\alpha_i$ combines learned opacity with the projected Gaussian footprint, and $c_i$ can depend on viewing direction through appearance coefficients. The product is remaining transmittance. Sorting, early termination, and tile assignment affect rendering correctness and speed; a global unsorted sum is not equivalent.


**Planned component problems:** Composite depth-ordered Gaussian contributions; Measure primitive contribution for density control. These are planned work, not runnable links; titles without a reviewed blueprint remain unreviewed ideas.

## Implement the components

- **Related implementation skill:** [Apply an SE(3) Transform to Batched Points](/problems/se3-transform-points). This isolates a supporting mechanism, not this paper's complete method.
- **Related implementation skill:** [Project Camera Points into Pixels](/problems/project-camera-points). This isolates a supporting mechanism, not this paper's complete method.

**Planned components:**

- Build Gaussian Covariances from Rotation and Scale.
- Project anisotropic covariance into an image.
- Composite depth-ordered Gaussian contributions.
- Measure primitive contribution for density control.

[Browse the planned curriculum](https://github.com/alexermolovich/Joint_Tonic/blob/main/CURRICULUM.md). Planned titles require a reviewed contract and evaluator before becoming runnable.

## Why this matters on a robot

Fast photorealistic rendering is useful for reconstruction and simulation, but splat opacity is not automatically a collision surface. Unobserved regions, moving objects, and inaccurate camera poses can produce artifacts that look plausible from training views. Evaluate geometry and rendering separately.

## Sources and scope

[Primary paper](https://arxiv.org/abs/2308.04079) · [Open-access manuscript](https://arxiv.org/pdf/2308.04079)

This is an original explanation of selected mechanisms. Equations use the notation defined here; simplified teaching models are identified explicitly. Small component exercises do not reproduce the paper's full experiments. The local PDF is a research reference; its redistribution terms remain those recorded in the metadata.
