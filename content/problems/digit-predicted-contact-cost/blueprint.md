---
{
  "schema_version": 1,
  "problem_id": "digit-predicted-contact-cost",
  "content_version": "1.0.0",
  "status": "drafted",
  "title": "Score Predicted Tactile Contact Outcomes",
  "summary": "Candidate tactile predictions can be compared with a desired image before choosing a command.",
  "type": "component",
  "difficulty": "medium",
  "estimated_minutes": 30,
  "domains": [
    "robot-learning"
  ],
  "topics": [
    "2020-digit-tactile-sensor",
    "policy-components"
  ],
  "paper_ids": [
    "2020-digit-tactile-sensor"
  ],
  "paper_sections": [
    "Original operational or vision diagnostic motivated by DIGIT. It is not the paper's reconstruction/controller implementation, calibrated force, or proof of contact safety."
  ],
  "track_ids": [],
  "prerequisite_problem_ids": [],
  "runtime": {
    "language": "python",
    "python": "3.12.3",
    "image_digest": "pending-local-worker-build",
    "runtime_id": "python-3.12.3-numpy-2.2.4-torch-2.6.0-cpu-bwrap-v2",
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
  "entrypoint": "solution.score_contact_outcomes",
  "physical_contract": {
    "frames": [
      "Declared normalized action/feature coordinates; no implicit frame conversion"
    ],
    "units": {
      "values": "Image intensities and normalized commands are dimensionless. Image coordinates use integer pixel centers with x right and y down. Time is seconds except explicitly microsecond exposure metadata."
    },
    "axes": "Capture, image row/column/channel, action and candidate axes defined in the contract",
    "timestamp_assumptions": "One sensor and aligned optical calibration; action timestamps share the sensor clock. No implicit clock or physical-frame conversion.",
    "batching": "Capture, image row/column/channel, action and candidate axes defined in the contract"
  },
  "grading": {
    "mode": "numerical",
    "seed": 20261114,
    "rtol": 1e-07,
    "atol": 1e-09,
    "public_case_families": [
      "two-worked-examples"
    ],
    "hidden_case_families": [
      "documented-boundaries",
      "invalid-inputs",
      "independent-invariants"
    ],
    "performance_class": "cpu"
  },
  "fixtures": {
    "source": "original-synthetic",
    "license": "CC0-1.0",
    "version_or_hash": "synthetic-v1-seed-20261113"
  },
  "provenance": {
    "authoring_notes": "Original operational or vision diagnostic motivated by DIGIT. It is not the paper's reconstruction/controller implementation, calibrated force, or proof of contact safety.",
    "primary_urls": [
      "https://arxiv.org/abs/2005.14679"
    ],
    "paper_card": "research/papers/humanoid-dexterity-tactile/2020-digit-tactile-sensor.md",
    "manifest": "research/manifests/expansion-150.md"
  },
  "owners": [
    "research_curator"
  ],
  "reviewers": []
}
---

# Score Predicted Tactile Contact Outcomes

## Contract

`predictions` is real `(K, H, W, C)`, `goal` is real `(H, W, C)`, `roi` is Boolean `(H, W)`, `action_effort` is real `(K,)` and `valid` is Boolean `(K,)`. Bounds are `0 <= K <= 64`, `1 <= H, W <= 64` and `1 <= C <= 3`. Image intensities lie in `[0, 1]`, effort in `[0, 1000]`, and scalar `effort_weight` in `[0, 100]`. The ROI must contain at least one pixel. Prediction and goal share pixel alignment and optical/exposure conventions.

For each candidate, compute image MSE over ROI pixels and all channels. Cost equals this MSE plus `effort_weight * action_effort`. Effort is a supplied dimensionless sum of squared normalized commands; the weight gives a common dimensionless cost convention.

Return a dictionary with `image_error` and `costs` (float64 `(K,)`, NaN for invalid candidates) and `best_index` (Python int, the lowest index attaining the minimum valid cost, or -1 if no valid candidate exists). Validate all numeric entries even when their candidate or pixel is masked.

Predicted images are supplied; no dynamics model runs. This original photometric planning diagnostic does not reproduce the DIGIT controller or measure force and safety.

Unless a tighter bound is stated below, numeric array-like inputs must have real integer/floating dtype after `np.asarray`, be finite with absolute values <=1e6 and at most 1,000,000 entries. Boolean, complex, string and object numeric arrays are invalid; Boolean masks must have Boolean dtype. Integer arrays/scalars exclude booleans. All invalid inputs raise ValueError. Return new arrays, preserve inputs, and compute floating outputs in float64 on CPU. No automatic differentiation is required.

## Source scope

Original operational or vision diagnostic motivated by DIGIT. It is not the paper's reconstruction/controller implementation, calibrated force, or proof of contact safety.

## Evaluation plan

Two numerical examples, independent invariants and documented invalid cases; deterministic seed20261114. Numeric rtol1e-7/atol1e-9, exact integer/Boolean fields. Synthetic CC0 fixtures. Run public and hidden cases in the isolated worker; reject empty starter and a mechanism-specific mutant.

## Visualization

Original trace table in Theory with a textual alternative; no motion required.
