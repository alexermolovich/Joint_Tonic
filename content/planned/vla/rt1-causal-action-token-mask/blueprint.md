---
schema_version: 1
problem_id: "rt1-causal-action-token-mask"
content_version: "0.1.0"
status: "reviewed"
title: "Build a Causal Action-Token Mask"
summary: "Construct RT-1’s reference causal mask while preventing direct action-slot attention to action slots."
type: "component"
difficulty: "medium"
estimated_minutes: 35
domains: ["VLA and embodied robot learning"]
topics: ["rt1","causal-attention","action-token-layout"]
paper_ids: ["2022-rt-1"]
paper_sections: ["RT-1 Section5.1: Loss and causal masking","TransformerNetwork._generate_masks and _assemble_input_token_sequence at commit 4569641b8111f3f402c32d8e24becd2a6e952ecc"]
track_ids: []
prerequisite_problem_ids: []
runtime: {"language":"python","python":"3.10.11","image_digest":null,"publication_note":"Proposed local CPU runtime; exact dependency versions match the inspected authoring environment. No sandbox image has been built or validated for this draft. Pin its OCI digest before publishing.","dependencies":{"numpy":"2.2.4"},"limits":{"wall_seconds":10,"cpu_seconds":8,"memory_mb":512,"output_kb":64}}
entrypoint: "solution.rt1_attention_mask"
physical_contract: {"frames":["Not applicable: token positions, not spatial coordinates"],"units":{"positions":"integer token indices","mask":"boolean allowed-attention relation"},"axes":"Rows=query positions; columns=key positions. Each timestep stores V visual slots then A action slots.","timestamp_assumptions":"Timesteps are ordered oldest to newest at a fixed caller-controlled period; no timestamp values enter the mask.","batching":"One(L,L) mask shared by examples with the same fixed layout; no padding or batch dimension in this component."}
grading: {"mode":"exact","seed":20261113,"rtol":0,"atol":0,"public_case_families":["one timestep with two visual and two action slots","two timesteps with one visual and one action slot"],"hidden_case_families":["multi-timestep layouts","query-key orientation","action diagonal exclusion","visual access to prior action placeholders","integer and size validation"],"performance_class":"none; resource budget only, no latency ranking"}
fixtures: {"source":"Independently authored synthetic inputs in examples.md; future evaluator fixtures must use this documented contract.","license":"CC0-1.0","version_or_hash":"vla-draft-fixtures-0.1.0"}
provenance: {"authoring_notes":"This exercise reproduces the structural mask in the pinned official RT-1 implementation using a NumPy boolean output. It omits token embedding, shifted prediction readouts, sequence padding, and the transformer. The reference implementation zeroes input action embeddings; this mask alone is not a license to insert teacher-forced action labels.","primary_urls":["https://arxiv.org/abs/2212.06817"],"implementation_urls":["https://github.com/google-research/robotics_transformer/blob/4569641b8111f3f402c32d8e24becd2a6e952ecc/transformer_network.py#L161-L196","https://github.com/google-research/robotics_transformer/blob/4569641b8111f3f402c32d8e24becd2a6e952ecc/transformer_network.py#L585-L600"]}
owners: ["Joint Tonic content"]
reviewers: ["code_issue_scout"]
review_status: {"author":"draft authored; verification recorded in review.md","independent_subject_matter":"approved by code_issue_scout","independent_evaluator":"contract approved by code_issue_scout; implementation pending"}
---

# Build a Causal Action-Token Mask

## Learning objective

Construct RT-1’s reference causal mask while preventing direct action-slot attention to action slots.

## Paper connection and scope

This exercise reproduces the structural mask in the pinned official RT-1 implementation using a NumPy boolean output. It omits token embedding, shifted prediction readouts, sequence padding, and the transformer. The reference implementation zeroes input action embeddings; this mask alone is not a license to insert teacher-forced action labels.

