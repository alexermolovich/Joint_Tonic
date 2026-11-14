---
{
  "schema_version": 1,
  "problem_id": "act-cvae-loss",
  "content_version": "0.1.0",
  "status": "reviewed",
  "title": "Compute a Masked CVAE Reconstruction and KL Loss",
  "summary": "Isolate ACT's L1 reconstruction plus diagonal-Gaussian KL objective.",
  "type": "component",
  "difficulty": "medium",
  "estimated_minutes": 35,
  "domains": [
    "VLA and embodied robot learning"
  ],
  "topics": [
    "2023-aloha-act",
    "policy-components"
  ],
  "paper_ids": [
    "2023-aloha-act"
  ],
  "paper_sections": [
    "Section IV-B–C: CVAE modeling and L1 reconstruction"
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
  "entrypoint": "solution.cvae_loss",
  "physical_contract": {
    "frames": [
      "As specified in the typed contract; no implicit frame conversion"
    ],
    "units": {
      "actions": "caller-declared normalized Euclidean action channels",
      "embeddings": "dimensionless",
      "time": "fixed control ticks, not flow time"
    },
    "axes": "B=batch,H=future control ticks,D=normalized Euclidean action channels,Z=latent coordinates",
    "timestamp_assumptions": "One aligned observation per batch item; temporal calibration is upstream.",
    "batching": "prediction/target(B,H,D), valid(B,H), mean/log_variance(B,Z), three scalar outputs"
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
    "authoring_notes": "Isolate ACT's L1 reconstruction plus diagonal-Gaussian KL objective. The global valid-scalar reconstruction mean and batch-mean latent sum are explicit teaching reductions. No encoder, latent sampling, transformer, or training run is reproduced.",
    "primary_urls": [
      "https://arxiv.org/abs/2304.13705"
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

# Compute a Masked CVAE Reconstruction and KL Loss

## Paper connection and scope

Isolate ACT's L1 reconstruction plus diagonal-Gaussian KL objective. The global valid-scalar reconstruction mean and batch-mean latent sum are explicit teaching reductions. No encoder, latent sampling, transformer, or training run is reproduced.

## Contract

Implement cvae_loss(prediction, target, valid, mean, log_variance, beta), returning a tuple (total, reconstruction, kl) of fresh zero-dimensional tensors.

prediction and target are finite CPU float32/float64 tensors of identical shape (B,H,D), dtype, and absolute value <=1e6. valid is a CPU bool tensor (B,H) with at least one True globally; individual items may contain no valid actions. mean and log_variance are CPU tensors of matching floating dtype and identical shape (B,Z), with finite values: abs(mean)<=1000 and -20<=log_variance<=20. All dimensions are positive; B<=64,H<=256,D<=64,Z<=256; each floating tensor has <=2,000,000 elements. beta is a built-in non-bool int/float, finite and in [0,100].

Reconstruction is the sum of absolute prediction-target residuals at valid timesteps, divided by D*valid.sum(). KL is 0.5 times the batch mean of the latent-dimension sum mean**2+exp(log_variance)-1-log_variance. Include every batch item's KL even if its action mask is empty. total=reconstruction+beta*kl. log_variance is log(sigma**2), not log(sigma).

Keep dtype/device and autograd through all four floating tensors; do not detach target or return Python numbers. At an exact zero residual, use the standard absolute-value subgradient zero. Accept noncontiguous tensors; preserve inputs. Validate masked padding too. All-false global validity is an error even if beta>0.

Raise TypeError for non-tensor tensor arguments or non-built-in numeric beta. Raise ValueError for every shape/dtype/device/bounds/finiteness violation. Errors are normalized Euclidean action coordinates, with fixed horizon control interval chosen upstream; latent dimensions have no robot frame or physical units. No circular/quaternion reconstruction or safety guarantee.

## Reference and evaluator plan

Implement the declared tensor/array operations without external models or assets. Validate each stated boundary before computation. Test the public examples, masks/reduction axes, invalid contracts, fresh output storage, noncontiguous data, exact dtype and gradients where required. Use seed20261113 for synthetic scale tests. Run public and hidden cases through the shared local bubblewrap worker; runtime limits above are actual shared limits, not a performance ranking. OCI image digest remains pending for this local environment.

## Visualization and theory

The original theory includes essential display math, defined symbols, a static shape/timeline table, a worked calculation, robot failure modes and questions. Tables render without an animation or motion preference. No external figures or paper code are copied.

## Provenance

Primary source: https://arxiv.org/abs/2304.13705; Section IV-B: Modeling human data. Numerical fixtures are original and CC0-1.0. Passing this component does not reproduce published training results.
