---
{
  "schema_version": 1,
  "problem_id": "diffusion-ddpm-action-sampler",
  "content_version": "1.0.0",
  "status": "drafted",
  "title": "Sample an Action Trajectory with DDPM Steps",
  "summary": "Reverse diffusion removes predicted corruption one level at a time.",
  "type": "component",
  "difficulty": "medium",
  "estimated_minutes": 30,
  "domains": [
    "robot-learning"
  ],
  "topics": [
    "2023-diffusion-policy",
    "policy-components"
  ],
  "paper_ids": [
    "2023-diffusion-policy"
  ],
  "paper_sections": [
    "Original DDPM posterior-variance teaching sampler motivated by Diffusion Policy. A real policy recomputes its conditional denoiser on each current state; this task supplies those outputs to isolate scheduler arithmetic."
  ],
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
  "entrypoint": "solution.sample_ddpm_actions",
  "physical_contract": {
    "frames": [
      "Declared normalized action/feature coordinates; no implicit frame conversion"
    ],
    "units": {
      "values": "Actions are normalized dimensionless controller channels; diffusion coefficients and noise are dimensionless."
    },
    "axes": "initial(H,D), predictions/noise(K,H,D), betas(K) -> reverse trace(K+1,H,D)",
    "timestamp_assumptions": "Diffusion indices are noise levels, not robot control timestamps; each H row denotes a future action slot.",
    "batching": "initial(H,D), predictions/noise(K,H,D), betas(K) -> reverse trace(K+1,H,D)"
  },
  "grading": {
    "mode": "numerical",
    "seed": 20261114,
    "rtol": 1e-07,
    "atol": 1e-09,
    "public_case_families": [
      "two-worked-examples"
    ],
    "hidden_case_families": [
      "documented-boundaries",
      "invalid-inputs",
      "independent-invariants"
    ],
    "performance_class": "cpu"
  },
  "fixtures": {
    "source": "original-synthetic",
    "license": "CC0-1.0",
    "version_or_hash": "synthetic-v1-seed-20261113"
  },
  "provenance": {
    "authoring_notes": "Original DDPM posterior-variance teaching sampler motivated by Diffusion Policy. A real policy recomputes its conditional denoiser on each current state; this task supplies those outputs to isolate scheduler arithmetic.",
    "primary_urls": [
      "https://arxiv.org/abs/2303.04137"
    ],
    "paper_card": "research/papers/vla-embodied/2023-diffusion-policy.md",
    "manifest": "research/manifests/vla-embodied.md"
  },
  "owners": [
    "research_curator"
  ],
  "reviewers": []
}
---

# Sample an Action Trajectory with DDPM Steps

## Contract

`sample_ddpm_actions(initial,predicted_noise,betas,step_noise)` receives initial(H,D),1<=H,D<=64; predicted_noise and step_noise:(K,H,D),1<=K<=64, abs all three tensors<=100; betas(K,) each in [0.0001,0.1]. Arrays at index k correspond to forward diffusion level k+1. Return float64 trajectory(K+1,H,D): first initial noisy sample, then states after reverse levels K,...,1. Let alpha=1-beta, abar=cumprod(alpha), previous_abar=1 at k=0 else abar[k-1], posterior_var=beta[k]*(1-previous_abar)/(1-abar[k]). At reverse index k compute mean=(x-beta[k]/sqrt(1-abar[k])*predicted_noise[k])/sqrt(alpha[k]); next=mean+sqrt(posterior_var)*step_noise[k] for k>0; at k=0 return mean without noise. Supplied predictions represent already evaluated denoiser outputs, not a callable model. No clipping or extra random draw.

Unless a tighter bound is stated below, numeric array-like inputs must have real integer/floating dtype after `np.asarray`, be finite with absolute values <=1e6 and at most1,000,000 entries. Boolean, complex, string and object numeric arrays are invalid; Boolean masks must have Boolean dtype. Integer arrays/scalars exclude booleans. All invalid inputs raise ValueError. Return new arrays, preserve inputs, and compute floating outputs in float64 on CPU. No automatic differentiation is required.

## Source scope

Original DDPM posterior-variance teaching sampler motivated by Diffusion Policy. A real policy recomputes its conditional denoiser on each current state; this task supplies those outputs to isolate scheduler arithmetic.

## Evaluation plan

Two numerical examples, independent invariants and documented invalid cases; deterministic seed20261114. Numeric rtol1e-7/atol1e-9, exact integer/Boolean fields. Synthetic CC0 fixtures. Run public and hidden cases in the isolated worker; reject empty starter and a mechanism-specific mutant.

## Visualization

Original trace table in Theory with a textual alternative; no motion required.
