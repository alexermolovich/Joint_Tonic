---
{
  "schema_version": 1,
  "problem_id": "extract-elastic-subnetwork",
  "content_version": "1.0.0",
  "status": "implemented",
  "title": "Extract a Depth, Width, and Kernel Subnetwork",
  "summary": "Extract a Depth, Width, and Kernel Subnetwork",
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
  "entrypoint": "solution.extract_subnetwork",
  "physical_contract": {
    "frames": [
      "No spatial transform; named records retain their supplied identity"
    ],
    "units": {
      "weights": "dimensionless float64 coefficients",
      "depth": "layer count",
      "width": "channel count",
      "kernel": "spatial sample count"
    },
    "axes": "Each layer (C_out,C_in,K_y,K_x) with equal C and square odd K.",
    "timestamp_assumptions": "No wall-clock timestamps; deterministic logical inputs only.",
    "batching": "Each layer (C_out,C_in,K_y,K_x) with equal C and square odd K."
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
    "evaluator_sha256": "9eac26e032c972aa77d4b0df284a0220a20587cf38d2324dc518d2dab30aec18",
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

# Extract a Depth, Width, and Kernel Subnetwork

Implement extract_subnetwork(weights, depth, width, kernel) -> list[np.ndarray].

weights is a list of1–16 NumPy float64 arrays, all finite and same shape(C,C,K,K), 1<=C<=64, odd1<=K<=9, absolute values<=100, total input entries<=1000000. These are consecutive SAME-width convolution blocks after a caller-provided compatible stem. depth,width,kernel are built-in non-bool ints, 1<=depth<=len(weights),1<=width<=C, and positive odd kernel<=K. Noncontiguous arrays are valid.

Return fresh independent arrays for the first depth blocks: select the FIRST width output and input channels, and the centered spatial kernel crop. Each output has shape(width,width,kernel,kernel). Preserve inputs and do not alias between output layers, even if input arrays alias. Validate every input layer, including layers beyond depth. Invalid types, dimensions, values or budgets raise ValueError.

Kernel center cropping is an ORIGINAL teaching simplification, not Once-for-All's learned kernel transformations. There are no activations, BN statistics, shortcuts, width sorting, training or inference. The caller must provide a stem and head matching the selected width; this is a block-parameter extraction task, not a complete executable model.
