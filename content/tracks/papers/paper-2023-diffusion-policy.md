---
{
  "schema_version": 1,
  "generated_by": "scripts/generate-paper-tracks.ts",
  "slug": "paper-2023-diffusion-policy",
  "paper_id": "2023-diffusion-policy",
  "title": "Diffusion Policy: Visuomotor Policy Learning via Action Diffusion",
  "status": "planned",
  "primary_url": "https://arxiv.org/abs/2303.04137",
  "source_cards": [
    "research/papers/vla-embodied/2023-diffusion-policy.md"
  ],
  "paper_aliases": [],
  "category": "vla-embodied",
  "topics": [
    "diffusion policy",
    "visuomotor control",
    "receding horizon",
    "multimodal actions"
  ],
  "runnable_problem_slugs": [
    "diffusion-action-noising",
    "diffusion-conditional-noise-loss",
    "diffusion-ddpm-action-sampler",
    "diffusion-receding-horizon-window",
    "diffusion-denoising-budget"
  ],
  "proposed_component_count": 2,
  "source_flow_node_count": 6,
  "source_flow_nodes": [
    {
      "card": "2023-diffusion-policy",
      "node": "observation-context"
    },
    {
      "card": "2023-diffusion-policy",
      "node": "forward-noising"
    },
    {
      "card": "2023-diffusion-policy",
      "node": "conditional-denoiser"
    },
    {
      "card": "2023-diffusion-policy",
      "node": "training-loss"
    },
    {
      "card": "2023-diffusion-policy",
      "node": "reverse-sampling"
    },
    {
      "card": "2023-diffusion-policy",
      "node": "receding-horizon"
    }
  ],
  "integration_status": "proposed",
  "assessment_status": "proposed"
}
---

# Diffusion Policy: Visuomotor Policy Learning via Action Diffusion — implementation track

## Orientation and scope

A robot often has several reasonable ways to act from the same observation. Averaging those demonstrations can produce a command that follows none of them. Diffusion Policy represents a conditional distribution over **whole action sequences**: it learns to remove noise from demonstrated sequences, then uses the learned denoiser to generate a coherent future chunk. Images and robot state condition the prediction; a receding-horizon controller executes a short prefix and replans from fresh observations.

The paper studies convolutional and transformer denoisers, observation conditioning, and temporal execution. The runnable Joint Tonic component, [Add Noise to an Action Sequence](/problems/diffusion-action-noising), isolates the forward process used to build training examples. It does not train a policy, implement a reverse sampler, or establish closed-loop task success.

The implementation path follows **Encode observations → Noise a demonstration → Predict the noise → Fit the denoiser → Denoise an action chunk → Execute and replan**. Work through the original explanation and the atomic tasks below before composing the proposed integration. Published exercises are small, independently graded components; this plan is not a completed or full-paper reproduction.

