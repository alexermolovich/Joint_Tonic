# Joint Tonic agent instructions

## Mission

Build **Joint Tonic**, a physical-AI learning and evaluation platform where engineers implement robotics and embodied-ML ideas as small, testable coding problems and longer research-paper tracks.

The product may use Tensor Tonic as an interaction reference, but it must have its own name, visual identity, copy, problem statements, solutions, datasets, and code. Do not scrape, reproduce, or closely paraphrase proprietary content.

## Source of truth

1. Read `SPEC.md` before making product or architecture decisions.
2. Read `MVP_10.md` before implementing the first vertical slice. It is the current ten-problem commitment.
3. Read `CURRICULUM.md` before adding, naming, grouping, or implementing any other problem or track. Keep the tree synchronized with reviewed blueprint decisions.
4. Read `research/README.md` and the relevant file under `research/manifests/` before authoring a paper-derived track.
5. Treat the checked-in PDFs under `research/papers/` as reference material, not redistributable product assets. The manifests record provenance and licenses/status.
6. Read the same-basename Markdown paper card beside a PDF before opening the PDF. Cards are the retrieval-optimized agent context and the seed for future problem blueprints.
7. If implementation and specification disagree, call out the discrepancy. Update the specification in the same change only when the requested work intentionally changes product behavior.

## Product priorities

In order:

1. Correct, reproducible learning tasks.
2. A fast edit-run-test feedback loop.
3. Physical-AI depth: perception, geometry, state estimation, planning, control, VLM/VLA, robot learning, and robotics MLOps.
4. Paper-to-code traceability.
5. Secure execution and sustainable content operations.
6. Visual polish and community features.

## Environment and deployment boundary

- The user has started Vercel web deployment and authorized its build repair. The website may run locally or on Vercel; the evaluator and MuJoCo remain local-only. Hosted Supabase is authorized for email/password Auth and account display metadata; local Supabase remains supported. See docs/supabase-auth.md and docs/vercel-web.md.
- Outside the authorized Vercel web build/deployment and hosted Auth/account flow, do not create or mutate hosted Supabase resources, run remote migrations, deploy evaluator/simulator services, or add production secrets unless the user explicitly requests that phase. This account slice needs only a publishable key; never use a secret/service-role key in the browser.
- The user subsequently authorized the remaining release implementation and Supabase persistence setup. Reviewed hosted migrations may run once authenticated access is available. Prepare the separate evaluator/simulator deployment; the user explicitly reserved hosting selection, so do not deploy those services yet. See docs/RELEASE_PLAN.md. The browser still receives only the publishable key; database service credentials belong to the trusted control plane, never learner processes.
- Keep the web/control plane compatible with Vercel and database/auth/storage compatible with Supabase.
- Never run untrusted learner code in Vercel Functions, Vercel Edge Functions, Supabase Edge Functions, or PostgreSQL. Use the separate sandbox-worker interface defined in `SPEC.md`.
- Local development must work without hosted credentials. Keep environment-specific configuration outside problem content and evaluator logic.
- Simulator-backed problems use a narrow versioned backend interface. MuJoCo is the required local baseline; Isaac Sim is an optional GPU backend. Pin simulator/asset versions, physics settings, frames, units, seeds, and capability flags, and keep learner workloads isolated from native simulator processes.

## Repository layout

Use this target structure unless the existing implementation establishes a compatible alternative:

```text
apps/
  web/                  # learner-facing TypeScript web application
  api/                  # content, identity, progress, and submission API
  worker/               # isolated code-evaluation workers
packages/
  problem-schema/       # versioned schema and validators
  ui/                   # shared accessible UI components and tokens
  telemetry/            # typed events and privacy-safe instrumentation
content/
  problems/             # one directory per standalone problem
  tracks/               # ordered paper implementations
  fixtures/             # small, licensed test assets
research/
  papers/               # topic folders containing paired .pdf and .md paper files
  manifests/            # provenance and problem ideas
  templates/            # paper-card and problem-blueprint Markdown templates
specs/                  # focused technical design documents when needed
```

Do not create empty scaffolding merely to match this tree. Add directories when the work needs them.

