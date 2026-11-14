---
{
  "schema_version": 1,
  "problem_id": "pid-anti-windup",
  "content_version": "1.0.0",
  "status": "reviewed",
  "title": "PID with Integral Anti-Windup",
  "summary": "PID with Integral Anti-Windup",
  "type": "function",
  "difficulty": "easy",
  "estimated_minutes": 25,
  "domains": [
    "robotics-foundations"
  ],
  "topics": [
    "control"
  ],
  "paper_ids": [],
  "paper_sections": [],
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
  "entrypoint": "solution.pid_step",
  "physical_contract": {
    "frames": [
      "one-robot-joint"
    ],
    "units": {
      "error": "radians",
      "integral": "radian-seconds",
      "dt": "seconds",
      "command": "normalized actuator effort"
    },
    "axes": "Positive error commands positive joint actuation.",
    "timestamp_assumptions": "One synchronized measurement clock; no offset correction.",
    "batching": "One scalar control step; gains length3, limits length2."
  },
  "grading": {
    "mode": "numerical",
    "seed": 20261113,
    "rtol": 1e-07,
    "atol": 1e-09,
    "public_case_families": [
      "worked-examples"
    ],
    "hidden_case_families": [
      "boundary",
      "validation",
      "empty-where-supported",
      "immutability",
      "scale"
    ],
    "performance_class": "cpu"
  },
  "fixtures": {
    "source": "original-synthetic",
    "license": "CC0-1.0",
    "version_or_hash": "synthetic-v1-seed-20261113"
  },
  "provenance": {
    "authoring_notes": "Original robotics-foundation exercise; no paper headline result or external dataset.",
    "primary_urls": [
      "https://fbswiki.org/wiki/index.php/Feedback_Systems"
    ],
    "implementation_urls": []
  },
  "owners": [
    "main-agent"
  ],
  "reviewers": [
    "code_issue_scout"
  ]
}
---

# PID with Integral Anti-Windup

## Contract

Implement **pid_step(error, previous_error, integral, dt, gains, output_limits)**.

The first four inputs are finite Python or NumPy real scalars excluding bool; 0<dt<=1e6. Other scalar magnitudes are <=1e6. gains=(kp,ki,kd) contains three finite nonnegative values <=1e6. output_limits=(lower,upper) contains two finite values of magnitude <=1e6, lower<upper. Reject numeric strings, booleans, complex data, malformed shapes, nonfinite inputs and nonfinite intermediate calculations with ValueError.

Errors refer to consecutive samples of one joint in radians on one clock; integral is radian-seconds and dt seconds. Gain units are command/rad, command/(rad*s), command*s/rad. Return three Python floats (command,next_integral,derivative).

Compute derivative=(error-previous_error)/dt, candidate integral Ic=integral+error*dt, and candidate command uc=kp*error+ki*Ic+kd*derivative. Reject Ic exactly when (uc>upper and error>0) or (uc<lower and error<0). Otherwise accept it, including exact equality. Recompute effort using the accepted integral, then clip to the limits. Inputs remain unchanged.

No derivative filtering, simulator integration or motor safety guarantee.

## Implementation and grading plan

Reference and tests follow independent contract review. Verify worked examples, documented boundaries/errors, dtype/shape, input preservation and synthetic batches. Run public and hidden tests in the existing isolated CPU worker. Limits above are actual shared worker limits; the local image digest remains pending.

## Theory and visualization

See theory.md for intuition, defined equations, numerical trace tables and robot failure analysis. Static tables need no reduced-motion variant.

## Provenance and operations

Fixtures are original synthetic CC0-1.0 data. Record content/runtime versions and sensor/calibration versions where relevant. No simulator, GPU, hosted service or external dataset is needed.