Verified source locations: RT-1 Section5.1: Loss and causal masking; TransformerNetwork._generate_masks and _assemble_input_token_sequence at commit 4569641b8111f3f402c32d8e24becd2a6e952ecc. [Primary paper](https://arxiv.org/abs/2212.06817).

## Contract

The complete normative function, inputs, outputs, errors, and shape/physical conventions are in [statement.md](statement.md). This blueprint proposes that contract for review; it does not publish it.

Return True=allowed, rows=query and columns=key. The exact predicate is causal AND NOT(action-query AND action-key). The sequence layout is fixed and unpadded; built-in integer parameters must produce1<=L<=1024. Action labels are not input content for this isolated mask.

## Learner prompt draft

Implement the reference structural attention relation and explain why an ordinary lower-triangular matrix is insufficient for the action rows.

## Worked examples

### Case1: one visual block followed by action slots

```text
steps=1, visual_tokens=2, action_tokens=2
slot labels: [V0.0,V0.1,A0.0,A0.1]
output (1=True, 0=False):
[[1,0,0,0],
 [1,1,0,0],
 [1,1,0,0],
 [1,1,0,0]]
```

The second visual query sees the first visual key and itself. Both action queries see both visual keys, but neither sees action keys.

### Case2: a later visual query can see an earlier placeholder

```text
steps=2, visual_tokens=1, action_tokens=1
slot labels: [V0,A0,V1,A1]
output (1=True, 0=False):
[[1,0,0,0],
 [1,0,0,0],
 [1,1,1,0],
 [1,0,1,0]]
```

The row for V1 includes A0. The row for A1 excludes A0 and A1. This is intentional reference behavior; replacing every action-key column with zeros would produce a different mask.

## Starter-code plan

A future `starter.py` will import numpy as np, provide the signature in statement.md, and leave only the named function body for the learner. No executable starter or evaluator is registered by this draft.

## Reference-solution plan

Validate built-in integer arguments before computing/allocating L. Construct token-type indicators from modulo positions and combine a lower-triangular boolean relation with the complement of the action/action outer relation. OutputO(L²), workO(L²), auxiliaryO(L) excluding broadcasted output operations.

## Evaluator plan

| Case family | Visibility | Required evidence |
|---|---|---|
| Two stated layouts | public | Exact boolean matrices and query/key orientation |
| Mixed V,A,T sizes | hidden | Compare each cell with the documented predicate |
| Diagonal and row visibility | hidden | Visual diagonals true; action diagonals false; visual rows retain causal action placeholders |
| Boundary and invalid integers | public/hidden | Reject bool/non-int, zero groups, negative values, and L>1024 |

Use seed 20261113 for generated fixtures. Exact shape, dtype, mask, exception class, and immutability checks accompany numerical tolerances in frontmatter. Generate fixtures only inside documented bounds. Dependency/image startup failures are platform errors, not wrong answers. The resource budget is proposed and must be calibrated in the isolated worker before publication.

## Visualization plan

The original Mermaid/shape diagram and its text alternative are written in [theory.md](theory.md). They are static and require no animation or reduced-motion exception. A future interactive adapter may consume only bounded numerical arrays; no learner HTML or simulation process is needed for this component.

## Theory and hints

[Theory](theory.md) provides intuition, defined equations, a worked calculation, the visual, robot failure modes, and three understanding questions. [Hints](hints.md) reveals the mechanism progressively; [review notes](review.md) keeps the question answer key away from the learner prompt.

## MLOps/reproducibility extension

Record T,V,A, flattening order, action-input convention, and prediction readout positions with a model checkpoint. A mask change is a model-contract change; compare training and inference construction rather than relying on equal tensor dimensions.

## Editorial checklist

- [x] Draft paper ID, canonical source, scope, and fixture license are recorded.
- [x] Shapes, dtypes, units, frames, time, errors, and batch axes are specified.
- [x] Statement, theory, hints, examples, diagram, and questions are independently authored.
- [x] Exact candidate dependency versions are recorded; OCI image remains explicitly pending.
- [ ] Independent subject-matter review approved.
- [ ] Independent evaluator review approved.
- [ ] Starter, reference implementation, public tests, and hidden tests implemented.
- [ ] Reference passes public/hidden cases in a pinned clean sandbox.
- [ ] Published renderer accessibility and narrow-screen presentation reviewed.
