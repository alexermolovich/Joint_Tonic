---
{
  "schema_version": 1,
  "problem_id": "calibration-sensitivity",
  "content_version": "1.0.0",
  "status": "implemented",
  "title": "Quantify Calibration Sensitivity",
  "summary": "Quantify Calibration Sensitivity",
  "type": "function",
  "difficulty": "medium",
  "estimated_minutes": 35,
  "domains": [
    "robotics-mlops"
  ],
  "topics": [
    "robotics-mlops",
    "2018-dynamics-randomization"
  ],
  "paper_ids": [
    "2018-dynamics-randomization"
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
  "entrypoint": "solution.calibration_sensitivity",
  "physical_contract": {
    "frames": [
      "Caller-declared calibration/frame retained; no implicit spatial transform"
    ],
    "units": {
      "baseline/plus/minus": "dimensionless performance score",
      "delta/scales": "caller-declared physical parameter unit per row",
      "slope": "score per parameter unit",
      "curvature": "score per squared parameter unit",
      "scaled_sensitivity": "dimensionless score"
    },
    "axes": "K parameters by M metrics; matched plus/minus evaluations share nominal calibration",
    "timestamp_assumptions": "No live timestamps; episode scenarios are supplied observations or declarations.",
    "batching": "K parameters by M metrics; matched plus/minus evaluations share nominal calibration"
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
    "evaluator_sha256": "5ff6e9258bb125f185c87d49c895045ac93c469f99988371ff114c408353d8b2",
    "performance_class": "none; no timing leaderboard"
  },
  "fixtures": {
    "source": "original synthetic fixtures",
    "license": "CC0-1.0",
    "version_or_hash": "original-synthetic-v1"
  },
  "provenance": {
    "authoring_notes": "This original bounded component is motivated by [2018-dynamics-randomization](https://arxiv.org/abs/1710.06537). It does not reproduce the full paper, trained model or benchmark protocol.",
    "primary_urls": [
      "https://arxiv.org/abs/1710.06537"
    ],
    "paper_card": "research/papers/mlops-sim2real/2018-dynamics-randomization.md",
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

# Quantify Calibration Sensitivity

Implement calibration_sensitivity(baseline, plus, minus, delta, scales) -> dict.

baseline is NumPy float64(M,), plus and minus float64(K,M), delta and scales float64(K,),1<=K<=64,1<=M<=64. All values finite; baseline/plus/minus in[-1e6,1e6], delta and scales in[1e-6,1e6]. Each metric is a comparable dimensionless performance score; parameter j uses its caller-declared physical unit, and both delta[j] and scales[j] use that same unit. plus[j]/minus[j] are matched evaluations after changing only parameter j by ±delta[j] about one nominal calibration. scales[j] is a physical uncertainty scale.

Return float64(K,M) slope=(plus-minus)/(2*delta[:,None]), curvature=(plus-2*baseline[None,:]+minus)/(delta[:,None]**2), scaled_sensitivity=abs(slope)*scales[:,None], and ranking:int64(K,), sorted by descending max scaled_sensitivity per parameter, breaking exact ties by smaller input index. Preserve inputs and return independent arrays; noncontiguous inputs valid. Invalid contracts raise ValueError. No parameter names or perturbations are inferred; no simulator runs occur.

Slope units are score per physical-unit, curvature score per physical-unit squared, scaled sensitivity dimensionless. These finite differences are a local diagnostic, not a global robustness bound or proof that the parameter perturbations are physically valid.
