---
schema_version: 1
problem_id: "rt1-compact-visual-tokens"
content_version: "0.1.0"
status: "reviewed"
title: "Select Compact Visual Tokens with Learned Attention"
summary: "Turn supplied learned spatial logits into normalized attention maps and compress visual features without mixing examples."
type: "component"
difficulty: "medium"
estimated_minutes: 40
domains: ["VLA and embodied robot learning"]
topics: ["rt1","visual-token-compression","masked-attention"]
paper_ids: ["2022-rt-1"]
paper_sections: ["RT-1 Section5.1: Image and language tokenization; TokenLearner","Official TokenLearnerModule.call at commit 4569641b8111f3f402c32d8e24becd2a6e952ecc"]
track_ids: []
prerequisite_problem_ids: []
runtime: {"language":"python","python":"3.10.11","image_digest":null,"publication_note":"Proposed local CPU runtime; exact dependency versions match the inspected authoring environment. No sandbox image has been built or validated for this draft. Pin its OCI digest before publishing.","dependencies":{"numpy":"2.2.4","torch":"2.6.0+cpu"},"limits":{"wall_seconds":10,"cpu_seconds":8,"memory_mb":2048,"output_kb":64}}
entrypoint: "solution.compact_visual_tokens"
physical_contract: {"frames":["Image-grid feature locations; no metric coordinate transform"],"units":{"features":"dimensionless learned features","logits":"dimensionless log scores","weights":"dimensionless normalized weights"},"axes":"B=batch, N=flattened row-major image locations, C=feature channels, K=output tokens","timestamp_assumptions":"Each batch item is one synchronized image feature map; independent frames may be folded into B by the caller.","batching":"features(B,N,C), logits(B,K,N), optional valid(B,N); independent normalization for every (b,k)."}
grading: {"mode":"numerical","seed":20261113,"rtol":0.000001,"atol":1e-7,"public_case_families":["two weighted tokens with a masked location","two independent single-location images"],"hidden_case_families":["stable logits","mixed masks","noncontiguous tensors","gradients","all-masked image rejection","dtype/device/shape/value validation"],"performance_class":"none; resource budget only, no latency ranking"}
fixtures: {"source":"Independently authored synthetic inputs in examples.md; future evaluator fixtures must use this documented contract.","license":"CC0-1.0","version_or_hash":"vla-draft-fixtures-0.1.0"}
provenance: {"authoring_notes":"This exercise isolates the spatial softmax and weighted aggregation in RT-1’s TokenLearner. Logits are supplied; learning their LayerNorm/MLP generator, image encoding, language conditioning, and policy training are out of scope. The optional padding mask is an original batching extension.","primary_urls":["https://arxiv.org/abs/2212.06817"],"implementation_urls":["https://github.com/google-research/robotics_transformer/blob/4569641b8111f3f402c32d8e24becd2a6e952ecc/tokenizers/token_learner.py#L103-L117"]}
owners: ["Joint Tonic content"]
reviewers: ["code_issue_scout"]
review_status: {"author":"draft authored; verification recorded in review.md","independent_subject_matter":"approved by code_issue_scout","independent_evaluator":"contract approved by code_issue_scout; implementation pending"}
---

# Select Compact Visual Tokens with Learned Attention

## Learning objective

Turn supplied learned spatial logits into normalized attention maps and compress visual features without mixing examples.

## Paper connection and scope

This exercise isolates the spatial softmax and weighted aggregation in RT-1’s TokenLearner. Logits are supplied; learning their LayerNorm/MLP generator, image encoding, language conditioning, and policy training are out of scope. The optional padding mask is an original batching extension.

Verified source locations: RT-1 Section5.1: Image and language tokenization; TokenLearner; Official TokenLearnerModule.call at commit 4569641b8111f3f402c32d8e24becd2a6e952ecc. [Primary paper](https://arxiv.org/abs/2212.06817).

## Contract

The complete normative function, inputs, outputs, errors, and shape/physical conventions are in [statement.md](statement.md). This blueprint proposes that contract for review; it does not publish it.

The supplied-logit aggregation returns both compact tokens and spatial weights. Masked positions have exactly zero weight; each image must retain a location. CPU float32/float64, stable normalization, noncontiguous inputs, no mutation/storage aliasing, and gradients through both floating inputs are required.

## Learner prompt draft

Implement the weighted visual-token compression in statement.md and expose its attention weights so the compression can be inspected.

## Worked examples

### Case1: two attention maps and one padded location

```text
features = [[[1,0], [3,2], [9,9]]]
logits = [[[0,ln(3),99], [0,0,99]]]
valid = [[True,True,False]]

tokens  = [[[2.5,1.5], [2,1]]]
weights = [[[0.25,0.75,0], [0.5,0.5,0]]]
```

Construct `ln(3)` in the chosen float dtype. The first token is `0.25*[1,0]+0.75*[3,2]`; the large masked logit contributes nothing. The second averages the two valid locations.

### Case2: independent single-location images

```text
features = [[[2]], [[-4]]]
logits = [[[1000]], [[-1000]]]
valid = None

tokens = [[[2]], [[-4]]]
weights = [[[1]], [[1]]]
```

Each batch item normalizes its own spatial axis. The large difference between images’ logits is irrelevant.

## Starter-code plan

A future `starter.py` will import torch, provide the signature in statement.md, and leave only the named function body for the learner. No executable starter or evaluator is registered by this draft.

## Reference-solution plan

Validate the documented contracts; replace invalid logits with negative infinity for normalization only; apply a stable spatial softmax; batch-multiply weights by features. Return fresh outputs. Compute workO(BKNC); storeO(BKN+BKC). Autograd must remain connected through normalization and aggregation.

## Evaluator plan

| Case family | Visibility | Required evidence |
|---|---|---|
| Two supplied examples | public | Both arrays, shape, dtype, and exact masked zeros |
| Large common logit shifts | hidden | Outputs unchanged and finite within declared tolerance |
| Noncontiguous features/logits | hidden | Same numerical outputs as contiguous copies |
| Gradient finite differences in float64 | hidden | Feature/logit gradients agree on nondegenerate valid entries; masked influence is zero |
| Invalid row and tensor contracts | public/hidden | Documented TypeError versus ValueError; no input mutation |

Use seed 20261113 for generated fixtures. Exact shape, dtype, mask, exception class, and immutability checks accompany numerical tolerances in frontmatter. Generate fixtures only inside documented bounds. Dependency/image startup failures are platform errors, not wrong answers. The resource budget is proposed and must be calibrated in the isolated worker before publication.

## Visualization plan

The original Mermaid/shape diagram and its text alternative are written in [theory.md](theory.md). They are static and require no animation or reduced-motion exception. A future interactive adapter may consume only bounded numerical arrays; no learner HTML or simulation process is needed for this component.

## Theory and hints

[Theory](theory.md) provides intuition, defined equations, a worked calculation, the visual, robot failure modes, and three understanding questions. [Hints](hints.md) reveals the mechanism progressively; [review notes](review.md) keeps the question answer key away from the learner prompt.

## MLOps/reproducibility extension

Version the image-grid flattening order, upstream logit network, validity-mask convention, and token count with the policy checkpoint. Compare latency and task coverage when changing K; a smaller token budget may remove rare manipulation cues.

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
