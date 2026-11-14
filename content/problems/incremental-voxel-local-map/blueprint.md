---
{
  "schema_version": 1,
  "problem_id": "incremental-voxel-local-map",
  "content_version": "1.0.0",
  "status": "published",
  "title": "Update an Incremental Local Map",
  "summary": "`update_local_map(existing, scan, world_from_lidar, center, half_extent, voxel_size)` existing(M,3)worldpoints,scan(N,3)lidarpoints,M/N0..16384, abs<=1e4; transformproper withtranslationabs<=1e4;center(3)worldmetersabs<=1e4;half_extent(3)meters[1e-3,1e4],voxelscalar[1e-3,1000]meters. Transformscanintoworld; merge candidates in existing-then-scan index order. Keep points in inclusive axis-aligned center\u00b1extent. Voxel key=floor(worldpoint/size),globaloriginfixedzero,negativecoordsfloor. Within each occupied voxel retain candidate closest in squaredmeters to voxelcenter (key+.5)*size, tie lower mergedcandidateindex. Return points(V,3),voxel_keys(V,3)int64,source_indices(V)int64(sortedlexicographicvoxelkeys),removed_existing(M)bool true iff existing point notretained (outsideorlosesvoxel). Candidateidentity from concatenation. Deterministic batch teaching equivalent of pruning/downsampling decisions; no incremental ikd-tree, runtimeclaim or scan deskew. Exampleexisting[[.1,0,0],[.4,0,0]],scan[[.6,0,0]],I,center0,extent2,voxel1=>selectexistingindex1 (equal .4/.6 center distances tie earlier),key[0,0,0],removed[True,False]. Exampleexisting[[-.1,0,0]],scanzero,I,size1=>keys[-1,0,0],[0,0,0] distinct. Implementation should handle up to32768candidates without quadraticpairwisearrays.",
  "type": "component",
  "difficulty": "medium",
  "estimated_minutes": 40,
  "domains": [
    "geometry-state-estimation"
  ],
  "topics": [
    "geometry-calibration-slam",
    "fast-lio-2"
  ],
  "paper_ids": [
    "2021-fast-lio-2"
  ],
  "paper_sections": [
    "Mechanism described in the linked paper card and theory"
  ],
  "track_ids": [
    "paper-2021-fast-lio-2"
  ],
  "prerequisite_problem_ids": [
    "se3-transform-points"
  ],
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
  "entrypoint": "solution.update_local_map",
  "physical_contract": {
    "frames": [
      "Explicit world, body, camera or dimensionless scaled-state frame in the contract"
    ],
    "units": {
      "values": "Meters, seconds, radians, pixels, or dimensionless normalized quantities as defined per argument"
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
    "evaluator_sha256": "7dfc1c702b08c5624ccecfa5a4483c6ef6e18d15584afb94f4edebf09e44dc7f"
  },
  "fixtures": {
    "source": "original synthetic examples in examples.md; future generated fixtures use declared seed",
    "license": "CC0-1.0",
    "version_or_hash": "synthetic-v1-seed-20261113"
  },
  "provenance": {
    "authoring_notes": "Original bounded teaching component; no source code or figures copied. Systems diagnostics are teaching contracts, not paper benchmark claims.",
    "primary_urls": [
      "https://arxiv.org/abs/2107.06829"
    ],
    "implementation_urls": []
  },
  "owners": [
    "perception_completion"
  ],
  "reviewers": [
    "root",
    "research_curator"
  ]
}
---

# Update an Incremental Local Map

Implement `update_local_map(existing, scan, world_from_lidar, center, half_extent, voxel_size)`.

`update_local_map(existing, scan, world_from_lidar, center, half_extent, voxel_size)` existing(M,3)world points,scan(N,3)lidar points,M/N0..16384, abs<=1e4; transformproper withtranslation abs<=1e4;center(3)world meters abs<=1e4;half_extent(3)meters[1e-3,1e4],voxelscalar [1e-3,1000]meters.

Transform scan into world coordinates; merge candidates in existing-then-scan index order.

Keep points in inclusive axis-aligned center±extent.

Voxel key=floor(worldpoint/size),global origin fixed zero,negative coordinates use floor.

Within each occupied voxel retain candidate closest in squared meters to voxel center (key+.5)*size, tie lower merged candidate index.

Return points(V,3),voxel_keys(V,3)int64,source_indices(V)int64(sorted lexicographic voxel keys),removed_existing(M)bool true iff existing point not retained (outside or loses voxel selection).

Candidate identity from concatenation.

Deterministic batch teaching equivalent of pruning/downsampling decisions; no incremental ikd-tree, runtimeclaim or scan deskew.

Example: existing[[.1,0,0],[.4,0,0]],scan[[.6,0,0]],I,center0,extent2,voxel1=>selectexistingindex1 (equal .4/.6 center distances tie earlier),key[0,0,0],removed[True,False].

Example: existing[[-.1,0,0]],scan zero,I,size1=>keys[-1,0,0],[0,0,0] distinct.

Implementation should handle up to 32768 candidates without quadratic pairwise arrays.

## Validation and runtime

All array arguments must be NumPy arrays with the stated rank and dtype: real arrays use float64, index arrays int64, masks bool.

Real entries must be finite with absolute value at most 1e6 unless a tighter range is stated.

All malformed types, shapes, ranges, or scalar arguments raise ValueError.

Support noncontiguous arrays, preserve every input, and return fresh arrays (no input storage alias).

CPU only; no implicit batch dimension.

Comparisons use rtol=1e-6 and atol=1e-7.

Fixtures are original synthetic data (CC0-1.0).

## Worked examples

1. Existing points [[0.1,0,0],[0.4,0,0]], incoming [[0.6,0,0]], identity pose, center [0,0,0], half extents [2,2,2] and voxel size 1 select existing index 1.

Points 0.4 and 0.6 tie around center 0.5, so the earlier candidate wins.

Removed-existing flags are [True,False].
2. Existing [-0.1,0,0] and incoming [0,0,0] belong to voxel keys [-1,0,0] and [0,0,0].

Negative coordinates use floor, not truncation toward zero.

## Source and scope

[Primary source](https://arxiv.org/abs/2107.06829).

This isolates the stated component using synthetic fixtures; completing it does not reproduce the full paper.

## Implementation and verification plan

Use a dictionary keyed by voxel coordinate, updating a winner only for a strictly smaller center distance.

Sort the occupied keys at the end. O((M+N)+V log V) expected time, O(M+N) storage; no pairwise point-distance matrix.
Reference Run and Submit must pass in bubblewrap, with starter and targeted wrong implementation rejected.

Independent review precedes publication.
