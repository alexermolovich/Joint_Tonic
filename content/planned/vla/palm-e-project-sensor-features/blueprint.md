---
{
  "schema_version": 1,
  "problem_id": "palm-e-project-sensor-features",
  "content_version": "0.1.0",
  "status": "reviewed",
  "title": "Project Continuous Sensor Features into Language Width",
  "summary": "Isolate a supplied affine projection into a language embedding width.",
  "type": "component",
  "difficulty": "easy",
  "estimated_minutes": 35,
  "domains": [
    "VLA and embodied robot learning"
  ],
  "topics": [
    "2023-palm-e",
    "policy-components"
  ],
  "paper_ids": [
    "2023-palm-e"
  ],
  "paper_sections": [
    "Sections3\u20134: continuous sensor embeddings"
  ],
  "track_ids": [],
  "prerequisite_problem_ids": [],
  "runtime": {
    "language": "python",
    "python": "3.12.3",
    "image_digest": "pending-local-worker-build",
    "dependencies": {
      "numpy": "2.2.4",
      "torch": "2.6.0+cpu"
    },
    "limits": {
      "wall_seconds": 18,
      "cpu_seconds": 10,
      "memory_mb": 4096,
      "output_kb": 64
    }
  },
  "entrypoint": "solution.project_sensor_features",
  "physical_contract": {
    "frames": [
      "As specified in the typed contract; no implicit frame conversion"
    ],
    "units": {
      "actions": "caller-declared normalized Euclidean action channels",
      "embeddings": "dimensionless",
      "time": "fixed control ticks, not flow time"
    },
    "axes": "B=independent observations,N=sensor token positions,C=sensor width,E=language width",
    "timestamp_assumptions": "One aligned observation per batch item; temporal calibration is upstream.",
    "batching": "features(B,N,C), weight(C,E), bias(E), valid(B,N), output(B,N,E)"
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
    "authoring_notes": "Isolate a supplied affine projection into a language embedding width. PaLM-E permits richer modality encoders; this exercise does not assert every encoder is one affine layer. Inputs are already normalized modality features, not raw heterogeneous physical units.",
    "primary_urls": [
      "https://arxiv.org/abs/2303.03378"
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

# Project Continuous Sensor Features into Language Width

## Paper connection and scope

Isolate a supplied affine projection into a language embedding width. PaLM-E permits richer modality encoders; this exercise does not assert every encoder is one affine layer. Inputs are already normalized modality features, not raw heterogeneous physical units.

## Contract

Implement project_sensor_features(features, weight, bias, valid), returning one fresh tensor (B,N,E).

features is a CPU float32/float64 tensor (B,N,C), weight (C,E), bias (E,), and valid a CPU bool tensor (B,N). All floating tensors share dtype and have finite entries with abs(value)<=1000. Require 1<=B<=32,0<=N<=1024,1<=C,E<=512; each floating input and output has <=2,000,000 elements. Empty N and all-false masks are valid. Inputs may be noncontiguous.

For valid tokens compute output[b,n,e]=sum_c features[b,n,c]*weight[c,e]+bias[e]. Invalid token rows are exactly zero, including the bias contribution. The bias is applied after the matrix product and masked afterward. Return matching dtype/device, no input mutation or storage alias, and preserve autograd through features, weight and bias. Masked rows have zero influence on every gradient. Do not create trainable parameters, normalize features, add positions, or merge batch/token axes semantically.

Raise TypeError if any argument is not a tensor. Raise ValueError for every tensor-contract violation, including invalid values in masked rows. Features are dimensionless normalized sensor descriptors measured in one synchronized observation per batch item. Row order stays unchanged; projected channels are language-embedding coordinates, not metric robot axes.

## Reference and evaluator plan

Implement the declared tensor/array operations without external models or assets. Validate each stated boundary before computation. Test the public examples, masks/reduction axes, invalid contracts, fresh output storage, noncontiguous data, exact dtype and gradients where required. Use seed20261113 for synthetic scale tests. Run public and hidden cases through the shared local bubblewrap worker; runtime limits above are actual shared limits, not a performance ranking. OCI image digest remains pending for this local environment.

## Visualization and theory

The original theory includes essential display math, defined symbols, a static shape/timeline table, a worked calculation, robot failure modes and questions. Tables render without an animation or motion preference. No external figures or paper code are copied.

## Provenance

Primary source: https://arxiv.org/abs/2303.03378; Sections3–4: continuous sensor embeddings. Numerical fixtures are original and CC0-1.0. Passing this component does not reproduce published training results.
