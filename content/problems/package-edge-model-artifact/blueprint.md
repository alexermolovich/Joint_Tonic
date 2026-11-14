---
{
  "schema_version": 1,
  "problem_id": "package-edge-model-artifact",
  "content_version": "1.0.0",
  "status": "implemented",
  "title": "Package and Verify an Edge Model Artifact",
  "summary": "Package and Verify an Edge Model Artifact",
  "type": "function",
  "difficulty": "medium",
  "estimated_minutes": 35,
  "domains": [
    "robotics-mlops"
  ],
  "topics": [
    "robotics-mlops",
    "2020-once-for-all"
  ],
  "paper_ids": [
    "2020-once-for-all"
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
  "entrypoint": "solution.package_edge_model",
  "physical_contract": {
    "frames": [
      "No spatial transform; preserve caller-supplied scenario/model identities"
    ],
    "units": {
      "size_bytes": "bytes",
      "input_shape": "dimensionless element extents",
      "digests": "lowercase SHA-256 hex"
    },
    "axes": "Input shape tuple has 1\u20134 caller-defined model axes; metadata preserves that tuple",
    "timestamp_assumptions": "No live timestamps; latency metrics are supplied durations only.",
    "batching": "Input shape tuple has 1\u20134 caller-defined model axes; metadata preserves that tuple"
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
    "evaluator_sha256": "c9cda1685d6cfcfbe0af745409aced5273efaa3c156f6e0ed4f12f6784a866f2",
    "performance_class": "none; no timing leaderboard"
  },
  "fixtures": {
    "source": "original synthetic fixtures",
    "license": "CC0-1.0",
    "version_or_hash": "original-synthetic-v1"
  },
  "provenance": {
    "authoring_notes": "This original bounded component is motivated by [2020-once-for-all](https://arxiv.org/abs/1908.09791). It does not reproduce the full paper, trained model or benchmark protocol.",
    "primary_urls": [
      "https://arxiv.org/abs/1908.09791"
    ],
    "paper_card": "research/papers/mlops-sim2real/2020-once-for-all.md",
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

# Package and Verify an Edge Model Artifact

Implement package_edge_model(model_bytes, metadata, expected_sha256) -> dict.

model_bytes is built-in bytes of1–1048576 bytes. expected_sha256 is64 lowercase hexadecimal characters and must equal SHA-256(model_bytes). metadata is exactly a dict with format in{"onnx","tflite"}, runtime a string ASCII[a-z][a-z0-9_.-]{0,63}, input_shape a tuple of1–4 positive built-in non-bool ints<=4096 with product<=1000000, input_dtype in{"float32","uint8"}, and calibration_sha256 a64-character lowercase hexadecimal string. These descriptors identify a supplied model interface; no actual model parsing occurs.

Return a fresh dict containing model_sha256, size_bytes, metadata (independent deep copy preserving its tuple shape), and manifest_sha256. The manifest hash is SHA-256 of UTF-8 json.dumps({"model_sha256":actual,"size_bytes":len(model_bytes),"metadata":metadata},sort_keys=True,separators=(",",":"),ensure_ascii=True). JSON converts input_shape's tuple to a JSON array. The manifest itself does not include manifest_sha256 in its hash. Preserve inputs. Invalid types/schema/bounds or mismatching expected digest raise ValueError.

This packages in-memory identity evidence, not a signed release, ONNX validator, file writer, or proof of execution safety. Calibration bytes are not supplied and their digest is only recorded, not independently verified. Model weights/input data remain dimensionless or quantized values under the declared external calibration contract.
