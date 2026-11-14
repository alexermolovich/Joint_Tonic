---
{
  "schema_version": 1,
  "problem_id": "openvla-fuse-visual-streams",
  "content_version": "1.0.0",
  "status": "implemented",
  "title": "Fuse Two Visual Feature Streams Safely",
  "summary": "Fuse Two Visual Feature Streams Safely",
  "type": "component",
  "difficulty": "medium",
  "estimated_minutes": 40,
  "domains": [
    "VLA and embodied robot learning"
  ],
  "topics": [
    "2024-openvla",
    "policy-interface"
  ],
  "paper_ids": [
    "2024-openvla"
  ],
  "paper_sections": [
    "Sections 3.1 and 3.4: fused DINOv2 and SigLIP representations"
  ],
  "track_ids": [],
  "prerequisite_problem_ids": [
    "palm-e-project-sensor-features"
  ],
  "runtime": {
    "language": "python",
    "python": "3.12.3",
    "runtime_id": "python-3.12.3-numpy-2.2.4-torch-2.6.0-cpu-bwrap-v2",
    "image_digest": null,
    "image_status": "pending OCI build",
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
  "entrypoint": "solution.fuse_visual_features",
  "physical_contract": {
    "frames": [
      "Aligned patch feature coordinates; no spatial transform"
    ],
    "units": {
      "features": "dimensionless",
      "weights": "dimensionless"
    },
    "axes": "first(B,N,C1), second(B,N,C2), projection(C1+C2,E), bias(E), masks(B,N), fused(B,N,E)",
    "timestamp_assumptions": "Same aligned observation context is supplied; no internal clock",
    "batching": "Nonempty bounded batch; exact axis bounds in statement"
  },
  "grading": {
    "mode": "numerical",
    "seed": 20261113,
    "rtol": 1e-06,
    "atol": 1e-07,
    "exact_fields": [
      "Boolean validity mask"
    ],
    "public_case_families": [
      "two-worked-examples",
      "minimal-shape"
    ],
    "hidden_case_families": [
      "typed-boundary-validation",
      "noncontiguous-inputs",
      "independent-oracle",
      "storage-and-nonmutation",
      "gradients-where-required",
      "realistic-scale"
    ]
  },
  "fixtures": {
    "source": "Original synthetic inputs",
    "license": "CC0-1.0",
    "version_or_hash": "synthetic-v1-seed-20261113"
  },
  "provenance": {
    "authoring_notes": "Original bounded contract; source mechanisms and teaching deviations are explicit. No full trained policy or paper benchmark is reproduced.",
    "primary_urls": [
      "https://arxiv.org/html/2406.09246v3"
    ],
    "paper_card": "research/papers/vla-embodied/2024-openvla.md",
    "manifest": "research/manifests/vla-embodied.md"
  },
  "owners": [
    "vla_implementation"
  ],
  "reviewers": [
    "curriculum_continuation"
  ]
}
---

# Fuse Two Visual Feature Streams Safely

Implement fuse_visual_features(first, second, projection, bias, first_valid, second_valid), returning (fused, valid).

The four floating inputs are finite CPU torch.float32 or torch.float64 tensors with one common dtype and absolute entries <= 100. first is (B,N,C1), second is (B,N,C2), projection is (C1+C2,E), and bias is (E,). Require 1 <= B <= 32, 1 <= N <= 512, 1 <= C1,C2 <= 256 and 1 <= E <= 512. Each input tensor and the fused output contain at most 1,000,000 entries. first_valid and second_valid are CPU torch.bool tensors (B,N). Noncontiguous inputs are supported.

The caller guarantees that the two token rows at each (b,n) correspond to the same image patch, with identical spatial ordering and synchronized observation context. This function cannot infer correspondence from equal shapes. Features and projected coordinates are dimensionless; no metric frame transformation or timestamp alignment occurs.

Set valid = first_valid & second_valid. Concatenate first then second along feature width, apply the supplied affine projection, and set every invalid output row to exact zeros after adding bias. Thus fused = where(valid[...,None], concat(first,second,-1) @ projection + bias, 0). Return fused(B,N,E) with the input floating dtype/device and valid(B,N) as bool. All-false validity is permitted; validate every floating entry even in masked-out rows.

Preserve input values and return independent storage. Gradients must reach both feature tensors, projection and bias wherever they require gradients; invalid rows contribute zero gradients. Do not detach floating inputs. Non-tensor inputs raise TypeError; all dtype/device/shape/bound violations raise ValueError.

This is an original affine fusion exercise motivated by OpenVLA's feature concatenation and projection. It does not implement the trained visual encoders, nonlinear full projector, image preprocessing, token resampling, missing-camera imputation or the language model. The intersection-mask rule is a declared teaching policy.

## Implementation and evaluator plan

Review the complete mathematical and physical contract before implementation. Use independent scalar/tensor oracles, both worked examples, stated invalid-input behavior, aliasing checks and analytical gradients where applicable. Verify the reference through actual isolated Run and Submit and reject the starter before publication. No new runtime dependency or model checkpoint is needed.
