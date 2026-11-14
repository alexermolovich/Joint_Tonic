---
{
  "schema_version": 1,
  "problem_id": "vit-resolution-profile",
  "content_version": "1.0.0",
  "status": "published",
  "title": "Profile Token Count, Memory, and Latency by Resolution",
  "summary": "Calculate explicit attention-score storage and summarize measured latency for each image resolution.",
  "type": "component",
  "difficulty": "medium",
  "estimated_minutes": 40,
  "domains": [
    "perception"
  ],
  "topics": [
    "vision-transformer",
    "vit-resolution-profile"
  ],
  "paper_ids": [
    "2021-vision-transformer"
  ],
  "paper_sections": [
    "Vision Transformer encoder architecture and image-resolution scaling"
  ],
  "track_ids": [
    "paper-2021-vision-transformer"
  ],
  "prerequisite_problem_ids": [
    "vit-patchify-reconstruct"
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
  "entrypoint": "solution.profile_vit",
  "physical_contract": {
    "frames": [
      "Image grid and benchmark experiment identity"
    ],
    "units": {
      "values": "pixels, bytes and milliseconds"
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
    "evaluator_sha256": "ebc60ad303bb68d84966255882b97fdc6a4af89126a5681eed1231fe6cb3d780"
  },
  "fixtures": {
    "source": "original synthetic examples in examples.md; future generated fixtures use declared seed",
    "license": "CC0-1.0",
    "version_or_hash": "synthetic-v1-seed-20261113"
  },
  "provenance": {
    "authoring_notes": "Original bounded teaching component; no source code or figures copied. Systems diagnostics are teaching contracts, not paper benchmark claims.",
    "primary_urls": [
      "https://arxiv.org/abs/2010.11929"
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

# Profile Token Count, Memory, and Latency by Resolution

Implement `profile_vit(resolutions: np.ndarray, patch_size: int, heads: int, bytes_per_value: int, latency_ms: np.ndarray) -> dict`.

Calculate explicit attention-score storage and summarize measured latency for each image resolution.
resolutions int64(R,2) stores (height,width),0<=R<=128; dimensions1..8192 divisible by patch_size. patch_size is built-in int1..256; heads built-in int1..128; bytes_per_value built-in int exactly2,4 or8. latency_ms float64(R,K),1<=K<=4096, strictly positive measurements<=1e6 from equivalent model/device/workload. Tokens include one class token: L=(H/P)*(W/P)+1. Return dict tokens int64(R,), attention_bytes int64(R,) = heads*L*L*bytes_per_value, and p95_latency_ms float64(R,) using nearest-rank: sorted sample at index ceil(0.95*K)-1. Reject any attention-byte count exceeding int64 max. Estimate one explicit score tensor for one image and one layer only: this is NOT total training memory or a claim about fused attention kernels. Latency is supplied measurement, not predicted by token count.

## Validation and runtime

All array arguments must be NumPy arrays with the stated rank and dtype: real arrays use float64, index arrays int64, masks bool. Real entries must be finite with absolute value at most 1e6 unless a tighter range is stated. All malformed types, shapes, ranges, or scalar arguments raise ValueError. Support noncontiguous arrays, preserve every input, and return fresh arrays (no input storage alias). CPU only; no implicit batch dimension. Comparisons use rtol=1e-6 and atol=1e-7. Fixtures are original synthetic data (CC0-1.0).

## Worked examples

1. Resolution (4,4),patch2,heads2,float32(4 bytes): L=5, score storage=2*25*4=200 bytes. Measurements `[1,2,3,4]` ms have nearest-rank p95=4 ms.
2. Resolution (8,8) under the same settings gives L=17 and 2312 bytes. Quadrupling patch count from4 to16 grows this tensor by2312/200, not4.

## Source and scope

[Primary source](https://arxiv.org/abs/2010.11929). This isolates the stated component using synthetic fixtures; completing it does not reproduce the full paper.

## Implementation and verification plan

Compute integer token/storage counts and sort each supplied latency row. O(RK log K) time.
Reference Run and Submit must pass in bubblewrap, with starter and targeted wrong implementation rejected. Independent review precedes publication.
