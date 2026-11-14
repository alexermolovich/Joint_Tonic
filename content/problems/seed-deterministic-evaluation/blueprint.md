---
{
  "schema_version": 1,
  "problem_id": "seed-deterministic-evaluation",
  "content_version": "1.0.0",
  "status": "implemented",
  "title": "Seed a Deterministic Evaluation Run",
  "summary": "Seed a Deterministic Evaluation Run",
  "type": "function",
  "difficulty": "medium",
  "estimated_minutes": 35,
  "domains": [
    "robotics-foundations"
  ],
  "topics": [
    "robotics-foundations",
    "numerics-evaluation"
  ],
  "paper_ids": [],
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
  "entrypoint": "solution.seeded_episode_noise",
  "physical_contract": {
    "frames": [
      "Caller-aligned robot sensor/controller frames; no implicit transform"
    ],
    "units": {
      "noise/mean/std": "caller-declared sensor unit per channel",
      "seed/episode IDs": "unsigned32 identities",
      "horizon": "simulation step count"
    },
    "axes": "Output(E,H,D), episodes in requested ID order; per-episode draws(H,D)",
    "timestamp_assumptions": "Episodes and fixed sample ordering supplied; no wall clock or timing inference.",
    "batching": "Output(E,H,D), episodes in requested ID order; per-episode draws(H,D)"
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
    "evaluator_sha256": "ce9ba8527e48024f49ebcee1eec7accb03718bb4fa59b292cc7706e68aae74db",
    "performance_class": "none; no timing leaderboard"
  },
  "fixtures": {
    "source": "original synthetic fixtures",
    "license": "CC0-1.0",
    "version_or_hash": "original-synthetic-v1"
  },
  "provenance": {
    "authoring_notes": "Original robotics foundation with synthetic fixtures; no paper-derived implementation.",
    "primary_urls": [
      "https://numpy.org/doc/2.2/reference/random/bit_generators/pcg64.html",
      "https://numpy.org/doc/2.2/reference/random/parallel.html"
    ]
  },
  "owners": [
    "curriculum_continuation"
  ],
  "reviewers": [
    "root"
  ]
}
---

# Seed a Deterministic Evaluation Run

Implement seeded_episode_noise(episode_ids, root_seed, horizon, mean, std) -> np.ndarray.

episode_ids is NumPy int64(E,),0<=E<=256, unique IDs0..2**32-1. root_seed built-in non-bool int0..2**32-1; horizon built-in non-bool int0..256. mean/std NumPy float64(D,),1<=D<=32, mean finite abs<=1000,std finite0..1000. Total E*horizon*D<=1000000. For each episode ID i independently construct np.random.Generator(np.random.PCG64(np.random.SeedSequence([root_seed,int(i)]))). Draw exactly standard_normal((horizon,D)) then multiply by std and add mean. Return fresh float64(E,horizon,D) in supplied ID order, preserving inputs and legacy global np.random state. Noncontiguous inputs valid; zero episodes/horizon returns correct shape while validating all settings. Invalid contracts raise ValueError.

Each feature channel uses one caller-declared sensor unit shared by mean/std and output; channels may differ in units. Noise samples are independent synthetic perturbations at fixed caller-defined simulation timesteps. Pin NumPy2.2.4 for this normal-draw replay contract; no claim across arbitrary library versions. Reordering or splitting episode IDs must preserve each episode's generated values. No simulator state is seeded here.
