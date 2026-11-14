---
{
  "schema_version": 1,
  "problem_id": "aggregate-policy-returns",
  "content_version": "0.1.0",
  "status": "reviewed",
  "title": "Aggregate Mean and Worst-Case Policy Returns",
  "summary": "Aggregate Mean and Worst-Case Policy Returns",
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
  "entrypoint": "solution.aggregate_policy_returns",
  "physical_contract": {
    "frames": [
      "Caller-declared calibration/frame retained; no implicit spatial transform"
    ],
    "units": {
      "returns": "dimensionless comparable episodic return",
      "tail_fraction": "dimensionless empirical probability mass"
    },
    "axes": "float64(P,E), policies by shared ordered evaluation episodes; outputs(P,)",
    "timestamp_assumptions": "No live timestamps; episode scenarios are supplied observations or declarations.",
    "batching": "float64(P,E), policies by shared ordered evaluation episodes; outputs(P,)"
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
    "evaluator_sha256": "6145fb3b1ca122b7fc3009901b74438e4874612a218e279874afbb84acc56851",
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

# Aggregate Mean and Worst-Case Policy Returns

Implement aggregate_policy_returns(returns, tail_fraction) -> dict.

returns is NumPy float64(P,E),1<=P<=64,1<=E<=10000,total<=200000, finite values in[-1e6,1e6]. Each row is one policy evaluated on the same ordered E scenario episodes, with comparable dimensionless undiscounted returns; higher is better. tail_fraction is a finite built-in non-bool int/float in(0,1]. Return fresh float64(P,) arrays mean, worst, lower_tail. mean is the arithmetic mean, worst the minimum. For each sorted ascending row x, let q=tail_fraction*E, k=floor(q), a=q-k. lower_tail=(sum(x[:k])+a*x[k])/q, omitting the fractional term when k=E. This fractional-mass empirical lower-tail mean is defined even when q<1. Preserve inputs; noncontiguous inputs valid. Invalid contracts raise ValueError.

This reports supplied episodic returns, not discounted-step accumulation, confidence bounds, importance weighting, policy learning, or a robust-control guarantee. The lower-tail statistic is an original evaluation extension to dynamics randomization.
