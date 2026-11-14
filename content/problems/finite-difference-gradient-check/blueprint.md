---
{
  "schema_version": 1,
  "problem_id": "finite-difference-gradient-check",
  "content_version": "1.0.0",
  "status": "implemented",
  "title": "Finite-Difference Gradient Check",
  "summary": "Finite-Difference Gradient Check",
  "type": "function",
  "difficulty": "medium",
  "estimated_minutes": 35,
  "domains": [
    "robotics-foundations"
  ],
  "topics": [
    "robotics-foundations",
    "numerics-evaluation"
  ],
  "paper_ids": [],
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
  "entrypoint": "solution.check_calibration_gradient",
  "physical_contract": {
    "frames": [
      "Caller-aligned robot sensor/controller frames; no implicit transform"
    ],
    "units": {
      "design/parameters/target": "dimensionless normalized calibration quantities",
      "step": "normalized parameter perturbation",
      "gradient": "dimensionless loss per normalized parameter unit"
    },
    "axes": "design(M,D),parameters(D),target(M),analytic(D); each column one calibration offset",
    "timestamp_assumptions": "Episodes and fixed sample ordering supplied; no wall clock or timing inference.",
    "batching": "design(M,D),parameters(D),target(M),analytic(D); each column one calibration offset"
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
    "evaluator_sha256": "5ae5ea718ee7e60c7b696407b3506b802a8019e3462f84dc19d879464bc166a1",
    "performance_class": "none; no timing leaderboard"
  },
  "fixtures": {
    "source": "original synthetic fixtures",
    "license": "CC0-1.0",
    "version_or_hash": "original-synthetic-v1"
  },
  "provenance": {
    "authoring_notes": "Original robotics foundation with synthetic fixtures; no paper-derived implementation.",
    "primary_urls": [
      "https://numpy.org/doc/2.2/reference/"
    ]
  },
  "owners": [
    "curriculum_continuation"
  ],
  "reviewers": [
    "root"
  ]
}
---

# Finite-Difference Gradient Check

Implement check_calibration_gradient(design, parameters, target, analytic, step, tolerance) -> dict.

design is NumPy float64(M,D), parameters and analytic float64(D,), target float64(M,),1<=M<=64,1<=D<=32. Arrays finite with magnitude<=100. step is finite built-in non-bool numeric in[1e-6,1e-2]; tolerance finite built-in numeric in[0,1], non-bool. Define loss(x)=0.5*sum((design@x-target)**2), no division by M. For each parameter independently evaluate loss at x±step*unit_vector; numeric[j]=(loss_plus-loss_minus)/(2*step). Return numeric:float64(D,), relative_error:float64(D,)=abs(numeric-analytic)/maximum(1,abs(numeric),abs(analytic)), passed:bool true iff every error<=tolerance. Preserve inputs; noncontiguous valid. Invalid contracts raise ValueError.

The design is a dimensionless normalized local sensor-calibration model, parameters normalized calibration offsets, target normalized residual measurements. This checks the supplied gradient against explicit finite differences of the stated objective, not an analytic shortcut. The finite difference is approximate; near-cancellation can require a larger step or tolerance. No simulator or differentiable framework is invoked.
