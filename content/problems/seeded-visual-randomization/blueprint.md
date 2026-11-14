---
{
  "schema_version": 1,
  "problem_id": "seeded-visual-randomization",
  "content_version": "1.0.0",
  "status": "implemented",
  "title": "Build a Seeded Visual Randomization Sampler",
  "summary": "Build a Seeded Visual Randomization Sampler",
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
  "entrypoint": "solution.sample_visual_scenarios",
  "physical_contract": {
    "frames": [
      "Camera yaw uses caller world +z; no transform or motion is executed"
    ],
    "units": {
      "brightness": "dimensionless exposure multiplier",
      "yaw": "radians about world +z",
      "distractors": "object count",
      "seed": "unsigned 32-bit integer"
    },
    "axes": "Each output vector has N scenarios; random columns texture,brightness,yaw,distractors",
    "timestamp_assumptions": "No live timestamps; latency metrics are supplied durations only.",
    "batching": "Each output vector has N scenarios; random columns texture,brightness,yaw,distractors"
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
    "evaluator_sha256": "9a886a58f2f00d5fff6d6ea4b825713e492fde666f5e6b674bc6ca43a38edc20",
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

# Build a Seeded Visual Randomization Sampler

Implement sample_visual_scenarios(count, seed, textures, brightness, yaw, distractors) -> dict.

count and seed are built-in non-bool ints in[0,10000] and[0,2**32-1]. textures is a Python list of1–64 unique ASCII IDs[a-z][a-z0-9_-]{0,63}, whose order is meaningful. brightness and yaw are tuples(lo,hi) of finite built-in non-bool numbers, lo<=hi: brightness in[0,10] is a dimensionless exposure multiplier, yaw in[-pi,pi] is camera yaw radians about caller's world+z axis with no angle wrapping. distractors is a tuple of built-in ints0<=lo<=hi<=100, a count not a physical density.

Use an independent np.random.Generator(np.random.PCG64(seed)); draw exactly U=rng.random((count,4)). In column order select texture index floor(u0*len(textures)), brightness=lo+u1*(hi-lo), yaw=lo+u2*(hi-lo), distractor count=lo+floor(u3*(hi-lo+1)). Return dict texture:list[str], brightness:float64(count,), yaw:float64(count,), distractors:int64(count,), all independent storage. No global RNG use, input mutation, rendering, robot movement, or label change. count0 returns correctly typed empty outputs but validates all settings. Invalid contracts raise ValueError.
