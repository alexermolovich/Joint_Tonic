---
{
  "schema_version": 1,
  "problem_id": "nerf-tiny-field-training",
  "content_version": "1.0.0",
  "status": "implemented",
  "title": "Fit a Tiny Coordinate-Feature Radiance Field",
  "type": "function",
  "difficulty": "hard",
  "paper_ids": [
    "2020-nerf"
  ],
  "track_ids": [
    "2020-nerf"
  ],
  "prerequisite_problem_ids": [
    "nerf-fourier-features",
    "nerf-render-color-depth",
    "nerf-rendered-color-gradients"
  ],
  "entrypoint": "solution.train_tiny_field",
  "owners": [
    "root"
  ],
  "reviewers": [
    "research_curator (contract, code, cases and theory)"
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
      "Ordered samples along normalized rays in one caller-defined scene frame"
    ],
    "units": {
      "features_parameters": "dimensionless",
      "density": "inverse meters with fixed1/m scale",
      "intervals": "meters",
      "colors": "linear RGB",
      "loss": "mean squared RGB error"
    },
    "axes": "B/R train/evaluation rays,S ordered samples,F frozen coordinate features; shared F,4 weight and 4 bias.",
    "timestamp_assumptions": "One static scene; training/evaluation rows supplied separately. No time integration or view dependence.",
    "batching": "Only explicitly declared dimensions; masks preserve original ordering."
  },
  "grading": {
    "mode": "numerical",
    "seed": 20261114,
    "rtol": 1e-06,
    "atol": 1e-07,
    "public_case_families": [
      "zero-error-field",
      "one-analytic-SGD-step"
    ],
    "hidden_case_families": [
      "independent-scalar-renderer",
      "finite-difference-gradient",
      "global-clipping",
      "held-out-isolation",
      "boundary-and-invalid-contract"
    ],
    "performance_class": "none",
    "evaluator_sha256": "8d453bffaee5cbbc30150e7bb65c18a3025609ee65e974ab2db30e2b60a78672"
  },
  "fixtures": {
    "source": "original synthetic examples in examples.md; future generated fixtures use declared seed",
    "license": "CC0-1.0",
    "version_or_hash": "synthetic-v1-seed-20261113"
  },
  "provenance": {
    "authoring_notes": "Original bounded teaching component; no source code or figures copied. Systems diagnostics are teaching contracts, not paper benchmark claims.",
    "primary_urls": [
      "https://arxiv.org/abs/2003.08934"
    ],
    "implementation_urls": []
  }
}
---

# Fit a Tiny Coordinate-Feature Radiance Field

Train one shared density/color function by differentiating image error through volume rendering. Use a deliberately small affine field so the rendering, gradients, optimizer and held-out evaluation remain inspectable.

```python
def train_tiny_field(train_features, train_intervals, train_targets,
                     eval_features, eval_intervals, eval_targets,
                     background, initial_weight, initial_bias,
                     steps, learning_rate):
    ...
```

## Inputs and physical contract

All arrays are CPU NumPy `float64` arrays with finite entries. Training and evaluation rays describe one static scene, using the same fixed coordinate-feature convention. Samples are ordered along normalized rays. Features are supplied; no camera projection or positional encoding occurs inside this function.

| Input | Shape | Bounds and units |
|---|---|---|
| `train_features` | `(B,S,F)` | Dimensionless coordinate features, absolute value ≤ 2 |
| `eval_features` | `(R,S,F)` | Same feature basis and bounds |
| `train_intervals`, `eval_intervals` | `(B,S)`, `(R,S)` | `[0.01,2]` meters along each ray |
| `train_targets`, `eval_targets` | `(B,3)`, `(R,3)` | Linear RGB in `[0,1]` |
| `background` | `(3,)` | Shared linear RGB in `[0,1]` |
| `initial_weight` | `(F,4)` | Dimensionless, absolute value ≤ 2 |
| `initial_bias` | `(4,)` | Dimensionless, absolute value ≤ 2 |

