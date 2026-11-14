---
{
  "schema_version": 1,
  "problem_id": "capstone-sim-to-real",
  "content_version": "1.0.0",
  "status": "implemented",
  "title": "Evaluate Sim-to-Real Release Evidence",
  "summary": "Generate deterministic stratified simulation factors and compare synthetic simulator, replay, shadow, and real-domain evidence.",
  "type": "integration",
  "difficulty": "hard",
  "estimated_minutes": 40,
  "domains": [
    "physical-ai"
  ],
  "topics": [
    "capstone",
    "sim-to-real"
  ],
  "paper_ids": [
    "2017-domain-randomization"
  ],
  "paper_sections": [
    "Mechanism described in the linked paper card and theory"
  ],
  "track_ids": [
    "paper-2017-domain-randomization"
  ],
  "prerequisite_problem_ids": [
    "seeded-visual-randomization",
    "stratify-visual-factors",
    "scenario-coverage-confidence"
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
  "entrypoint": "solution.sim_to_real",
  "physical_contract": {
    "frames": [
      "Declared optical camera/world frames or explicitly nonspatial feature axes"
    ],
    "units": {
      "values": "Meters, pixels, milliseconds, normalized features and rates as defined in the contract"
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
      "Two end-to-end worked examples"
    ],
    "hidden_case_families": [
      "Independent scalar mechanism oracle",
      "Failure path and missing evidence",
      "Invalid inputs",
      "Noncontiguous realistic scale and preservation"
    ],
    "performance_class": "none",
    "evaluator_sha256": "32526b229b330756c5a15609932796f04405cd216646c1fecfac8810b0e19f7e"
  },
  "fixtures": {
    "source": "original synthetic examples in examples.md; future generated fixtures use declared seed",
    "license": "CC0-1.0",
    "version_or_hash": "synthetic-v1-seed-20261113"
  },
  "provenance": {
    "authoring_notes": "Original cross-paper synthetic integration. Its stage contracts, limits, diagnostics and release policies are teaching choices, not a reproduced trained model or permission to deploy hardware.",
    "primary_urls": [
      "https://arxiv.org/abs/1703.06907"
    ],
    "implementation_urls": []
  },
  "owners": [
    "perception_completion"
  ],
  "reviewers": [
    "root",
    "research_curator"
  ]
}
---

# Evaluate Sim-to-Real Release Evidence

Implement `sim_to_real(success, observed, latency, seed, min_rate, max_gap, budget_ms)`.

Generate deterministic stratified simulation factors and compare synthetic simulator, replay, shadow, and real-domain evidence.

`success` and `observed` are bool `(N,4)`, with columns in exactly simulator/replay/shadow/real order, `4<=N<=1024`. Success values at unobserved slots are ignored. Rows identify independently sampled scenario trials; repeated observations from one physical episode would violate the statistical assumption. Each row has one factor assignment shared across all four domains. The data are supplied synthetic outcomes, not an actual simulator or real-robot run. `latency` float64 `(N,4)` is milliseconds `[0,10000]` and is also ignored where unobserved after finite/range validation. `seed` is exactly int in `[0,2**32-1]`.

Generate `u=np.random.Generator(np.random.PCG64(seed)).random((N,2))` once. Stratum `s=i%4` at row i combines friction half `s//2` and lighting half `s%2`. Friction is `0.4+0.4*(s//2+u[i,0])`, a dimensionless coefficient; lighting gain is `0.5+0.5*(s%2+u[i,1])`, dimensionless. This stratifies the four joint-factor buckets with counts differing by at most one. It versions a simple synthetic distribution, not the complete paper randomization model.

Return `factors` fresh float64 `(N,2)`, `strata` int64 `(N,)`, `counts` int64 `(4,4)` indexed bucket/domain, `rates` float64 `(4,4)` success fractions (NaN when missing), `mean_rate` float64 `(4,)`, `worst_rate` float64 `(4,)` minimum among observed bucket rates (NaN if no observations), `p95_ms` float64 `(4,)` nearest-rank observed latency (NaN when none), and `wilson` float64 `(4,2)` lower/upper two-sided Wilson intervals for total observed Bernoulli trials per domain, using z=1.959963984540054. Empty domains have both endpoints NaN. `sim_real_gap` float64 `(4,)` is simulator rate minus real rate in each bucket, NaN unless both observed.

`min_rate,max_gap` are Python int/float in `[0,1]`, `budget_ms` in `[0,10000]`. `decision` is `promote` only if **every bucket/domain** has at least two observations, real-domain Wilson lower endpoint is >=min_rate, every bucket's sim-real gap <=max_gap (improvements are allowed), and real-domain p95<=budget_ms; otherwise `hold`. No failure/unknown value is silently filled with zero. Also return `distribution_sha256`: SHA256 hex of the ASCII canonical JSON (`sort_keys=True`, compact separators) of exactly `{schema:1,seed:seed,samples:N,friction:[0.4,1.2],lighting:[0.5,1.5],strata:4}`. The fingerprint identifies this declared distribution and generator seed; supplied outcomes require separate provenance in Notes. Runtime O(N log N), bounded memory O(N).


## Validation and runtime

All array arguments must be NumPy arrays with the stated rank and dtype: real arrays use float64, index arrays int64, masks bool. Real entries must be finite with absolute value at most 1e6 unless a tighter range is stated. All malformed types, shapes, ranges, or scalar arguments raise ValueError. Support noncontiguous arrays, preserve every input, and return fresh arrays (no input storage alias). CPU only; no implicit batch dimension. Comparisons use rtol=1e-6 and atol=1e-7. Fixtures are original synthetic data (CC0-1.0).

## Worked examples

### Example 1: complete synthetic evidence

Use eight rows, all successes and observed, every latency 5 ms, seed 7, minimum rate 0.5, maximum gap 0.2, and budget 10 ms. Strata are `[0,1,2,3,0,1,2,3]`, counts are all 2, rates/means/worst rates are all 1, p95 is 5 ms, gaps are zero. Wilson intervals are approximately `[0.675592,1]` for each domain; decision is `promote`. The first factor pair is approximately `(0.650038,0.948607)`.

### Example 2: a hidden transfer failure

Set real-domain success False at rows 0 and 4. Real overall rate is 0.75, but bucket-zero real rate is 0 and its sim-real gap is 1. Decision is `hold`, even though the other three buckets all succeed. This failure must appear in the evidence report.

## Source and scope

[Primary source](https://arxiv.org/abs/1703.06907). This isolates the stated component using synthetic fixtures; completing it does not reproduce the full paper.

## Implementation and verification plan

Follow the stage equations in Theory. The reference composes bounded NumPy operations and explicit validation; it never executes a trained model or contacts a robot. Runtime is linear in supplied tensor entries except the documented buffer allocation search.
Reference Run and Submit must pass in bubblewrap, with starter and targeted wrong implementation rejected. Independent review precedes publication.