[Primary source](https://arxiv.org/abs/2303.04137) · [Paper explanation and graph](/projects/2023-diffusion-policy) · [All paper tracks](../../PAPER_TRACKS.md)

Source cards: [2023-diffusion-policy](../../../research/papers/vla-embodied/2023-diffusion-policy.md).

**Available now:** 5 paper-associated runnable components; 0 supporting runnable components. **Proposed:** 2 distinct component ideas, plus integration and assessment. A planned title can be a reviewed blueprint or an unreviewed idea; its presence is not a publication promise.

## Prerequisites and diagnostic

Read the input contracts and locally defined mathematics in the source explanation. Before starting, trace one small input through **Encode observations** and identify the shapes, masks, units, coordinate frames and time conventions that apply. This is a robotics diagnostic, not a general Python or mathematics course.

- **Supporting prerequisite:** [Add Noise to an Action Sequence](/problems/diffusion-action-noising). Its own contract remains authoritative; it does not implement the entire paper.
- **Supporting prerequisite:** [Build Sliding Action Chunks with Padding Masks](/problems/act-sliding-action-chunks). Its own contract remains authoritative; it does not implement the entire paper.

## Ordered mechanisms and component tasks

The sequence below is a learning order. The explicit connections retain branching, conditioning and feedback; adjacent entries are not assumed to have interchangeable tensor interfaces.

### 1. Encode observations

<!-- source-flow: 2023-diffusion-policy#observation-context -->

Images and robot state become conditioning features shared across the denoising steps.

[Study the mechanism and math](/projects/2023-diffusion-policy#paper-section-observation-conditioning).

- **Proposed component, not runnable:** Encode Synchronized Observations for an Action Denoiser.

**Step evidence:** retain a small input/output trace and the invariant described in the linked explanation. Before implementing a proposed task, write and review its blueprint with explicit shapes, units, frames, examples, tolerances and failure behavior.

### 2. Noise a demonstration

<!-- source-flow: 2023-diffusion-policy#forward-noising -->

Gather one cumulative schedule value per batch item and broadcast over the action horizon.

[Study the mechanism and math](/projects/2023-diffusion-policy#paper-section-forward-noising).

- **Runnable paper-associated component:** [Add Noise to an Action Sequence](/problems/diffusion-action-noising). Gather one cumulative signal coefficient per batch item and broadcast over horizon/action axes; mix clean actions and supplied noise with square-root weights.

**Step evidence:** retain a small input/output trace and the invariant described in the linked explanation. Before implementing a proposed task, write and review its blueprint with explicit shapes, units, frames, examples, tolerances and failure behavior.

### 3. Predict the noise

<!-- source-flow: 2023-diffusion-policy#conditional-denoiser -->

A conditional network receives a noisy action chunk, diffusion index, and observation features.

[Study the mechanism and math](/projects/2023-diffusion-policy#paper-section-conditional-denoiser).

- **Proposed component, not runnable:** Build a Conditional Action Denoiser.

**Step evidence:** retain a small input/output trace and the invariant described in the linked explanation. Before implementing a proposed task, write and review its blueprint with explicit shapes, units, frames, examples, tolerances and failure behavior.

### 4. Fit the denoiser

<!-- source-flow: 2023-diffusion-policy#training-loss -->

Training compares predicted noise with the noise used to corrupt the demonstration.

[Study the mechanism and math](/projects/2023-diffusion-policy#paper-section-training-objective).

- **Runnable paper-associated component:** [Compute a Conditional Noise-Prediction Loss](/problems/diffusion-conditional-noise-loss). Reduce predicted-versus-supplied diffusion noise errors over exactly the valid action scalars while preserving training gradients.

**Step evidence:** retain a small input/output trace and the invariant described in the linked explanation. Before implementing a proposed task, write and review its blueprint with explicit shapes, units, frames, examples, tolerances and failure behavior.

### 5. Denoise an action chunk

<!-- source-flow: 2023-diffusion-policy#reverse-sampling -->

Inference starts from Gaussian noise and applies the trained network through the reverse schedule.

[Study the mechanism and math](/projects/2023-diffusion-policy#paper-section-reverse-sampling).

- **Runnable paper-associated component:** [Sample an Action Trajectory with DDPM Steps](/problems/diffusion-ddpm-action-sampler). Reverse diffusion removes predicted corruption one level at a time.

**Step evidence:** retain a small input/output trace and the invariant described in the linked explanation. Before implementing a proposed task, write and review its blueprint with explicit shapes, units, frames, examples, tolerances and failure behavior.

### 6. Execute and replan

<!-- source-flow: 2023-diffusion-policy#receding-horizon -->

Execute a short valid prefix, capture new observations, and plan the next overlapping chunk.

[Study the mechanism and math](/projects/2023-diffusion-policy#paper-section-receding-horizon-execution).

- **Runnable paper-associated component:** [Execute a Receding-Horizon Action Window](/problems/diffusion-receding-horizon-window). Extract the controller-supported prefix of a predicted future trajectory after a specified alignment offset.
- **Runnable paper-associated component:** [Budget Denoising Steps Against Control Frequency](/problems/diffusion-denoising-budget). More denoising iterations can improve a sampler while missing a robot deadline.

**Step evidence:** retain a small input/output trace and the invariant described in the linked explanation. Before implementing a proposed task, write and review its blueprint with explicit shapes, units, frames, examples, tolerances and failure behavior.

| From | Signal or dependency | To |
|---|---|---|
| Encode observations | context | Predict the noise |
| Noise a demonstration | noisy actions | Predict the noise |
| Predict the noise | predicted noise | Fit the denoiser |
| Noise a demonstration | target noise | Fit the denoiser |
| Predict the noise | trained network | Denoise an action chunk |
| Denoise an action chunk | action chunk | Execute and replan |

## Integration exercise

**Proposed exercise — not runnable yet.** Build a short normalized action sequence, fixed Gaussian noise and a declared variance schedule. Compose forward noising, conditional noise-prediction loss and the receding-horizon execution window. A future sampler step must receive a reviewed DDPM update contract before it is integrated; a supplied analytic denoiser can support a deterministic toy rollout.

The integration boundary is selected observation-to-action mechanisms with supplied features and deterministic model callbacks; a learned robot policy and real-world success claims are outside scope. Treat any stubbed learned stage as a named fixture, never as measured model capability. Author original synthetic data and record its generation rules; external datasets or assets need a separate provenance and license review.

Deliver an executable fixture generator, the component wiring, a compact expected-output trace and a report of the remaining differences from [the paper](/projects/2023-diffusion-policy). Proposed pieces must pass blueprint review and isolated evaluation before this integration becomes an available exercise.

## Evaluation and failure analysis

**Proposed assessment — not runnable yet.** Report target/loss correctness and executed action indices before any trajectory score. Compare step count with model-call budget, and inject an observation-window offset to expose a control-time alignment error.

Use one clean baseline and a separately recorded fault case: remove a modality, alter one action scale, or delay an observation; identify the exact component that rejects or masks the inconsistent input. Identify the affected stage and report its intermediate evidence. Do not average away the failing case.

Before grading, define an independent oracle, exact-versus-tolerant comparisons, allowed dtypes/devices, empty/minimal cases, invalid-input behavior and resource bounds. Compare failure detection and mathematical correctness separately from timing. A synthetic result establishes only the declared component contract; paper benchmark scores and physical safety require their own protocol.

## Reproducibility deliverable

**Proposed final artifact:** an original implementation/model card for **Diffusion Policy: Visuomotor Policy Learning via Action Diffusion** containing the source revision, exercised and stubbed stages, and an explicit list of omitted paper experiments.

Record action bounds and units, embodiment channel mapping, control period, observation/action horizon, normalization statistics and model-call schedule. Pin problem/content versions, code revision, Python/dependency versions, evaluator identity, deterministic seeds and fixture hashes. Include the baseline/fault report and runtime observations. If any component updates parameters, record the update count and trainable state; otherwise state that no model was trained.

Package the fixture and expected trace with a machine-readable manifest. Replaying the same manifest must recover the same evidence within declared tolerances. Record limitations and the next unimplemented mechanism; completion of this proposal must not be labeled full-paper reproduction. Research PDFs remain local reference inputs, with canonical sources linked rather than redistributed.