## Working rules

- Make the smallest coherent change that satisfies the request.
- Before editing, state the interpretation being implemented and surface assumptions or tradeoffs that can change the public contract, grading behavior, data provenance, safety envelope, or architecture. Ask one concise question only when guessing would create material risk; otherwise state the assumption and proceed.
- Prefer the direct implementation. Do not add speculative features or configurability, create an abstraction for one caller, or introduce a dependency when existing code can express the behavior clearly.
- Match local style and keep diffs reviewable. Do not reformat, rename, or reorganize adjacent code as a side effect. Remove only imports/helpers made unused by the current change; report unrelated cleanup separately.
- When a proposed design expands scope without improving the requested outcome, offer the smaller verified path first.
- Preserve user changes and unrelated work. Never reset or overwrite them to get a clean tree.
- Prefer stable, typed interfaces and explicit validation at system boundaries.
- Keep UI copy plain, concise, and technically accurate.
- Use accessible semantic HTML, keyboard navigation, visible focus states, and WCAG AA contrast.
- Design responsive layouts from narrow mobile widths through large desktop workspaces.
- Never expose secrets to the browser or commit credentials, tokens, private datasets, or signed URLs.
- Treat all learner code as hostile. It must run in an isolated environment with no ambient credentials, no unrestricted network, bounded CPU/memory/time/output, and a disposable filesystem.
- Keep deterministic grading separate from explanatory examples. Hidden tests must test documented behavior, not tricks.
- Pin runtime and dependency versions for every published problem version.
- Do not add a service or framework without explaining why the current stack cannot meet the need.

## Research and paper policy

- For every new paper-track or major curriculum expansion, keep a dedicated **research-curator agent** in the work split. That agent searches primary sources, verifies paper identity and open-access status, downloads/validates the PDF, and creates/updates the paired Markdown card. Product/problem agents may consume those cards but must not silently invent paper metadata.
- Use primary, authoritative sources: conference proceedings, publisher pages, arXiv, or official project repositories.
- Download only openly accessible author/preprint PDFs. Never bypass authentication, paywalls, robots controls, or access restrictions.
- Use stable names: `YYYY-short-paper-title.pdf`.
- For every PDF, record the title, authors, year, venue/status, landing page, direct PDF URL, local path, contribution, and implementable problem ideas in the relevant manifest.
- Pair every `paper.pdf` with a same-directory, same-basename `paper.md` following `research/templates/paper-card.md`. The Markdown is an original agent-oriented summary and implementation map, not a full-text transcription.
- Validate that a download is a real PDF (header `%PDF`), is non-empty, and opens successfully. Record page count when practical.
- Do not claim that the library is exhaustive. It is a curated working set.
- Prefer linking to the canonical source in the product. Do not ship local research PDFs to end users unless redistribution rights were explicitly verified.
- Paper-derived explanations must be original summaries with precise citations. Quote sparingly.
- Start future paper-derived problems from `research/templates/problem-blueprint.md`. Create one Markdown blueprint per problem before implementation, and keep its paper ID, version, physical contract, runtime, grading, provenance, and license metadata complete.

## Problem authoring contract

Every problem must include:

- A stable slug and immutable semantic content version.
- Domain, topic, difficulty, runtime, dependency, and paper/dataset provenance metadata.
- A concise goal, typed function/class contract, constraints, and explicit tensor shapes/units/coordinate frames.
- At least two worked examples that do not reveal hidden tests.
- Starter code, reference solution, public tests, hidden tests, and an explanation/theory note.
- Deterministic seeds and numerical tolerances where relevant.
- Edge cases covering empty/minimal shapes, dtype/device behavior, invalid inputs where documented, and realistic scale.
- A declared resource budget and a license for original or adapted fixtures.

Difficulty rubric:

- **Easy:** one core idea, usually under 25 reference-solution lines, no architectural ambiguity.
- **Medium:** two or three interacting ideas, vectorization or careful shape/state handling, usually under 75 lines.
- **Hard:** a paper component or systems task with several invariants, performance constraints, or multi-stage evaluation.
- **Research:** reproduction or open-ended benchmark work; graded with explicit metrics and a reproducibility report, not a brittle single output.

