# Paper explanation and component-map status

All **157 paper cards** have original explanations, defined mathematics, execution flows and component guidance. The library contains **156 distinct primary papers**; Open X-Embodiment retains two existing topic cards. The application now contains **274 runnable problems**, including all 190 named curriculum exercises.

These are explanations of selected mechanisms, not exhaustive derivations or full-paper reproductions. A linked exercise may implement a component or teach a supporting prerequisite. Each flow node distinguishes runnable exercises from proposed ideas. See [the complete component map](FLOW_PROBLEM_MAP.md), [paper tracks](../content/PAPER_TRACKS.md), and [curriculum completion](../content/CURRICULUM_COMPLETION.md).

## Verification — 2026-11-14

- Content validation: 274 problem packages and 157 paper cards passed.
- Paper-card KaTeX syntax: 334 display equations and 1,212 inline expressions parsed without errors.
- All 853 in-article problem links resolve to published slugs.
- All 156 generated tracks passed validation across 1,877 checked links. Their 475 explained stages and 319 graph connections have complete component coverage: 400 runnable exercise associations and 369 explicitly proposed associations. Associations are not unique-problem counts.
- All 157 PDF/card pairs passed PDF signature, recorded byte/page count, and SHA-256 checks and opened with Poppler. The artifacts contain 3,411 pages. This is parser and integrity verification, not a visual review of every page. See the [artifact manifest](manifests/library-integrity-2026-11-14.md).
- This completion pass filled 19 display-math gaps and refreshed perception, VLA and MLOps explanations and exercise links. Operational formalizations and simplified teaching components are identified explicitly.
- Source-fidelity review clarified GR00T flow-matching conventions and latent-action supervision, pi0 attention blocks, and simplified OFA kernel extraction.

Syntax and link checks do not independently validate every derivation. Selected additions received source review and numerical-example checks; published exercises received the separate peer-review and isolated-evaluator workflow. Existing PDFs remain local authoring references, not redistributable product assets.

## Remaining scope

The named curriculum exercises are complete. Additional proposed graph components and full-paper experiments remain in progress and are labeled accordingly. Four bounded cross-paper capstones and two bounded paper integrations are runnable; they do not complete every proposed integration. Completing a component does not establish reproduction of the paper's published benchmark results.

The [grouped paper inventory](../content/PAPER_TRACKS.md) links every canonical track. The [flow map](FLOW_PROBLEM_MAP.md) links its explanations and runnable or proposed components. Provenance and licensing records remain in `manifests/`, with each original summary beside its PDF in `papers/`.
