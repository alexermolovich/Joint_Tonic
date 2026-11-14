# Curriculum completion — 2026-11-14

All **190 named problems** in CURRICULUM.md sections 1–4 are implemented. The local application exposes **193 runnable problem packages**, including three supporting exercises. No named entry remains queued or in draft. The full topic tree and package links are in [AUTHORING_STATUS.md](AUTHORING_STATUS.md).

This completion pass added 115 packages to the existing 78:

| Authoring lane | New problems |
|---|---:|
| Geometry, kinematics, timing, estimation and control | 26 |
| Sensor numerics and episode evaluation | 6 |
| Vision, VLM and 3D perception | 24 |
| VLA and embodied learning | 35 |
| Robotics MLOps, deployment and sim-to-real | 24 |

Every added package contains a versioned blueprint and metadata, explicit input/output and physical contracts, at least two worked examples, original theory with rendered mathematics and a purposeful visual/shape trace, hints, starter code, reference solution, public/hidden cases, and review notes. The exercise scopes are bounded components, not claims of full-paper benchmark reproduction.

## Verification

- All 115 new references passed public Run and full Submit in the actual pinned Linux bubblewrap worker. Each starter and a plausible mechanism mutation was rejected. Authors and independent reviewers recorded fixes in package review notes.
- A final trusted-reference integration sweep passed **1,150 checks across all 193 packages**. This arithmetic sweep supplements the isolated batch checks; it is not a replacement for learner-code isolation.
- Content validation passed for 193 packages and 157 paper cards. Four content-validator regression tests passed.
- All 1,430 mathematical expressions across the 193 problem packages parsed with KaTeX without errors.
- `npm run build` succeeded, including route generation.
- A new Kalman Theory page rendered its equations and visual table in the browser without client errors. Theory and editor remained side by side at 1440 px; at 390 px the page had no horizontal overflow. New Kalman and iterative-IK routes returned HTTP 200.
- All 156 generated paper tracks passed validation: 1,778 checked links, 474 explained stages, and 318 graph connections. The flow map contains 318 runnable exercise associations and 450 explicitly proposed associations across papers.
- All 157 local PDF/card pairs passed signature, SHA-256, byte-count and page-count checks and opened with Poppler; 156 distinct sources contain 3,411 pages. See [artifact integrity](../research/manifests/library-integrity-2026-11-14.md).

## Research explanations and limits

The collected paper cards contain original explanations, defined mathematics, execution graphs, primary-source links and component/prerequisite links. This pass filled 19 display-math gaps, refreshed core perception/VLA/MLOps associations, and corrected source-convention distinctions such as GR00T flow matching, pi0 attention blocks, and simplified OFA kernel extraction. [Explanation status](../research/EXPLANATION_STATUS.md) records the final audit.

The four cross-paper capstone assessments, paper-specific integration experiments and additional proposed graph ideas are still future work. They are not counted among the 190 completed named exercises. Completing the available components does not reproduce a paper's headline training results.

Code execution and MuJoCo remain local services. Production sandbox deployment, a built OCI evaluator image, hosted progress storage and other platform backlog items are outside this curriculum pass. The local worker's trust boundary and remaining production requirements are documented in [the worker README](../apps/worker/README.md).

## Reproduce the focused checks

From the repository root:

```text
npm run validate
npm run test:content
node --experimental-strip-types scripts/validate-paper-tracks.ts
npm run validate:paper-links
npm run build
```

In the configured Linux/WSL Python environment, use `apps/worker/check_references.py` for trusted reference arithmetic or add `--sandbox` and selected problem slugs for isolated Run/Submit checks. Never execute learner submissions through the trusted-reference tool.
