---
{
  "schema_version": 1,
  "problem_id": "diffusion-conditional-temporal-denoiser",
  "content_version": "1.0.0",
  "status": "implemented",
  "title": "Build a Conditional Action Denoiser",
  "type": "function",
  "difficulty": "hard",
  "paper_ids": [
    "2023-diffusion-policy"
  ],
  "paper_sections": [
    "Bounded mechanism identified in the original theory note"
  ],
  "track_ids": [
    "2023-diffusion-policy"
  ],
  "prerequisite_problem_ids": [
    "diffusion-observation-window-encoder"
  ],
  "entrypoint": "solution.conditional_denoiser",
  "owners": [
    "root"
  ],
  "reviewers": [
    "research_curator"
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
  "physical_contract": {
    "frames": [
      "Fixed normalized action/observation channel conventions"
    ],
    "units": {
      "actions_context_noise": "dimensionless",
      "timesteps": "normalized diffusion level, not seconds"
    },
    "axes": "B batches,H horizon,A actions,C hidden channels,F context features",
    "timestamp_assumptions": "Fixed supplied batch; cameras/observations are aligned by caller. No clock inference, state history or real-time guarantee.",
    "batching": "Only explicitly declared dimensions; masks preserve original ordering."
  },
  "grading": {
    "mode": "numerical",
    "seed": 20261114,
    "rtol": 1e-06,
    "atol": 1e-07,
    "public_case_families": [
      "two-worked-examples"
    ],
    "hidden_case_families": [
      "independent-mechanism-oracle",
      "boundary-and-invalid-input",
      "maximum-advertised-dimensions",
      "input-preservation-and-output-aliasing"
    ],
    "performance_class": "none",
    "evaluator_sha256": "e24b3ccac19094c5cdc35735c88beadc99ee207a1794e5c57036d71bfb76e919"
  },
  "fixtures": {
    "source": "original synthetic examples in examples.md; future generated fixtures use declared seed",
    "license": "CC0-1.0",
    "version_or_hash": "synthetic-v1-seed-20261113"
  },
  "provenance": {
    "authoring_notes": "Original bounded teaching component; no source code or figures copied. Systems diagnostics are teaching contracts, not paper benchmark claims.",
    "primary_urls": [
      "https://arxiv.org/abs/2303.04137"
    ],
    "implementation_urls": []
  }
}
---

# Build a Conditional Action Denoiser

An action denoiser uses both a noisy action window and observation context. A temporal kernel mixes nearby actions; a conditioning vector changes each hidden channel's scale and offset. This original one-block network isolates that mechanism without pretending to train a full policy.

```python
def conditional_denoiser(actions, timesteps, context, kernel, context_weight, time_weight, head, bias):
    ...
```

## Function contract

Inputs: `actions: float64(B, H, A)`, `timesteps: float64(B,)` in `[0, 1]`, `context: float64(B, F)`, `kernel: float64(3, A, C)`, `context_weight: float64(F, 2*C)`, `time_weight: float64(2, 2*C)`, `head: float64(C, A)` and `bias: float64(A,)`. Bounds: `1<=B<=8`, `1<=H<=32`, `1<=A<=8`, `1<=C, F<=16`. All parameter/context/action entries have absolute value at most 100.

Actions are normalized dimensionless noised action channels. Timestep is diffusion level, not robot time. Zero-pad the horizon one step on each side. Compute temporal cross-correlation `conv[b, t, c] = sum_{k, a} padded_actions[b, t+k, a]*kernel[k, a, c]`; do not reverse the kernel.

Embed time as `[sin(pi*t), cos(pi*t)]`. Compute FiLM values `context @ context_weight + time_embedding @ time_weight`; split the first C channels as gamma and the last C as beta. Apply `hidden = SiLU((1+gamma[:, None,:])*conv + beta[:, None,:])`, then `hidden @ head + bias`. SiLU must remain finite at all allowed inputs.

Return fresh `float64(B, H, A)` predicted noise. This is an original one-block conditional temporal denoiser, not a full U-Net, trained policy, reverse sampler or safety filter.

## Validation and execution

All arrays must be NumPy arrays with the exact stated `float64`, `int64` or `bool` dtype. Validate every entry, including masked entries: numeric inputs must be finite with absolute value at most 1e6, and each input array may contain at most 2,000,000 entries. More specific bounds below take precedence. Built-in Python `int`/`float` scalars exclude `bool`; sizes require built-in `int`. All type, shape and range violations raise `ValueError`. Noncontiguous CPU arrays are supported. Preserve every input and return fresh arrays with no shared storage between inputs or outputs. No implicit batching is accepted.

Runtime: Python 3.12.3 and NumPy 2.2.4; 18 seconds wall time, 10 seconds CPU, 4096 MiB address space and 64 KiB output. Numerical comparisons use `rtol=1e-6, atol=1e-7`. Fixtures are original synthetic CC0-1.0 data; no model checkpoint or external dataset is downloaded.

## Worked examples

**Example 1.** Actions `[[[0]]]`, all-zero kernel and conditioning/time weights, head `[[1]]`, bias `[2]`: output predicted noise is `[[[2]]]`.

**Example 2.** Use action value `1`, center kernel value `1`, other kernel entries zero, head `1`, bias `0` and zero conditioning/time weights. Output is `[[[1/(1+exp(-1))]]]`, approximately `[[[0.73105858]]]`; do not add the original action.

## Source and scope

Original bounded component based on [2023-diffusion-policy](https://arxiv.org/abs/2303.04137). Temporal conditioning helps an action sequence reflect current observations. Kernel reversal changes which neighbor influences a command; confusing diffusion level with wall-clock time changes the model input. Predicted noise is not an executable robot command and needs a separate sampler and safety checks.

## Evaluation plan

Two worked public examples; independent hidden mechanism oracle; documented invalid inputs; boundary and scale checks; input preservation and output storage independence. Reference Run/Submit, starter rejection, mechanism-mutant rejection and peer review precede publication.
