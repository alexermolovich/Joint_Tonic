---
{
  "schema_version": 1,
  "problem_id": "stratify-visual-factors",
  "content_version": "1.0.0",
  "status": "implemented",
  "title": "Stratify Texture, Lighting, Camera, and Distractor Factors",
  "summary": "Stratify Texture, Lighting, Camera, and Distractor Factors",
  "type": "function",
  "difficulty": "medium",
  "estimated_minutes": 35,
  "domains": [
    "robotics-mlops"
  ],
  "topics": [
    "robotics-mlops",
    "2017-domain-randomization"
  ],
  "paper_ids": [
    "2017-domain-randomization"
  ],
  "paper_sections": [
    "Mechanism described in theory; bounded teaching contract"
  ],
  "track_ids": [],
  "prerequisite_problem_ids": [],
  "runtime": {
    "language": "python",
    "python": "3.12.3",
    "runtime_id": "python-3.12.3-numpy-2.2.4-torch-2.6.0-cpu-bwrap-v2",
    "image_digest": null,
    "image_status": "pending OCI build; local bubblewrap baseline",
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
  "entrypoint": "solution.stratify_visual_factors",
  "physical_contract": {
    "frames": [
      "No spatial transform; preserve caller-supplied scenario/model identities"
    ],
    "units": {
      "coordinates": "dimensionless values in [0,1)",
      "jitter": "dimensionless within-stratum offset"
    },
    "axes": "float64(N,4), columns normalized texture,lighting,camera,distractors",
    "timestamp_assumptions": "No live timestamps; latency metrics are supplied durations only.",
    "batching": "float64(N,4), columns normalized texture,lighting,camera,distractors"
  },
  "grading": {
    "mode": "numerical",
    "seed": 20261114,
    "rtol": 1e-09,
    "atol": 1e-10,
    "public_case_families": [
      "two-worked-examples"
    ],
    "hidden_case_families": [
      "independent-oracle",
      "edge-shapes",
      "invalid-contract",
      "preservation",
      "scale"
    ],
    "evaluator_sha256": "3e2df46980603d61f14e1ad5190c79c7cbc1cb711c031cef0e8ae433ffb17f9c",
    "performance_class": "none; no timing leaderboard"
  },
  "fixtures": {
    "source": "original synthetic fixtures",
    "license": "CC0-1.0",
    "version_or_hash": "original-synthetic-v1"
  },
  "provenance": {
    "authoring_notes": "This original bounded component is motivated by [2017-domain-randomization](https://arxiv.org/abs/1703.06907). It does not reproduce the full paper, trained model or benchmark protocol.",
    "primary_urls": [
      "https://arxiv.org/abs/1703.06907"
    ],
    "paper_card": "research/papers/mlops-sim2real/2017-domain-randomization.md",
    "manifest": "research/manifests/mlops-sim2real.md"
  },
  "owners": [
    "curriculum_continuation"
  ],
  "reviewers": [
    "root"
  ]
}
---

# Stratify Texture, Lighting, Camera, and Distractor Factors

Implement stratify_visual_factors(permutations, jitter) -> np.ndarray.

permutations is a NumPy int64(N,4) array,1<=N<=10000. Every column must independently be a permutation of0..N-1. jitter is a matching NumPy float64 array, finite in[0,1). Noncontiguous arrays are valid. Return new float64(N,4) values(permutations+jitter)/N. Column meanings are normalized texture-choice coordinate, lighting coordinate, camera coordinate, and distractor-choice coordinate.  Floating-point boundary policy: clamp the computed value to at least lower=permutations/N and at most np.nextafter(upper,lower), where upper=(permutations+1)/N, so rounding cannot cross a half-open stratum boundary. Each factor occupies every one of N half-open strata exactly once; rows define joint scenarios. Preserve inputs and avoid storage aliasing. All invalid types/dtypes/shapes/permutations/values raise ValueError.

The caller supplies permutations and jitter; no RNG occurs. These are dimensionless design coordinates, not actual texture IDs, light intensities or camera poses. Categorical mapping and physical bounds belong downstream. This Latin-hypercube-style marginal design does not promise coverage of all N^4 joint cells or reproduce a paper's exact sampler.
