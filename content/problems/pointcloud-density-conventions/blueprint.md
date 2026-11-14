---
{
  "schema_version": 1,
  "problem_id": "pointcloud-density-conventions",
  "content_version": "1.0.0",
  "status": "published",
  "title": "Validate Point-Cloud Density and Coordinate Conventions",
  "summary": "Report declared coordinate compatibility and spatial sampling density without guessing a frame from geometry.",
  "type": "component",
  "difficulty": "medium",
  "estimated_minutes": 40,
  "domains": [
    "perception"
  ],
  "topics": [
    "pointnet",
    "pointcloud-density-conventions"
  ],
  "paper_ids": [
    "2017-pointnet"
  ],
  "paper_sections": [
    "Network architecture: shared per-point mapping and symmetric aggregation; original input-data diagnostics"
  ],
  "track_ids": [
    "paper-2017-pointnet"
  ],
  "prerequisite_problem_ids": [],
  "runtime": {
    "language": "python",
    "python": "3.12.3",
    "image_digest": null,
    "image_status": "pending-image-build; local bubblewrap baseline",
    "platform": "linux-x86_64-cpu",
    "dependencies": {
      "numpy": "2.2.4"
    },
    "limits": {
      "wall_seconds": 18,
      "cpu_seconds": 10,
      "memory_mb": 4096,
      "output_kb": 64
    },
    "baseline_id": "python-3.12.3-numpy-2.2.4-torch-2.6.0-cpu-bwrap-v2",
    "budget_status": "actual shared worker caps; per-process address-space limit"
  },
  "entrypoint": "solution.audit_cloud",
  "physical_contract": {
    "frames": [
      "Caller-declared frame, never inferred"
    ],
    "units": {
      "values": "input m/cm/mm; output meters and points per voxel"
    },
    "axes": "Explicitly defined below; feature axes do not imply physical directions.",
    "timestamp_assumptions": "Inputs describe one synchronized observation unless the contract explicitly defines history. No clock estimation.",
    "batching": "Only dimensions explicitly named in the function contract are supported."
  },
  "grading": {
    "mode": "numerical",
    "seed": 20261114,
    "rtol": 1e-06,
    "atol": 1e-07,
    "public_case_families": [
      "Two worked examples",
      "Minimal supported input"
    ],
    "hidden_case_families": [
      "Independent mechanism checks",
      "Boundary and invalid inputs",
      "Input preservation"
    ],
    "performance_class": "none",
    "evaluator_sha256": "87d907d5a915e652f979e1a99a9783f3e228c87a18c7ccb2f6aa2425eb92a3bc"
  },
  "fixtures": {
    "source": "original synthetic examples in examples.md; future generated fixtures use declared seed",
    "license": "CC0-1.0",
    "version_or_hash": "synthetic-v1-seed-20261113"
  },
  "provenance": {
    "authoring_notes": "Original bounded teaching component; no source code or figures copied. Systems diagnostics are teaching contracts, not paper benchmark claims.",
    "primary_urls": [
      "https://arxiv.org/abs/1612.00593"
    ],
    "implementation_urls": []
  },
  "owners": [
    "perception_completion"
  ],
  "reviewers": [
    "research_curator"
  ]
}
---

# Validate Point-Cloud Density and Coordinate Conventions

Implement `audit_cloud(points: np.ndarray, unit: str, frame: str, expected_frame: str, voxel_size: float) -> dict`.

Report declared coordinate compatibility and spatial sampling density without guessing a frame from geometry.
`points` is float64 (N,3), 0<=N<=4096. `unit` is exactly "m", "cm", or "mm"; frame and expected_frame are nonempty ASCII identifiers of at most 32 characters using letters/digits/underscore. `voxel_size` is a built-in int/float (not bool), finite in [1e-4,1000], in meters. Convert to meters using the declared unit. Quantize each axis by floor(position_m/voxel_size), anchored at the declared frame origin, including negatives. Return exactly {"frame_matches":bool,"occupied_voxels":int,"points_per_voxel":float,"extent_m":float64(3,)}. Density is N/number_of_occupied_voxels (0 for empty); extent is coordinatewise max-minus-min (zeros for empty). Duplicate points count toward density. Unit conversion changes scale but does not rotate/translate or repair a frame mismatch. No target density threshold or physical surface area is inferred.

## Validation and runtime

All array arguments must be NumPy arrays with the stated rank and dtype: real arrays use float64, index arrays int64, masks bool. Real entries must be finite with absolute value at most 1e6 unless a tighter range is stated. All malformed types, shapes, ranges, or scalar arguments raise ValueError. Support noncontiguous arrays, preserve every input, and return fresh arrays (no input storage alias). CPU only; no implicit batch dimension. Comparisons use rtol=1e-6 and atol=1e-7. Fixtures are original synthetic data (CC0-1.0).

## Worked examples

1. Points `[[0,0,0],[50,0,0],[100,0,0]]`, unit="cm", matching frame="base", voxel_size=1 m occupy 2 voxels, density 1.5 points/voxel, extent `[1,0,0]` m.
2. Points `[[-0.01,0,0],[0,0,0]]` in meters with voxel_size=1 occupy 2 voxels because floor(-0.01)=-1. Frame "camera" versus expected "base" reports False without modifying the coordinates.

## Source and scope

[Primary source](https://arxiv.org/abs/1612.00593). This isolates the stated component using synthetic fixtures; completing it does not reproduce the full paper.

## Implementation and verification plan

Convert declared units, form integer voxel keys, count unique keys and compute extents. Sorting-based unique takes O(N log N) time and O(N) storage.
Reference Run and Submit must pass in bubblewrap, with starter and targeted wrong implementation rejected. Independent review precedes publication.
