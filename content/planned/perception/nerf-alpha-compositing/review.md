# Author and independent review: Compute Transmittance and Alpha Compositing Weights

Status: **reviewed for implementation**. Author: `ui_issue_scout`. Independent reviewer: `paper_explanations`. This approves the draft contract and source explanation; executable publication still requires the checks below.

## Author checks

- [x] Read AGENTS.md, SPEC.md, CURRICULUM.md section 2, blueprint template, vision manifest, and paired paper card.
- [x] Preserved the exact curriculum title; selected a stable draft slug without publishing metadata.
- [x] Compared the selected mechanism with primary sources and curator caveats.
- [x] Wrote original theory, contract, diagrams/text alternatives, examples, and progressive hints.
- [x] Explicitly distinguished this component from full-paper reproduction.
- [x] Author arithmetic/shape checks passed for both examples on NumPy 2.2.4 / PyTorch 2.6.0+cpu; also checked CLIP derivative, ViT round trips, point-order invariance, NeRF mass, and sequential EMA where applicable.
- [x] Shared structural/KaTeX validation passed (six packages, 107 expressions): `node scripts/validate-drafts.mjs content/planned/perception/nerf-alpha-compositing`.

## Risks and remaining work

The draft's numerical bounds and API are original teaching choices, not claims about all implementations of the paper. Confirm that these choices fit the intended difficulty during independent review. The author check is not an evaluator suite. The runtime image has not been built for this exercise; `image_digest: null` is intentional. No real camera dataset, model weights, or copied paper illustration is included.

- [x] Independent mathematical/source/contract review.
- [x] Independent worked-example and pedagogy review.
- [ ] Implement starter, reference solution, public and hidden tests.
- [ ] Verify dependency installation, sandbox limits, and reference behavior.
- [ ] Render theory/diagrams accessibly in the application before publication.

## Review findings and disposition

Independent review checked the complete statement, theory, examples, hints, and blueprint against the paired source card and primary mechanism. Worked examples were recalculated independently. See [review findings](../review-findings.md) for findings and disposition. Runtime budgets in this draft are proposed targets; published packages must declare the actual baseline worker caps and pinned runtime. No learner evaluator or application publication is approved by this prose review.
