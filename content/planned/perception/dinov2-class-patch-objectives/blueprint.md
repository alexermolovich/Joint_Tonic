---
{
  "schema_version": 1,
  "problem_id": "dinov2-class-patch-objectives",
  "content_version": "0.1.0",
  "status": "reviewed",
  "title": "Combine Class-Token and Masked-Patch Objectives",
  "summary": "Combine Class-Token and Masked-Patch Objectives",
  "type": "function",
  "difficulty": "hard",
  "estimated_minutes": 40,
  "domains": [
    "perception"
  ],
  "topics": [
    "dinov2",
    "paper-component"
  ],
  "paper_ids": [
    "2023-dinov2"
  ],
  "paper_sections": [
    "Mechanism and explicit teaching conventions in theory.md"
  ],
  "track_ids": [],
  "prerequisite_problem_ids": [
    "dinov2-center-sharpen"
  ],
  "runtime": {
    "language": "python",
    "python": "3.12.3",
    "runtime_id": "python-3.12.3-numpy-2.2.4-torch-2.6.0-cpu-bwrap-v2",
    "image_digest": null,
    "image_status": "pending OCI build; baseline worker exists",
    "dependencies": {
      "torch": "2.6.0+cpu",
      "numpy": "2.2.4"
    },
    "limits": {
      "wall_seconds": 18,
      "cpu_seconds": 10,
      "memory_mb": 4096,
      "output_kb": 64
    }
  },
  "entrypoint": "solution.class_patch_loss",
  "physical_contract": {
    "frames": [
      "Explicit caller grid/view frames in statement"
    ],
    "units": {
      "features": "dimensionless; BEV geometry in metres where stated"
    },
    "axes": "student_class(B,V,K), teacher_class(B,2,K), student_patch/teacher_patch(B,P,K), mask(B,P); scalar output.",
    "timestamp_assumptions": "One explicitly paired batch; no internal clock.",
    "batching": "student_class(B,V,K), teacher_class(B,2,K), student_patch/teacher_patch(B,P,K), mask(B,P); scalar output."
  },
  "grading": {
    "mode": "numerical",
    "seed": 20261113,
    "rtol": 0.000001,
    "atol": 1e-7,
    "public_case_families": [
      "worked-examples",
      "minimal-shape"
    ],
    "hidden_case_families": [
      "validation",
      "edge-policy",
      "layout",
      "preservation",
      "independent-oracle",
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
    "authoring_notes": "Original bounded teaching task; variants explicitly distinguished from full paper systems.",
    "primary_urls": [
      "https://arxiv.org/abs/2304.07193"
    ],
    "implementation_urls": [],
    "paper_card": "research/papers/vision-vlm-3d/2023-dinov2.md",
    "manifest": "research/manifests/vision-vlm-3d.md"
  },
  "owners": [
    "perception_implementation"
  ],
  "reviewers": ["vla_implementation"]
}
---

# Combine Class-Token and Masked-Patch Objectives

## Contract

Implement class_patch_loss(student_class, teacher_class, student_patch, teacher_patch, mask, temperature, class_weight, patch_weight).

The four value tensors are CPU torch.float32 or torch.float64 with a common dtype. Shapes are student_class(B,V,K), teacher_class(B,2,K), student_patch(B,P,K), teacher_patch(B,P,K), with 1<=B<=32, 2<=V<=8, 2<=K<=2048, 0<=P<=1024 and at most 1,000,000 elements per tensor. mask is CPU torch.bool (B,P). Noncontiguous tensors are valid.

All entries are finite. Student logits have absolute value <=100. Each teacher row is nonnegative and sums to one with rtol=0, atol=1e-6; teachers are already prepared probability targets, not logits. Validate all teacher rows, including unmasked patches. Empty P is allowed.

temperature, class_weight and patch_weight are built-in non-bool int/float; temperature is finite in [0.01,10], weights finite in [0,10]. The first two student views correspond to teacher views 0 and 1; any remaining student views are local crops.

Compute class cross-entropy for each teacher view t in {0,1} against every student view v except v=t, and average over B*2*(V-1) pairs. Compute patch cross-entropy only for mask=True entries in the single supplied aligned patch-view batch, averaging over all selected entries across B and P. If no patches are selected, patch loss is a differentiable zero connected to student_patch. Return class_weight*class_loss + patch_weight*patch_loss as a new zero-dimensional tensor with the input dtype/device.

Student probabilities use log_softmax(student_logits/temperature). Detach teacher targets: gradients flow to both student tensors, never to either teacher. In a grad-enabled call, the output supports backward when a student requires gradients, including empty/all-false masks and zero weights. Preserve input values and masks; no mutation or aliasing.

Non-tensor inputs among the five tensors raise TypeError. All other violations raise ValueError. Scores and losses are dimensionless, views refer to the same underlying image, and patch targets are already aligned to student positions. This specified two-term reduction isolates DINO/iBOT mechanisms; crop generation, Sinkhorn/centering, teacher EMA, KoLeo, distributed reduction, and the complete DINOv2 training recipe are outside the task.

## Implementation and proof

Independent contract review precedes implementation. Test the examples, typed validation, boundary policies, input preservation and realistic scale with independent oracles. Publish only after isolated Run/Submit and starter-negative checks. Review risk: Verify cross-view pair normalization, mixed float32/float64 rejection, teacher stop-gradient, selected-patch global mean versus per-image mean, and empty/all-false patch graph behavior.

## Resources and provenance

https://arxiv.org/abs/2304.07193. Actual shared local worker caps: 18 s wall, 10 s CPU, 4096 MiB address space, 64 KiB output. OCI image digest is pending; no image or reproducibility claim is invented. Original examples and future fixtures use CC0-1.0.

