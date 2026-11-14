---
{
  "schema_version": 1,
  "problem_id": "grounding-language-query-selection",
  "content_version": "1.0.0",
  "status": "published",
  "title": "Select Language-Guided Object Queries",
  "summary": "Select visual queries by their strongest usable text-token compatibility.",
  "type": "component",
  "difficulty": "medium",
  "estimated_minutes": 40,
  "domains": [
    "perception"
  ],
  "topics": [
    "grounding-dino",
    "grounding-language-query-selection"
  ],
  "paper_ids": [
    "2023-grounding-dino"
  ],
  "paper_sections": [
    "Language-guided query selection and text-grounded box outputs; phrase aggregation and orchestration are declared teaching contracts"
  ],
  "track_ids": [
    "paper-2023-grounding-dino"
  ],
  "prerequisite_problem_ids": [],
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
  "entrypoint": "solution.select_grounded_queries",
  "physical_contract": {
    "frames": [
      "Visual-query and text-token identity axes"
    ],
    "units": {
      "values": "dimensionless compatibility scores"
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
    "evaluator_sha256": "7b1a240d1d755b7644f02f5bb94bbc6d94469e5fc66b0bacff9eee15387ebe20"
  },
  "fixtures": {
    "source": "original synthetic examples in examples.md; future generated fixtures use declared seed",
    "license": "CC0-1.0",
    "version_or_hash": "synthetic-v1-seed-20261113"
  },
  "provenance": {
    "authoring_notes": "Original bounded teaching component; no source code or figures copied. Systems diagnostics are teaching contracts, not paper benchmark claims.",
    "primary_urls": [
      "https://arxiv.org/abs/2303.05499"
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

# Select Language-Guided Object Queries

Implement `select_grounded_queries(scores: np.ndarray, usable_tokens: np.ndarray, k: int) -> tuple[np.ndarray, np.ndarray]`.

Select visual queries by their strongest usable text-token compatibility.
scores float64 (Q,T) contains logits or unnormalized similarities,0<=Q<=4096,1<=T<=512; usable_tokens bool(T,) excludes padding and special tokens. k is built-in int non-bool with 0<=k<=Q. If k>0 at least one token must be usable. Rank each query by max score across usable tokens; sort descending, tie smaller query index. Return int64(k,) query indices and corresponding float64(k,) rank scores in that order. k=0 returns empty arrays even with no usable tokens. No softmax, sigmoid, NMS or decoder is run; supplied scores already follow the model's feature enhancement stage.

## Validation and runtime

All array arguments must be NumPy arrays with the stated rank and dtype: real arrays use float64, index arrays int64, masks bool. Real entries must be finite with absolute value at most 1e6 unless a tighter range is stated. All malformed types, shapes, ranges, or scalar arguments raise ValueError. Support noncontiguous arrays, preserve every input, and return fresh arrays (no input storage alias). CPU only; no implicit batch dimension. Comparisons use rtol=1e-6 and atol=1e-7. Fixtures are original synthetic data (CC0-1.0).

## Worked examples

1. scores=`[[1,100,3],[4,0,2],[4,9,1]]`, usable=`[True,False,True]`, k=2 gives indices `[1,2]`, scores `[4,4]`. The masked score 100 cannot win.
2. scores=`[[-3,-1],[-2,-4]]`, all tokens usable, k=1 gives index `[0]`, score `[-1]`. Negative logits remain valid evidence.

## Source and scope

[Primary source](https://arxiv.org/abs/2303.05499). This isolates the stated component using synthetic fixtures; completing it does not reproduce the full paper.

## Implementation and verification plan

Compute usable-token maxima and stable descending query ranking. O(QT+Q log Q) time.
Reference Run and Submit must pass in bubblewrap, with starter and targeted wrong implementation rejected. Independent review precedes publication.
