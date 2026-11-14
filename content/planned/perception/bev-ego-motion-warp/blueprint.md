---
{
  "schema_version": 1,
  "problem_id": "bev-ego-motion-warp",
  "content_version": "0.1.0",
  "status": "reviewed",
  "title": "Warp a Previous BEV with Ego Motion",
  "summary": "Warp a Previous BEV with Ego Motion",
  "type": "function",
  "difficulty": "hard",
  "estimated_minutes": 40,
  "domains": [
    "perception"
  ],
  "topics": [
    "bevformer",
    "paper-component"
  ],
  "paper_ids": [
    "2022-bevformer"
  ],
  "paper_sections": [
    "Mechanism and explicit teaching conventions in theory.md"
  ],
  "track_ids": [],
  "prerequisite_problem_ids": [
    "se3-transform-points"
  ],
  "runtime": {
    "language": "python",
    "python": "3.12.3",
    "runtime_id": "python-3.12.3-numpy-2.2.4-torch-2.6.0-cpu-bwrap-v2",
    "image_digest": null,
    "image_status": "pending OCI build; baseline worker exists",
    "dependencies": {
      "numpy": "2.2.4"
    },
    "limits": {
      "wall_seconds": 18,
      "cpu_seconds": 10,
      "memory_mb": 4096,
      "output_kb": 64
    }
  },
  "entrypoint": "solution.warp_previous_bev",
  "physical_contract": {
    "frames": [
      "Explicit caller grid/view frames in statement"
    ],
    "units": {
      "features": "dimensionless; BEV geometry in metres where stated"
    },
    "axes": "previous(H,W,C), previous_from_current(3,3), origin(2,); output(H,W,C).",
    "timestamp_assumptions": "One explicitly paired batch; no internal clock.",
    "batching": "previous(H,W,C), previous_from_current(3,3), origin(2,); output(H,W,C)."
  },
  "grading": {
    "mode": "numerical",
    "seed": 20261113,
    "rtol": 0.000001,
    "atol": 1e-7,
    "public_case_families": [
      "worked-examples",
      "minimal-shape"
    ],
    "hidden_case_families": [
      "validation",
      "edge-policy",
      "layout",
      "preservation",
      "independent-oracle",
      "scale"
    ],
    "performance_class": "cpu"
  },
  "fixtures": {
    "source": "original-synthetic",
    "license": "CC0-1.0",
    "version_or_hash": "synthetic-v1-seed-20261113"
  },
  "provenance": {
    "authoring_notes": "Original bounded teaching task; variants explicitly distinguished from full paper systems.",
    "primary_urls": [
      "https://arxiv.org/abs/2203.17270"
    ],
    "implementation_urls": [],
    "paper_card": "research/papers/vision-vlm-3d/2022-bevformer.md",
    "manifest": "research/manifests/vision-vlm-3d.md"
  },
  "owners": [
    "perception_implementation"
  ],
  "reviewers": ["vla_implementation"]
}
---

# Warp a Previous BEV with Ego Motion

## Contract

Implement warp_previous_bev(previous, previous_from_current, resolution, origin).

previous is a finite NumPy float64 array (H,W,C), with 1<=H,W<=256, 1<=C<=64, at most 1,000,000 entries and absolute values <=1e6. Features are dimensionless. Arrays may be noncontiguous. previous_from_current is finite float64 (3,3), absolute entries <=1e6, with bottom row [0,0,1] within atol=1e-7, rtol=0; its top-left rotation R satisfies R.T@R=I and det(R)=1 with the same tolerance. Treat its top two rows as supplied; do not project a near-valid rotation onto SO(2).

resolution is a finite built-in non-bool int/float in [1e-3,1e3], in metres per cell. origin is finite float64 (2,) with absolute values <=1e6, in metres. The current and previous grids use this same numerical origin and resolution in their respective local frames. Column increases +x, row increases +y; x,y,z form a right-handed frame. No image-down or vehicle-forward meaning is inferred.

For output row r and column c, its current-frame cell center is x=origin[0]+(c+0.5)*resolution, y=origin[1]+(r+0.5)*resolution. Apply previous_from_current to [x,y,1] to get the point in the PREVIOUS frame; no projective divide is used. Convert its previous coordinates to fractional array indices u=(x_previous-origin[0])/resolution-0.5, v=(y_previous-origin[1])/resolution-0.5.

Bilinearly sample the previous feature grid at (u,v), treating each out-of-bounds integer neighbor as an all-zero feature vector. Do not clamp coordinates, wrap indices, renormalize surviving weights, or simply reject a sample whose center lies outside the grid. A sample halfway beyond the final cell can retain half that cell's value. Return a new float64 array (H,W,C), preserving all inputs.

Non-array previous, previous_from_current or origin raises TypeError; all other violations raise ValueError. No empty spatial/channel axes, output-grid-size option, GPU, gradients, temporal attention, moving-object compensation or simulator is included. The transform is an already supplied pairing of adjacent ego frames; there is no internal clock or transform estimation. This is an explicit planar alignment exercise motivated by BEVFormer, not its complete temporal-attention implementation.

## Implementation and proof

Independent contract review precedes implementation. Test the examples, typed validation, boundary policies, input preservation and realistic scale with independent oracles. Publish only after isolated Run/Submit and starter-negative checks. Review risk: Independently test transform direction, nonzero origin, cell-center convention, rotation and fractional translations, partial zero padding, negative index wraparound, and nonmutation.

## Resources and provenance

https://arxiv.org/abs/2203.17270. Actual shared local worker caps: 18 s wall, 10 s CPU, 4096 MiB address space, 64 KiB output. OCI image digest is pending; no image or reproducibility claim is invented. Original examples and future fixtures use CC0-1.0.

