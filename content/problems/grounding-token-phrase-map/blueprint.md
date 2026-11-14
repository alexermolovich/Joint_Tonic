---
{
  "schema_version": 1,
  "problem_id": "grounding-token-phrase-map",
  "content_version": "1.0.0",
  "status": "published",
  "title": "Map Text Tokens to Grounded Phrases",
  "summary": "Map character spans to tokens with an explicit half-open overlap rule.",
  "type": "component",
  "difficulty": "easy",
  "estimated_minutes": 40,
  "domains": [
    "perception"
  ],
  "topics": [
    "grounding-dino",
    "grounding-token-phrase-map"
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
  "entrypoint": "solution.phrase_token_map",
  "physical_contract": {
    "frames": [
      "Original instruction string offsets"
    ],
    "units": {
      "values": "Unicode code-point indices"
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
    "evaluator_sha256": "901c5da2b8922f6c525ff0ede1eedcc6a018a1922723d8ff88943a93e92748e7"
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

# Map Text Tokens to Grounded Phrases

Implement `phrase_token_map(token_offsets: np.ndarray, phrase_spans: np.ndarray, text_length: int) -> np.ndarray`.

Map character spans to tokens with an explicit half-open overlap rule.
token_offsets int64 (T,2) and phrase_spans int64 (P,2) store [start,end) character offsets into the same original string,0<=T,P<=4096. text_length is a built-in int 0..1000000, not bool. Tokens may have empty offsets [a,a), representing special/padding tokens; phrases must be nonempty. All bounds satisfy 0<=start<=end<=text_length. Return bool (P,T), true for positive-length token/phrase intersection: max(starts)<min(ends). Preserve order, allow overlapping phrases and unsorted offsets, and permit all-false rows when tokenization provides no coverage. Offsets are Unicode code-point indices supplied by the caller, not bytes. This is an original deterministic alignment contract; no tokenizer or phrase parser runs.

## Validation and runtime

All array arguments must be NumPy arrays with the stated rank and dtype: real arrays use float64, index arrays int64, masks bool. Real entries must be finite with absolute value at most 1e6 unless a tighter range is stated. All malformed types, shapes, ranges, or scalar arguments raise ValueError. Support noncontiguous arrays, preserve every input, and return fresh arrays (no input storage alias). CPU only; no implicit batch dimension. Comparisons use rtol=1e-6 and atol=1e-7. Fixtures are original synthetic data (CC0-1.0).

## Worked examples

1. Tokens `[[0,0],[0,3],[4,7],[8,11]]`, phrase `[4,11)`, text_length=11 gives `[False,False,True,True]`.
2. Token `[2,5)` overlaps phrase `[4,6)` but not phrase `[5,6)`: touching at a half-open endpoint has zero overlap.

## Source and scope

[Primary source](https://arxiv.org/abs/2303.05499). This isolates the stated component using synthetic fixtures; completing it does not reproduce the full paper.

## Implementation and verification plan

Compute pairwise interval intersections by broadcast maxima/minima. O(PT) time/output storage.
Reference Run and Submit must pass in bubblewrap, with starter and targeted wrong implementation rejected. Independent review precedes publication.
