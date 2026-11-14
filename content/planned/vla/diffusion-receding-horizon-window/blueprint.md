---
{
  "schema_version": 1,
  "problem_id": "diffusion-receding-horizon-window",
  "content_version": "0.1.0",
  "status": "reviewed",
  "title": "Execute a Receding-Horizon Action Window",
  "summary": "Extract the controller-supported prefix of a predicted future trajectory after a specified alignment offset.",
  "type": "component",
  "difficulty": "easy",
  "estimated_minutes": 35,
  "domains": [
    "VLA and embodied robot learning"
  ],
  "topics": [
    "2023-diffusion-policy",
    "policy-components"
  ],
  "paper_ids": [
    "2023-diffusion-policy"
  ],
  "paper_sections": [
    "SectionIII: receding-horizon control"
  ],
  "track_ids": [],
  "prerequisite_problem_ids": [
    "act-sliding-action-chunks"
  ],
  "runtime": {
    "language": "python",
    "python": "3.12.3",
    "image_digest": "pending-local-worker-build",
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
  "entrypoint": "solution.receding_horizon_window",
  "physical_contract": {
    "frames": [
      "As specified in the typed contract; no implicit frame conversion"
    ],
    "units": {
      "actions": "caller-declared normalized Euclidean action channels",
      "embeddings": "dimensionless",
      "time": "fixed control ticks, not flow time"
    },
    "axes": "B=independent observations,H=future control ticks,D=unchanged actuator channels",
    "timestamp_assumptions": "One aligned observation per batch item; temporal calibration is upstream.",
    "batching": "trajectory(B,H,D), valid(B,H), output(B,execute_steps,D)"
  },
  "grading": {
    "mode": "numerical",
    "seed": 20261113,
    "rtol": 1e-06,
    "atol": 1e-07,
    "public_case_families": [
      "two-worked-examples"
    ],
    "hidden_case_families": [
      "shape-dtype-validation",
      "masked-behavior",
      "boundaries",
      "noncontiguous-and-immutability",
      "gradients-where-declared",
      "realistic-scale"
    ]
  },
  "fixtures": {
    "source": "Original synthetic inputs",
    "license": "CC0-1.0",
    "version_or_hash": "synthetic-v1-seed-20261113"
  },
  "provenance": {
    "authoring_notes": "Extract the controller-supported prefix of a predicted future trajectory after a specified alignment offset. This returns a command buffer for a synthetic controller; it does not drive a robot, run denoising or infer the observation-horizon offset.",
    "primary_urls": [
      "https://arxiv.org/abs/2303.04137"
    ],
    "implementation_urls": []
  },
  "owners": [
    "vla_implementation"
  ],
  "reviewers": [
    "code_issue_scout"
  ]
}
---

# Execute a Receding-Horizon Action Window

## Paper connection and scope

Extract the controller-supported prefix of a predicted future trajectory after a specified alignment offset. This returns a command buffer for a synthetic controller; it does not drive a robot, run denoising or infer the observation-horizon offset.

## Contract

Implement receding_horizon_window(trajectory, valid, offset, execute_steps), returning a fresh copy of shape (B,execute_steps,D).

trajectory is a float32/float64 NumPy array (B,H,D), finite with abs(value)<=1e6. Require 1<=B<=64,1<=H<=256,1<=D<=64, and <=2,000,000 elements. valid is a bool NumPy array (B,H). offset and execute_steps are built-in non-bool ints; 0<=offset<H,1<=execute_steps<=H,offset+execute_steps<=H.

Copy trajectory[:,offset:offset+execute_steps,:] preserving dtype, order, units and coordinate frame. Every selected validity entry must be True; otherwise raise ValueError for the entire batch. Invalid entries outside the selected window are allowed, but all trajectory values must still satisfy finiteness/range. Do not skip holes, shorten the requested window, extrapolate, repeat the last action or zero invalid selected commands. Noncontiguous inputs are supported. Never mutate inputs or return an alias.

Raise TypeError for non-array trajectory/valid or invalid integer types. Raise ValueError for every array-contract, range or selected-validity violation. Each batch item is one already-aligned observation with a fixed controller period; offset is a discrete tick count, not seconds. Caller supplies physical channel conventions. No quaternion averaging, actuator safety checking or actual execution is performed.

## Reference and evaluator plan

Implement the declared tensor/array operations without external models or assets. Validate each stated boundary before computation. Test the public examples, masks/reduction axes, invalid contracts, fresh output storage, noncontiguous data, exact dtype and gradients where required. Use seed20261113 for synthetic scale tests. Run public and hidden cases through the shared local bubblewrap worker; runtime limits above are actual shared limits, not a performance ranking. OCI image digest remains pending for this local environment.

## Visualization and theory

The original theory includes essential display math, defined symbols, a static shape/timeline table, a worked calculation, robot failure modes and questions. Tables render without an animation or motion preference. No external figures or paper code are copied.

## Provenance

Primary source: https://arxiv.org/abs/2303.04137; SectionIII: receding-horizon control. Numerical fixtures are original and CC0-1.0. Passing this component does not reproduce published training results.
