---
{
  "schema_version": 1,
  "problem_id": "stable-masked-softmax",
  "content_version": "1.0.0",
  "status": "implemented",
  "title": "Stable Softmax for Masked Sequences",
  "summary": "Stable Softmax for Masked Sequences",
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
  "entrypoint": "solution.stable_masked_softmax",
  "physical_contract": {
    "frames": [
      "Caller-aligned robot sensor/controller frames; no implicit transform"
    ],
    "units": {
      "logits": "dimensionless relative evidence",
      "output": "dimensionless token probability or all-zero unavailable row"
    },
    "axes": "Each row is one context; columns caller-ordered sensor/action tokens(B,L)",
    "timestamp_assumptions": "Episodes and fixed sample ordering supplied; no wall clock or timing inference.",
    "batching": "Each row is one context; columns caller-ordered sensor/action tokens(B,L)"
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
    "evaluator_sha256": "7881d458275ad4de3459b34b8f3d917b6f0d70809fd2393fed6a2d126b32e6f5",
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

# Stable Softmax for Masked Sequences

Implement stable_masked_softmax(logits, valid) -> np.ndarray.

logits is NumPy float64(B,L), valid bool(B,L),1<=B<=256,0<=L<=2048,total<=200000. Every logit, including masked positions, is finite with magnitude<=10000. Return fresh float64(B,L). For each row with any valid entry, compute softmax over valid positions only using max subtraction; masked entries are exactly0. A row with no valid entries returns all zeros, without NaN; L=0 returns shape(B,0). Preserve inputs; noncontiguous arrays valid. Invalid contracts raise ValueError.

Logits are dimensionless relative evidence scores for a caller-ordered sensor/action token sequence. Mask presence is explicit; this function does not create a causal mask or enforce actuator constraints. Exact normalization is subject to standard float64 rounding.
