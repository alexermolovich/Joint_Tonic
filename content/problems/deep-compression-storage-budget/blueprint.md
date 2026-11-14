---
{
  "schema_version": 1,
  "problem_id": "deep-compression-storage-budget",
  "content_version": "1.0.0",
  "status": "implemented",
  "title": "Compute a Compressed Model Storage Budget",
  "summary": "Compute a Compressed Model Storage Budget",
  "type": "function",
  "difficulty": "medium",
  "estimated_minutes": 35,
  "domains": [
    "robotics-mlops"
  ],
  "topics": [
    "robotics-mlops",
    "model-compression",
    "2015-deep-compression"
  ],
  "paper_ids": [
    "2015-deep-compression"
  ],
  "paper_sections": [
    "Selected bounded mechanism explained in theory"
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
  "entrypoint": "solution.compressed_storage_budget",
  "physical_contract": {
    "frames": [
      "Neural feature channels; no spatial frame transform"
    ],
    "units": {
      "counts/lengths/budgets": "counts, bits, bytes; compression ratio dimensionless"
    },
    "axes": "frequencies/code_lengths(K,); all budgets aggregate one model.",
    "timestamp_assumptions": "Offline fixed calibration batch; no timestamps",
    "batching": "frequencies/code_lengths(K,); all budgets aggregate one model."
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
    "performance_class": "none; no timing leaderboard",
    "evaluator_sha256": "44144e2a86ae44f1473735ffd7e0307d1e57e7d22be599d871f814b95a4eb6d9"
  },
  "fixtures": {
    "source": "original synthetic fixtures",
    "license": "CC0-1.0",
    "version_or_hash": "original-synthetic-v1"
  },
  "provenance": {
    "authoring_notes": "Original bounded component; no full paper reproduction or hardware speed guarantee. Backlog PB-111",
    "primary_urls": [
      "https://arxiv.org/abs/1510.00149"
    ],
    "paper_card": "research/papers/mlops-data-deployment/2015-deep-compression.md",
    "manifest": "research/manifests/expansion-150.md"
  },
  "owners": [
    "curriculum_continuation"
  ],
  "reviewers": [
    "root",
    "perception_completion"
  ]
}
---

# Compute a Compressed Model Storage Budget

## Goal and contract

Implement `compressed_storage_budget(dense_count, frequencies, code_lengths, index_bits, centroid_bits, header_bytes) -> dict`. dense_count int1..10^12; frequencies int64(K,) counts0..10^12 with sum<=dense_count; code_lengths int64(K,) in1..32;1<=K<=256; index_bits int1..64; centroid_bits int16 or32; header_bytes int0..10^6. Validate prefix-code feasibility sum(2**(-length))<=1 exactly (multiply by2**32 and use Python integers). The caller supplies code lengths; do not construct Huffman codes. For n=sum(frequencies), symbol_bits=sum(freq*length); symbol_bytes=ceil(symbol_bits/8), index_bytes=ceil(n*index_bits/8), codebook_bytes=K*centroid_bits/8. Round the symbol and index streams separately. Return Python ints symbol_bits,symbol_bytes,index_bytes,codebook_bytes,total_bytes and dense_bytes=4*dense_count, plus float compression_ratio=dense_bytes/total_bytes. total includes header_bytes. Models use dense float32 baseline; no tensor allocator, alignment beyond bytes, or speed estimate. Work O(K).

## Shared numerical and physical contract

All numeric arrays must be NumPy arrays with float32 or float64 dtype, finite values with absolute value at most 10^6, and at most 1,000,000 entries, unless a different dtype or bound is stated. Compute float results in float64 on CPU, return new arrays, and preserve every input. Noncontiguous arrays are valid. Invalid inputs raise ValueError, including wrong dtype, rank, shape or nonfinite values. Scalar integers are built-in int, excluding bool. Scalars described as real accept built-in int/float excluding bool and must be finite. No gradients or in-place mutation are required. Values are dimensionless calibrated neural-layer features and weights; columns retain the caller's channel order. No spatial frame transform or timestamp inference occurs.

## Worked examples

dense_count=10, frequencies=[3,2], lengths=[1,1], index_bits=3, centroid_bits=32, header_bytes=2 yields symbol_bits5,symbol_bytes1,index_bytes2,codebook_bytes8,total_bytes13,dense_bytes40,compression_ratio40/13.

 dense_count=1, frequencies=[0], lengths=[1], index_bits=1, centroid_bits=16, header_bytes=0 yields symbol_bits0,symbol_bytes0,index_bytes0,codebook_bytes2,total_bytes2,dense_bytes4,compression_ratio2.

## Source and scope

Original bounded component inspired by [2015-deep-compression](https://arxiv.org/abs/1510.00149). No pretrained model, paper benchmark result, retraining or hardware latency claim is included.
