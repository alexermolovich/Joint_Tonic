---
{
  "schema_version": 1,
  "problem_id": "sim-to-real-robustness-gate",
  "content_version": "1.0.0",
  "status": "implemented",
  "title": "Gate Sim-to-Real Release with Robustness Evidence",
  "summary": "Gate Sim-to-Real Release with Robustness Evidence",
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
  "entrypoint": "solution.robustness_release_gate",
  "physical_contract": {
    "frames": [
      "Caller-declared calibration/frame retained; no implicit spatial transform"
    ],
    "units": {
      "trials/successes": "independent scenario episode counts",
      "success_rate": "dimensionless fraction",
      "worst_return": "dimensionless comparable return",
      "distribution": "SHA-256 declaration identity"
    },
    "axes": "One summary per required named scenario slice; no pooled substitution",
    "timestamp_assumptions": "No live timestamps; episode scenarios are supplied observations or declarations.",
    "batching": "One summary per required named scenario slice; no pooled substitution"
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
    "evaluator_sha256": "79812e6f18b5581085964c4a1f6ccacbf0f77b1b90649386ad24f3e98e7183e3",
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

# Gate Sim-to-Real Release with Robustness Evidence

Implement robustness_release_gate(required, evidence, expected_distribution, min_trials, min_success_rate, min_worst_return) -> dict.

required is a Python list of1..128 unique ASCII slice IDs[a-z][a-z0-9_-]{0,63}. expected_distribution is64 lowercase hex. min_trials is a built-in non-bool int1..1e6; min_success_rate is a finite built-in non-bool int/float in[0,1]; min_worst_return finite in[-1e6,1e6]. evidence is a Python list of0..128 exact dicts with keys slice, distribution_sha256, trials, successes, worst_return. Slice IDs are unique and must be required. Distribution digest has the same hex schema; trials is a built-in int1..1e6, successes a built-in int0..trials, and worst_return a finite built-in numeric in[-1e6,1e6]. Validate every evidence record even when another record already fails.

Return {"approved":bool,"reasons":list[str]}. For each required slice in lexicographic order, emit slice+":missing" if absent. Otherwise emit every failing reason in this fixed order: distribution (digest mismatch), trials (trials<min_trials), success (successes/trials<min_success_rate), worst-return (worst_return<min_worst_return). Equality passes. Invalid contracts raise ValueError; missing/weak/mismatched valid evidence returns rejection reasons. Preserve inputs.

Trials are per-slice independent scenario episodes; success fractions and comparable normalized returns are dimensionless. The distribution hash identifies a declared simulation protocol. This original deterministic evidence checklist does not certify real-robot safety, verify raw logs, estimate confidence, deploy a policy or replace hardware validation.