For physical-AI content, always declare coordinate frames, units, axis conventions, timestamp assumptions, and batching rules. Diagram or visualize transformations when prose is insufficient.

### Theory-page contract

Every published problem has a Theory tab written in original language. It must contain:

- A short intuition section before formal math.
- Inline and display LaTeX for the essential mathematics, with every symbol, shape, unit, frame, and assumption defined near first use.
- At least one purposeful visual: an original diagram, interactive visualization, plot, animation, tensor/shape trace, or pipeline view. Decorative stock art does not satisfy this requirement.
- A worked numerical or tensor example connected directly to the learner contract.
- A “why this matters on a robot” section and at least one failure mode.
- Concise links to primary paper sources and prerequisites. Default to paraphrase; do not copy paper prose, figures, captions, tables, or code.
- A text/table alternative for visual content and reduced-motion behavior for animation.

Use `$...$` for inline math and `$$...$$` for display math in Markdown. Render with an accessible KaTeX/MathJax-compatible pipeline. Do not embed equations as raster images.

## Paper-track contract

A track decomposes one paper or a tightly related family into ordered, independently testable steps. It must include:

1. Orientation: what the learner will reproduce and what is deliberately out of scope.
2. Prerequisite diagnostic or links to prerequisite problems.
3. Atomic components before integration.
4. A small end-to-end implementation using licensed or synthetic fixtures.
5. Evaluation matching the paper's intent without pretending a toy run reproduces the published headline result.
6. A final model card or reproducibility note describing deviations, compute, data, seeds, and limitations.

Do not reduce a paper track to copying an architecture class. Include data contracts, loss/evaluation behavior, and at least one failure-analysis task.

## MLOps requirements

MLOps is first-class content, not only infrastructure. Include tasks for dataset validation, lineage, experiment tracking, reproducible builds, model packaging, edge optimization, deployment, drift/health monitoring, rollback, and incident analysis. Robotics tasks must account for sensor timing, calibration, hardware/software versions, scenario coverage, safety envelopes, and sim-to-real gaps.

Every backend feature that changes a submission, evaluation, or published content state must be observable with structured logs, a correlation ID, and privacy-safe metrics. Model/problem versions and evaluator images must be traceable from every score.

## Quality gates

### Issue-to-PR workflow

- Scouts coordinate review areas and deduplicate findings before opening issues.
- Assign one concrete issue to a dedicated fix worker in an isolated `codex/` branch/worktree. Preserve unrelated local feature changes.
- The worker reproduces the defect, implements the smallest coherent fix, runs focused checks, and prepares a PR linking the issue.
- The main agent reviews the exact diff and relevant checks, then merges ready issue-fix PRs. The user has authorized this workflow; a separate per-PR merge confirmation is not required.
- Do not bypass branch protection, required checks, or automatic approval rejections. Report blockers and retain concrete local drafts when a remote action is unavailable.

Before handing off a change:

- Define the proof of success before implementation: reproduce the failing case for a bug, name the observable outcome for a feature, identify behavior that must remain invariant for a refactor, and list concrete risks/tests for a review.
- Use the narrowest meaningful verification that proves the outcome, then broaden checks in proportion to risk. If a relevant check cannot run, say why and record the remaining risk.
- Run the most focused relevant tests, then broader tests in proportion to risk.
- Validate content/schema changes with the repository validator.
- For evaluator changes, run public and hidden test suites in a clean sandbox and verify time/memory/output limits.
- For UI changes, check loading, empty, error, success, signed-out, and narrow-screen states.
- For accessibility-sensitive UI, check keyboard use, labels, focus order, and contrast.
- For PDFs added to `research/papers/`, validate file signature and page readability; keep temporary renders outside final research folders.
- Report exactly what was verified and any checks that could not run.

## Definition of done

A task is done when behavior matches `SPEC.md`, tests cover the important contract, documentation/provenance is current, no secrets or unlicensed assets were added, and the result can be reproduced by another contributor from the repository instructions.

For non-trivial handoffs, report assumptions, changed behavior/files, verification performed, and remaining risk. Keep this lightweight for trivial edits.
