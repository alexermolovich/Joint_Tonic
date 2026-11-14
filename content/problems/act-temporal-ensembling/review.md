# Author review: Blend Overlapping Action Chunks with Temporal Ensembling

Status: **reviewed contract; implementation checks remain separate**.

## Proof of success

Both numerical examples and the masked-candidate variant must match; each nonzero weight must correspond to an eligible prediction for the requested tick. A gapped-start case must distinguish rank from elapsed-age weighting.

## Source verification and decisions

ACT SectionIV.A explicitly assignsw0 to the oldest action prediction and usesexp(-m*i), with smaller m incorporating new observations faster. This draft preserves that direction. It makes validity and irregular chunk-start availability explicit without claiming these extensions are the paper’s complete deployment loop.

## Author checks

- [x] Paired paper card read before primary-source verification.
- [x] Complete deterministic contract and two worked examples written.
- [x] Original explanation, equations, static diagram, text fallback, and questions written.
- [x] Numerical examples and equation rendering checked after authoring. Author arithmetic: 12 examples across the batch, including masked gradients and exact matrices. Shared validator: 6 packages, 132 LaTeX expressions. This is not executable evaluator approval.
- [ ] Independent subject-matter reviewer approved the source interpretation.
- [ ] Independent evaluator reviewer approved errors, bounds, tolerances, and gradient/aliasing rules.
- [ ] Executable starter/reference/tests and isolated runtime validated.

## Question answer key

1. Older predictions:rank0 has weight1 and newer ranks decay more strongly.
2. Offset3, provided it exists within H and valid[c,3] isTrue.
3. Componentwise averaging can violate unit-quaternion constraints or choose the wrong path across angle wraparound; those representations require different geometry-aware operations.

## Risks for the next reviewer

Independent reviewer must check weight direction, target-time alignment, rank compression, and exclusion of non-Euclidean action channels. Existing ACT implementations sometimes filter zero arrays as availability; this draft deliberately uses an explicit validity mask instead.

The original contract review is retained above. This implementation directory now contains application metadata, reference code and an evaluator.

## Independent review — code_issue_scout

Read all six files and ACT card/primary paper, sectionIV.A page5. Confirmed oldest-first exponential rank in the paper and same-target-time aggregation. Independently checked weights4/7,2/7,1/7 and action24/7 plus the zero-valued eligible candidate example. Reviewed compressed rank, masking, gapped ticks, no-eligible errors, float64 accumulation and exclusion of non-Euclidean action channels. No blocking contract issue.

Approved for implementation. Use the actual CPython3.12.3 baseline and enforced worker caps; draft approval does not certify an unpublished evaluator or OCI image.


## Runtime verification — implementation worker

Reference passed 7 unique public/hidden checks in the actual Linux bubblewrap worker, using both public Run and complete Submit. Python3.12.3, NumPy2.2.4 and PyTorch2.6.0CPU where required; shared18s wall/10s CPU/4096MiB/64KiB caps. The checks cover the published contract, not full-paper reproduction. The evaluator source SHA-256 is pinned in blueprint.md; no OCI digest is claimed for the local environment. Static theory tables and original LaTeX are present; no source figure or paper code was copied.
