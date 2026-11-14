---
{
  "schema_version": 1,
  "problem_id": "nerf-rendered-color-gradients",
  "content_version": "1.0.0",
  "status": "implemented",
  "title": "Differentiate Rendered Color on a Small Synthetic Field",
  "type": "function",
  "difficulty": "hard",
  "paper_ids": [
    "2020-nerf"
  ],
  "paper_sections": [
    "Bounded mechanism identified in the original theory note"
  ],
  "track_ids": [
    "2020-nerf"
  ],
  "prerequisite_problem_ids": [
    "nerf-hierarchical-depth-sampling"
  ],
  "entrypoint": "solution.render_color_gradients",
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
      "Ordered samples along normalized rays in one caller-defined scene frame"
    ],
    "units": {
      "density": "inverse meters",
      "intervals": "meters",
      "colors": "linear RGB",
      "density_gradient": "meters times squared RGB units",
      "loss": "squared RGB units"
    },
    "axes": "B rays,S ordered samples,3 RGB channels",
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
    "evaluator_sha256": "4db07252b3fc757734d9f84042d327b25a1d671bb9186de7f8d019bcab60adf9"
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

# Differentiate Rendered Color on a Small Synthetic Field

Increasing one sample's density makes its own color more visible and hides everything behind it. The gradient must account for both effects, including background. Differentiating only the local opacity misses the occlusion mechanism that trains a radiance field.

```python
def render_color_gradients(density, intervals, colors, background, target):
    ...
```

## Function contract

Inputs: `density: float64(B, S)`, `intervals: float64(B, S)`, `colors: float64(B, S, 3)`, `background: float64(3,)` and `target: float64(B, 3)`. Bounds: `1<=B<=32`, `1<=S<=128`. Density is in `[0, 1000]` inverse meters; intervals are in `[1e-9, 10]` meters along normalized rays. All RGB entries lie in `[0, 1]` and are linear RGB.

For ordered samples, compute opacity `alpha_i = 1-exp(-density_i*interval_i)`, exclusive transmittance `T_i = exp(-sum of earlier optical thicknesses)`, weight `w_i = T_i*alpha_i` and terminal transmittance over all intervals. Render the weighted RGB sum plus terminal transmittance times background. Loss is mean squared error over all B*3 RGB channels.

Return `rgb: float64(B, 3)`, `loss: Python float`, `density_gradient: float64(B, S)` and `color_gradient: float64(B, S, 3)`. Gradients are analytic derivatives of this scalar loss. Every density affects its own color, all downstream samples and background. No interval/background/target derivative, field MLP or autograd package is required. Full opacity may consistently underflow transmittance to zero.

## Validation and execution

All arrays must be NumPy arrays with the exact stated `float64`, `int64` or `bool` dtype. Validate every entry, including masked entries: numeric inputs must be finite with absolute value at most 1e6, and each input array may contain at most 2,000,000 entries. More specific bounds below take precedence. Built-in Python `int`/`float` scalars exclude `bool`; sizes require built-in `int`. All type, shape and range violations raise `ValueError`. Noncontiguous CPU arrays are supported. Preserve every input and return fresh arrays with no shared storage between inputs or outputs. No implicit batching is accepted.

Runtime: Python 3.12.3 and NumPy 2.2.4; 18 seconds wall time, 10 seconds CPU, 4096 MiB address space and 64 KiB output. Numerical comparisons use `rtol=1e-6, atol=1e-7`. Fixtures are original synthetic CC0-1.0 data; no model checkpoint or external dataset is downloaded.

## Worked examples

**Example 1.** One ray/sample has density `0`, interval `1`, red sample color `[1, 0, 0]`, and black target/background. Output RGB is `[0, 0, 0]`, loss `0`, and both gradient arrays are zero.

**Example 2.** Replace density by `log(2)`. Output RGB is `[.5, 0, 0]`, loss `1/12`, density gradient `1/6`, and color gradient `[1/6, 0, 0]`, with original batch/sample dimensions retained.

## Source and scope

Original bounded component based on [2020-nerf](https://arxiv.org/abs/2003.08934). Differentiable rendering connects image errors to a robot's learned scene representation. Ignoring background attenuation gives wrong gradients even for an empty-looking ray. A low RGB loss does not alone establish correct metric geometry or collision safety.

## Evaluation plan

Two worked public examples; independent hidden mechanism oracle; documented invalid inputs; boundary and scale checks; input preservation and output storage independence. Reference Run/Submit, starter rejection, mechanism-mutant rejection and peer review precede publication.
