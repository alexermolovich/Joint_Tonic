---
{
  "schema_version": 1,
  "problem_id": "rt2-mix-web-robot-batches",
  "content_version": "1.0.0",
  "status": "drafted",
  "title": "Mix Web and Robot Batches at a Target Ratio",
  "summary": "Co-training mixes robot examples with web supervision, but a ratio alone does not specify finite batch rounding or what happens when a source is small.",
  "type": "component",
  "difficulty": "medium",
  "estimated_minutes": 30,
  "domains": [
    "robot-learning"
  ],
  "topics": [
    "2023-rt-2",
    "policy-components"
  ],
  "paper_ids": [
    "2023-rt-2"
  ],
  "paper_sections": [
    "Original deterministic co-training mixer inspired by RT-2. Half-up rounding, source order and cycling are teaching rules rather than the paper\u2019s training sampler."
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
  "entrypoint": "solution.mix_web_robot",
  "physical_contract": {
    "frames": [
      "Declared normalized action/feature coordinates; no implicit frame conversion"
    ],
    "units": {
      "values": "Dataset IDs/source labels and ratios are dimensionless; no common raw action space is assumed."
    },
    "axes": "web_ids(W), robot_ids(R) -> source(B), ids(B)",
    "timestamp_assumptions": "This is one training batch assembly; per-source sequence order remains external.",
    "batching": "web_ids(W), robot_ids(R) -> source(B), ids(B)"
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
    "authoring_notes": "Original deterministic co-training mixer inspired by RT-2. Half-up rounding, source order and cycling are teaching rules rather than the paper\u2019s training sampler.",
    "primary_urls": [
      "https://arxiv.org/abs/2307.15818"
    ],
    "paper_card": "research/papers/vla-embodied/2023-rt-2.md",
    "manifest": "research/manifests/vla-embodied.md"
  },
  "owners": [
    "research_curator"
  ],
  "reviewers": []
}
---

# Mix Web and Robot Batches at a Target Ratio

## Contract

`mix_web_robot(web_ids,robot_ids,robot_fraction,batch_size)` receives nonnegative integer ID vectors(W,),(R,), lengths0..10000; scalar robot_fraction in[0,1]; integer batch_size1..4096. Set robot quota=floor(batch_size*robot_fraction+0.5), web quota=remainder. Any source with positive quota must be nonempty. Return dict source:int64(B,) where1robot/0web and ids:int64(B,). Emit all robot rows then all web rows, cycling each source’s IDs from index0 with replacement. Duplicate IDs allowed; no random draw or shuffling.

Unless a tighter bound is stated below, numeric array-like inputs must have real integer/floating dtype after `np.asarray`, be finite with absolute values <=1e6 and at most1,000,000 entries. Boolean, complex, string and object numeric arrays are invalid; Boolean masks must have Boolean dtype. Integer arrays/scalars exclude booleans. All invalid inputs raise ValueError. Return new arrays, preserve inputs, and compute floating outputs in float64 on CPU. No automatic differentiation is required.

## Source scope

Original deterministic co-training mixer inspired by RT-2. Half-up rounding, source order and cycling are teaching rules rather than the paper’s training sampler.

## Evaluation plan

Two numerical examples, independent invariants and documented invalid cases; deterministic seed20261114. Numeric rtol1e-7/atol1e-9, exact integer/Boolean fields. Synthetic CC0 fixtures. Run public and hidden cases in the isolated worker; reject empty starter and a mechanism-specific mutant.

## Visualization

Original trace table in Theory with a textual alternative; no motion required.