Require `1<=B,R<=16`, `1<=S<=32`, `1<=F<=16`. `steps` is a built-in integer in `[0,64]`. `learning_rate` is a built-in integer or float in `[1e-6,0.1]`. Boolean scalars are invalid. All type, shape and range violations raise `ValueError`, including invalid evaluation inputs when `steps=0`.

Preserve all inputs, support noncontiguous arrays, and return independent arrays. Coordinate features must not contain privileged target colors. No timestamps, view-direction inputs or physical actuation are involved.

## Field, rendering and training

1. Compute `raw = features @ weight + bias`. The first channel becomes density through stable softplus; the last three become RGB through stable sigmoid. The fixed density scale is one inverse meter. Use `max(z,0)+log1p(exp(-abs(z)))` for softplus and a stable sigmoid branch.
2. For each ray, compute opacity `1-exp(-density*interval)`, exclusive transmittance from earlier optical thicknesses, and color weights `transmittance*opacity`. Sum weighted colors and add the surviving terminal transmittance times background.
3. Training loss is mean squared RGB error over all `B*3` entries. Record it before the first update and after each update.
4. Analytically differentiate that loss through volume rendering, including downstream colors and background, then through field activations into the shared weight and bias. Compute one global L2 norm across **all** weight and bias gradient entries. Divide both gradients by `max(1,norm)` and apply a simultaneous SGD update with the given learning rate. Record the raw, unclipped norm.
5. After exactly `steps` updates, render evaluation rays and report their mean squared RGB error. Evaluation features, intervals and targets must not influence training, gradient clipping, stopping or model selection.

There is no random sampling, early stopping, optimizer state, deep MLP or full-scene reconstruction. Loss need not decrease monotonically for every allowed input. Theory derives the analytic gradient and the exact normalization.

## Return value

Return exactly these dictionary entries:

| Key | Type/shape |
|---|---|
| `weight` | `float64(F,4)` |
| `bias` | `float64(4,)` |
| `train_loss` | `float64(steps+1,)` |
| `gradient_norm` | `float64(steps,)` |
| `eval_rgb` | `float64(R,3)` |
| `eval_mse` | Python `float` |

## Worked example 1: zero error

Use `B=R=S=F=1`, feature value `1`, interval `1`, all-zero initial weight/bias, and background/training/evaluation target `[0.5,0.5,0.5]`. With `steps=3`, `learning_rate=0.1`, return unchanged zero parameters, `train_loss=[0,0,0,0]`, `gradient_norm=[0,0,0]`, `eval_rgb=[[0.5,0.5,0.5]]` and `eval_mse=0.0`.

## Worked example 2: one update

Use the same dimensions, features, intervals and zero parameters, but black targets/background. Set `steps=1`, `learning_rate=0.1`. Initial density is `log(2)`, color is `[0.5,0.5,0.5]`, rendered RGB is `[0.25,0.25,0.25]`, and loss is `1/16`.

The returned weight row and bias are both `[-1/160,-1/480,-1/480,-1/480]`. The single raw gradient norm is `sqrt(1/96)`, so clipping does not activate. Define

$$v=(1-\exp(-\operatorname{softplus}(-1/80)))\operatorname{sigmoid}(-1/240).$$

Return `train_loss=[1/16,v*v]`, `eval_rgb=[[v,v,v]]` and `eval_mse=v*v`. This checks the shared weight/bias updates and the post-update evaluation.

## Runtime and scope

Python 3.12.3, NumPy 2.2.4; 18 seconds wall time, 10 seconds CPU, 4096 MiB address space, 64 KiB output. Numerical tolerances: `rtol=1e-6`, `atol=1e-7`. All fixtures are original synthetic CC0-1.0 data.

Based on selected mechanisms from [NeRF](https://arxiv.org/abs/2003.08934). The supplied-feature, affine, view-independent field and clipped SGD are explicit teaching substitutions. This exercise does not reproduce the paper's full architecture, training recipe or benchmark results.
