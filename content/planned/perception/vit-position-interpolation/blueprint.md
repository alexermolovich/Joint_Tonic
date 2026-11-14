---
{
  "schema_version": 1,
  "problem_id": "vit-position-interpolation",
  "content_version": "0.1.0",
  "status": "reviewed",
  "title": "Interpolate 2D Positional Embeddings",
  "summary": "Interpolate 2D Positional Embeddings",
  "type": "function",
  "difficulty": "medium",
  "estimated_minutes": 35,
  "domains": [
    "perception"
  ],
  "topics": [
    "vision-transformer",
    "paper-component"
  ],
  "paper_ids": [
    "2021-vision-transformer"
  ],
  "paper_sections": [
    "Mechanism and conventions defined in theory.md"
  ],
  "track_ids": [],
  "prerequisite_problem_ids": [
    "vit-patch-class-tokens"
  ],
  "runtime": {
    "language": "python",
    "python": "3.12.3",
    "image_digest": null,
    "image_status": "pending-image-build",
    "dependencies": {
      "torch": "2.6.0+cpu"
    },
    "limits": {
      "wall_seconds": 18,
      "cpu_seconds": 10,
      "memory_mb": 4096,
      "output_kb": 64
    }
  },
  "entrypoint": "solution.resize_positions",
  "physical_contract": {
    "frames": [
      "Explicit caller-observation conventions in statement"
    ],
    "units": {
      "features": "dimensionless"
    },
    "axes": "positions(1,1+H0*W0,D), old_grid(H0,W0),new_grid(H1,W1); result(1,1+H1*W1,D).",
    "timestamp_assumptions": "One observation batch; no internal clock.",
    "batching": "positions(1,1+H0*W0,D), old_grid(H0,W0),new_grid(H1,W1); result(1,1+H1*W1,D)."
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
    "authoring_notes": "Original bounded teaching task. No copied source code or figure.",
    "primary_urls": [
      "https://arxiv.org/abs/2010.11929"
    ],
    "implementation_urls": []
  },
  "owners": [
    "perception_implementation"
  ],
  "reviewers": ["vla_implementation"]
}
---

# Interpolate 2D Positional Embeddings

## Contract

Implement resize_positions(positions, old_grid, new_grid). positions is a finite CPU torch float32/float64 tensor, abs values<=100, shape(1,1+H0*W0,D),1<=D<=256. Each grid is a length2 tuple of built-in ints excluding bool; each dimension1..128. Input and output each have at most1,000,000 elements. Row0 is a class-token position and must remain exactly unchanged. Remaining rows are a row-major H0xW0 grid; reshape to channels-first, interpolate with torch.nn.functional.interpolate(size=new_grid,mode='bicubic',align_corners=False,antialias=False), then restore row-major sequence order and prepend row0. Return new independent storage preserving dtype/device and gradients. Noncontiguous input supported; input unchanged. TypeError for non-tensor; ValueError for other violations. No square-grid inference or image interpolation. Embeddings are dimensionless learned position coordinates, not metric robot poses. The interpolation convention is explicit; some model libraries use align_corners=True, which is outside this contract.

## Implementation and proof

Independent review precedes implementation. Test both examples and documented invalid/empty/layout cases; use independent objective/shape/value oracles. Verify actual isolated public Run and hidden Submit plus starter negative control. Reference and fixture code are original. Theory includes original math and static numerical/layout table with text alternative. No full-paper reproduction is claimed.
