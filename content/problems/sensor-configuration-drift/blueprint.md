---
{
  "schema_version": 1,
  "problem_id": "sensor-configuration-drift",
  "content_version": "1.0.0",
  "status": "published",
  "title": "Compare Drift Across Sensor Configurations",
  "summary": "`compare_drift(estimated, reference, valid, baseline)` estimated(C,N,3),1<=C<=64,1<=N<=8192,C*N<=262144; reference(N,3),valid(C,N), baseline builtinint0..C-1. Positions meters, already same world frame and matched timestamps. Use ONLY common evidence common=all(valid,axis0) for every configuration. Return common(N),countint,errors(C,N) with NaN outsidecommon,rmse(C),endpoint(C),improvement(C),best int. Errors Euclidean position norm; RMSE=sqrt(mean(errors\u00b2)); endpoint uses highest common sample index, not arbitrary last valid perconfig; improvement=baseline_rmse-rmse inmeters. Best minRMSE first-index ties; ifno common count0,allmetricsNaN,best-1. No posthoc alignment, interpolation, or assertion that better absolute error is solely less accumulated drift. Example reference[[0,0,0],[1,0,0]], estimated0=reference,estimated1=reference+[1,0,0],allvalid,baseline1=>rmse[0,1],endpoint[0,1],improvement[1,0],best0. Examplevalid[[True,False],[False,True]]=>no common. Comparison intentionally sacrifices coverage to prevent missing-data advantages.",
  "type": "component",
  "difficulty": "medium",
  "estimated_minutes": 40,
  "domains": [
    "geometry-state-estimation"
  ],
  "topics": [
    "geometry-calibration-slam",
    "vins-fusion"
  ],
  "paper_ids": [
    "2019-vins-fusion"
  ],
  "paper_sections": [
    "Mechanism described in the linked paper card and theory"
  ],
  "track_ids": [
    "paper-2019-vins-fusion"
  ],
  "prerequisite_problem_ids": [
    "aligned-trajectory-position-error"
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
  "entrypoint": "solution.compare_drift",
  "physical_contract": {
    "frames": [
      "Explicit world, body, camera or dimensionless scaled-state frame in the contract"
    ],
    "units": {
      "values": "Meters, seconds, radians, pixels, or dimensionless normalized quantities as defined per argument"
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
    "evaluator_sha256": "83d530dfbd6c8b2940564122a3f19ce3425be36f9ecead34da31c1986689a5ca"
  },
  "fixtures": {
    "source": "original synthetic examples in examples.md; future generated fixtures use declared seed",
    "license": "CC0-1.0",
    "version_or_hash": "synthetic-v1-seed-20261113"
  },
  "provenance": {
    "authoring_notes": "Original bounded teaching component; no source code or figures copied. Systems diagnostics are teaching contracts, not paper benchmark claims.",
    "primary_urls": [
      "https://arxiv.org/abs/1901.03642"
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

# Compare Drift Across Sensor Configurations

Implement `compare_drift(estimated, reference, valid, baseline)`.

`compare_drift(estimated, reference, valid, baseline)` estimated(C,N,3),1<=C<=64,1<=N<=8192,C*N<=262144; reference(N,3),valid(C,N), baseline built-in int0..C-1.

Positions meters, already same world frame and matched timestamps.

Use ONLY common evidence common=all(valid,axis0) for every configuration.

Return common(N),count int,errors(C,N) with NaN outsidecommon,rmse(C),endpoint(C),improvement(C),best int.

Errors Euclidean position norm; RMSE=sqrt(mean(errors²)); endpoint uses highest common sample index, not arbitrary last valid per configuration; improvement=baseline_rmse - rmse inmeters.

Best minRMSE first-index ties; if no common count 0,all metrics NaN,best -1.

No posthoc alignment, interpolation, or assertion that better absolute error is solely less accumulated drift.

Example: reference[[0,0,0],[1,0,0]], estimated0=reference,estimated1=reference+[1,0,0],all valid,baseline1=>rmse[0,1],endpoint[0,1],improvement[1,0],best0.

Example: valid[[True,False],[False,True]]=>no common.

Comparison intentionally sacrifices coverage to prevent missing-data advantages.

## Validation and runtime

All array arguments must be NumPy arrays with the stated rank and dtype: real arrays use float64, index arrays int64, masks bool.

Real entries must be finite with absolute value at most 1e6 unless a tighter range is stated.

All malformed types, shapes, ranges, or scalar arguments raise ValueError.

Support noncontiguous arrays, preserve every input, and return fresh arrays (no input storage alias).

CPU only; no implicit batch dimension.

Comparisons use rtol=1e-6 and atol=1e-7.

Fixtures are original synthetic data (CC0-1.0).

## Worked examples

1. Reference positions are [[0,0,0],[1,0,0]].

Configuration 0 equals reference; configuration 1 adds [1,0,0] at both times.

With all entries valid and baseline 1, RMSE and endpoint errors are [0,1] meters, improvement [1,0], and best index 0.
2. Valid masks [[True,False],[False,True]] have no common sample.

Count is 0, best is -1, and every error/aggregate is NaN.

## Source and scope

[Primary source](https://arxiv.org/abs/1901.03642).

This isolates the stated component using synthetic fixtures; completing it does not reproduce the full paper.

## Implementation and verification plan

Intersect availability first, then compute Euclidean errors and aggregates on that shared support.

Time/storage O(CN).
Reference Run and Submit must pass in bubblewrap, with starter and targeted wrong implementation rejected.

Independent review precedes publication.
