---
{
  "schema_version": 1,
  "problem_id": "broadcast-batched-sensor-features",
  "content_version": "0.1.0",
  "status": "reviewed",
  "title": "Broadcast Batched Sensor Features",
  "summary": "Broadcast Batched Sensor Features",
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
  "entrypoint": "solution.broadcast_sensor_features",
  "physical_contract": {
    "frames": [
      "Caller-aligned robot sensor/controller frames; no implicit transform"
    ],
    "units": {
      "features/context": "dimensionless normalized features"
    },
    "axes": "sensor(B,T,F),context(B,C),present(B,T),output(B,T,F+C)",
    "timestamp_assumptions": "Episodes and fixed sample ordering supplied; no wall clock or timing inference.",
    "batching": "sensor(B,T,F),context(B,C),present(B,T),output(B,T,F+C)"
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
    "evaluator_sha256": "8d2ec76192e8a7d09dbda89dbec62103de1cbb18c312cab161e4204b0b1a5779",
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
      "https://numpy.org/doc/2.2/reference/"
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

# Broadcast Batched Sensor Features

Implement broadcast_sensor_features(sensor, context, present) -> np.ndarray.

sensor is NumPy float64(B,T,F), context float64(B,C), present bool(B,T). Bounds:1<=B<=32,0<=T<=256,1<=F,C<=64, B*T*(F+C)<=1000000. All sensor/context values finite and absolute value<=1e6, including absent timesteps. For each valid timestep concatenate sensor[b,t,:] followed by context[b,:]; absent timesteps return all zeros, including the context part. Return fresh float64(B,T,F+C). Preserve all inputs; noncontiguous arrays are valid. Invalid types/dtypes/shapes/values raise ValueError.

Each batch row represents one robot episode, T ordered synchronized sensor samples. Features are dimensionless pre-normalized channels; context is fixed episode metadata already encoded into C numerical features. This does not convert units, infer timestamps, transform frames, or infer presence from feature values.
