# Joint Tonic product specification

**Status:** Implementation-ready baseline  
**Version:** 1.1.0

**Date:** 2026-11-13  
**Audience:** Product, design, content, research, platform, and evaluation engineers

## 1. Product definition

Joint Tonic is an interactive learning and benchmarking platform for **physical AI**. Learners solve focused coding problems, build paper implementations step by step, and practice the operational work required to move embodied-ML systems from notebooks to robots.

The core loop is:

> Understand a physical-AI concept → implement it in a browser workspace → run deterministic tests → inspect failures and visualizations → submit a versioned solution → continue through a paper track.

The launch wedge is the gap between generic machine-learning exercises and full robotics projects. Joint Tonic teaches the pieces that repeatedly fail in real systems: frames and transforms, sensor alignment, perception post-processing, policy inputs/outputs, dataset quality, reproducibility, deployment, monitoring, and sim-to-real evaluation.

### 1.1 Reference product

[Tensor Tonic's problem catalog](https://www.tensortonic.com/problems) demonstrates a useful catalog with topic/language filters, difficulty, progress, search, and browser execution. Its [research-paper experience](https://www.tensortonic.com/research) decomposes a landmark paper into ordered implementation steps. Individual problems separate Problem, Theory, Solution, Submissions, and Notes.

Joint Tonic will adopt these general interaction patterns while using original design, wording, curricula, solutions, tests, and physical-AI-specific features. It is not a visual or content clone.

## 2. Goals and non-goals

### 2.1 Goals

- Make physical-AI fundamentals executable and testable without requiring a robot.
- Turn important papers in perception, VLM/VLA, robot learning, and robotics systems into coherent implementation tracks.
- Give MLOps, data, deployment, evaluation, and monitoring at least equal weight to model architecture in advanced tracks.
- Provide trustworthy grading with pinned environments, deterministic fixtures, clear tolerances, and versioned evaluators.
- Support an on-ramp from NumPy/Python exercises to PyTorch, simulation, GPU kernels, and reproducible experiments.
- Record learner progress, submissions, track completion, and competency evidence.
- Build a content system that research engineers can extend without editing application code.

### 2.2 Non-goals for the first release

- General-purpose interview preparation for all of ML.
- Hosting unbounded user training jobs or arbitrary internet-connected code.
- Claiming that toy datasets reproduce published headline metrics.
- Real-robot remote control.
- A marketplace, paid creator economy, social feed, or live competitions.
- Republishing local reference PDFs unless redistribution rights are verified.

## 3. Target users and jobs

### 3.1 Primary users

- ML engineers moving into robotics or embodied AI.
- Robotics engineers strengthening modern deep-learning and MLOps skills.
- Graduate students implementing VLM, VLA, perception, or policy-learning research.
- Teams onboarding engineers to a common physical-AI stack.

### 3.2 Jobs to be done

- “Help me understand this paper by making me implement the important pieces in the right order.”
- “Let me practice a robotics concept without spending a day configuring a simulator.”
- “Show me why my tensor, transform, timestamp, or evaluator is wrong.”
- “Teach me how a research model becomes a reproducible, monitored deployment.”
- “Give me credible evidence of what I can implement, not just what I watched.”

## 4. Product principles

1. **Executable over passive.** Explanations lead quickly to code, tests, or an interactive visualization.
2. **Physics-aware contracts.** Shapes alone are insufficient; units, frames, time, calibration, and uncertainty are explicit.
3. **Small steps, real composition.** Atomic problems culminate in an integrated model or pipeline.
4. **Reproducibility over leaderboard theater.** Versions, seeds, environments, metrics, and deviations are visible.
5. **Failure is curriculum.** Learners inspect class imbalance, drift, calibration errors, latency, and sim-to-real gaps.
6. **CPU first, acceleration when meaningful.** Most onboarding tasks run immediately; GPU work is queued and budgeted.
7. **Original and attributable.** Content is original, and research/data provenance is precise.

## 5. Information architecture

### 5.1 Launch navigation

- **Problems:** searchable standalone exercises.
- **Tracks:** ordered curricula, including paper implementations.
- `/tracks` keeps the three introductory paths and adds a searchable, topic-filtered track for every canonical research paper. Each `/tracks/paper-{paper-id}` page exposes ordered component exercises, prerequisite links, proposed components and a paper-specific integration/evaluation/reproducibility plan from `content/tracks/papers/`. Available exercise progress is separate from pending integration assessment; paper tracks do not imply full-paper reproduction. The left navigation groups these tracks by research topic. `content/PAPER_TRACKS.md` is the complete Markdown index, synchronized with the paper library.
- **Projects:** topic sheets leading to paper-based model explanations, execution graphs, and linked coding components.
- **Systems:** MLOps and production-robotics scenarios.
- **Progress:** completed problems, track state, strengths, and saved work.

Later: team classrooms, benchmark labs, authoring studio, and community discussion.

Site navigation is a persistent left tree, replacing the horizontal header, announcement strip, and footer navigation. It contains Home, Problems with individual exercises, Tracks with learning paths, Projects with topics and papers, Systems, Progress, and Settings. Expand/collapse controls reveal nested entries; search filters page and paper names. The current page is marked. Desktop can collapse the tree into an icon rail without remounting the workspace; narrow screens use the rail and an accessible drawer with Escape/focus restoration. Existing project and paper pages use this shared tree rather than duplicate navigation panels.

The Projects index at `/projects` groups the research corpus into nine topic sheets at `/projects/sheets/{topic}`. Each source paper opens at `/projects/{paper-id}` with orientation, a model execution flow, mathematical explanations, and available coding exercises. The original source title and citation remain visible. Existing `/papers` URLs redirect to Projects, including alternate IDs for the same canonical paper.

Project topics live under Projects in the shared left tree; the selected topic, search, availability filter, and cards occupy the main column. Topic counts reflect the full corpus, independently of search. Individual paper views follow the browser pattern of the [TensorTonic research reference](https://www.tensortonic.com/research?paper=lstm): a searchable, grouped paper list on the left, with the selected paper's summary, actual linked-problem progress, implementation stages, and model diagram on the right. Detailed mathematics and practice links continue below. The current topic/paper is marked in navigation; no large topic grid precedes the content.

Cards distinguish **coding components available**, **model explanation available**, and **in preparation**. Stage counts come from validated execution-flow metadata. Linked-problem counts combine direct paper associations and flow-node links without duplicates; these can include prerequisites and do not measure full paper reproduction. Cards show the linked exercises' difficulty breakdown and actual locally saved solved count. Search covers titles, authors, and topics; filters separate coding availability from explanation availability. Incomplete authoring cards show a preparation notice instead of agent instructions. Research PDFs remain local authoring references.

Every paper flow stage associates exercises with the mechanism explained by that stage. `problem_slugs` contains verified runnable tasks; `planned_problems` contains original future-exercise titles, using exact curriculum/blueprint names when available. Planned titles never create dead problem routes. A unique exact title match can become a runnable association when its problem is published; keyword guesses and ambiguous titles do not. The graph shows runnable/planned counts and an Implement link for a single runnable component, or a link to that stage's exercise list. Stage lists and the corresponding math explanation provide the problem name, implementation scope and supporting-prerequisite distinction. New paper ideas do not silently expand the approved curriculum.

### 5.2 Problem catalog

The catalog must support:

- A simulator filter with All simulators and MuJoCo. MuJoCo matches explicit `simulator.backend: "mujoco"` metadata, combines with the other filters, and persists as `?simulator=mujoco`. This identifies simulator-backed exercises, independent of whether a hosted simulator is available.

- Full-text search over title, summary, concept, paper, and tags.
- Filters for domain, topic, difficulty, runtime, framework, modality, estimated time, paper, and status.
- Sort by recommended, newest, difficulty, duration, and completion.
- Cards/rows showing title, difficulty, domain, runtime/framework, estimated time, paper badge, and solve status.
- Shareable URL state for filters, search, sorting, and pagination.
- Signed-out browsing. The local prototype continues to allow browser-local Run/Submit; hosted private progress and authoritative account-owned submissions require the later server-verified persistence adapter. Account login alone does not change evaluator ownership.

Initial top-level domains:

| Domain | Representative topics |
|---|---|
| Geometry and calibration | SE(2)/SE(3), quaternions, camera models, hand-eye calibration, projections |
| Perception | detection, segmentation, tracking, depth, optical flow, point clouds, BEV |
| State estimation | Bayesian filters, Kalman variants, particle filters, visual-inertial fusion |
| Planning and control | search, trajectories, MPC, PID, collision checking, constraints |
| Robot learning | imitation, offline RL, diffusion policies, action chunking, evaluation |
| VLM and VLA | multimodal tokens, grounding, action tokenization, robot prompting, policy heads |
| Simulation and sim-to-real | domain randomization, scenario generation, system identification |
| Robotics MLOps | data quality/lineage, training pipelines, packaging, edge inference, monitoring, rollback |
| Safety and evaluation | OOD, uncertainty, scenario coverage, guardrails, incident analysis |

The local catalog uses a compact problem list with horizontal topic chips, runtime tabs derived from available problems, search, difficulty/status filters, and sorting. Filter state is shareable in the URL. A progress sidebar links to the next exercise and guided paths; narrow screens prioritize the list. Original robotics icons identify the domains in both filters and rows.

### 5.3 Visual direction

Default to Gruvbox Dark: warm charcoal surfaces, orange accents, and cream text. Settings offers immediately applied, locally persisted Gruvbox Dark, Slate Dark, Warm Light, and Graphite choices. Graphite is an opt-in alternative inspired by the reference's neutral dark surfaces, clear white/gray text, and mint accent; adding it does not change the existing default or saved preference. Shared semantic colors apply to navigation, catalogs, problem material, full-window Theory, charts, and the code editor. Use the system sans-serif stack observed on the TensorTonic reference (Segoe UI on Windows), with 16–17px reading text and a separate monospace code font. Keep positive and negative results visually distinct and labeled, keyboard focus visible, and layouts responsive.

Learning-path cards show real solved counts and a difficulty breakdown, with concrete component-oriented titles. Keep cards without artwork until the user supplies approved imagery. The supplied robot-arm illustration accompanies the manipulation-related VLM/VLA path; provenance is recorded in `docs/user-provided-media.md`. Original robotics topic icons identify frames, cameras, grippers, robot learning, and deployment.

### 5.4 Local account statistics

The Progress page is the local account dashboard: solved totals, saved submissions, graded acceptance, current/best recorded streaks, an activity calendar, robotics-domain breakdowns, recent unique completions, learning paths, and drafts. Use actual local records and clearly show empty/loading states. Acceptance excludes platform errors; day-based activity uses the browser's local calendar dates. History metrics cover only the latest 100 retained submissions, while solved totals use the persistent solved set. Explain this limit in the interface. Rank, XP, awards, and quizzes require defined rules/content before appearing as product metrics.

## 6. Learner workspace

The local desktop workspace fills the available viewport beside the collapsible navigation tree, with learning material on the left and code/results on the right. A compact breadcrumb identifies the current problem; the problem title appears once in the learning pane. Equal-width desktop panes have no large outer frame or margins. Run/Submit sit in the editor toolbar, and the results panel collapses to its header to return space to the editor. Appearance links to Settings. Narrow screens stack the learning and coding panes. Resizable panes and mobile pane switching remain follow-up work.

### 6.1 Content tabs and Tensor Tonic workflow parity

The learner workspace targets functional parity with the relevant Tensor Tonic learning loop: separate learning tabs, an adjacent code workspace, immediate Run/Submit feedback, and saved progress. Joint Tonic uses original design and content, and adds physical contracts plus paper/MLOps traceability.

- **Problem:** goal, contract, examples, constraints, and submission requirements.
- **Theory:** original intuition, LaTeX mathematics, worked examples, interactive/static visuals, paper links, prerequisites, robot relevance, and failure modes. Theory is an ordinary tab within the left learning pane, alongside Problem and Solution; it never opens a full-screen modal. The editor and results remain visible and mounted on the right, preserving drafts and active evaluation. The shared problem heading introduces the article. Essential equations use readable, horizontally scrollable display cards, and the interactive visual and numerical readouts fit the learning pane with a text alternative.
- **Solution:** locked until solve or explicit reveal; reference implementation, complexity, alternatives, and failure modes.
- **Submissions:** immutable records with content/evaluator/runtime version, status, score, resources, and code snapshot.
- **Notes:** private autosaved Markdown notes with optional links to lines or test failures.

### 6.2 Code and result area

- Monaco-style editor with Python syntax, formatting, keyboard shortcuts, and accessible labels.
- Starter files and fixture browser when a problem needs more than one file.
- Run public tests without creating a scored submission.
- Submit against hidden tests in an isolated worker.
- Results grouped by correctness, numerical accuracy, performance, robustness, and style only when documented.
- Diff-friendly expected/actual values, tensor shape/dtype/device diagnostics, and plots for spatial/temporal outputs.
- Reset with a confirmation if unsaved local changes would be lost.
- Autosave drafts locally for signed-out users and server-side for signed-in users.

### 6.3 Robot simulator sidecar

Problems that benefit from embodied feedback—especially forward/inverse kinematics, motion planning, control, collision, and sim-to-real tasks—may provide a **Simulation** tab in the right coding pane. The current FR3 slice keeps learning material/Theory on the left and switches Code/Simulation on the right without unmounting the editor. Opening the problem initializes the local MuJoCo model; playback starts only on explicit user action. The learner can reset, play/pause, single-step, scrub a deterministic replay, select a camera, toggle frames/collision geometry, and inspect target/current pose and joint values.

The sidecar supports two backend adapters:

- **MuJoCo:** required local baseline for lightweight CPU-compatible development, deterministic fixtures, and the first kinematics/control problems.
- **NVIDIA Isaac Sim:** optional local/remote GPU backend for higher-fidelity sensors, assets, and later simulation workloads. Problems using it must declare hardware requirements and provide a MuJoCo or recorded-replay fallback when the learning objective does not depend on Isaac-specific behavior.

Both adapters implement the same bounded problem-facing protocol: `load_scene`, `reset(seed)`, `set_target`, `step(action, steps)`, `get_observation`, `get_state`, and `get_replay_frame`. Backend-specific features live behind declared capabilities rather than conditionals in learner code.

Every simulator problem pins the backend/version, robot/scene asset hashes and licenses, timestep, solver/integrator settings, joint limits, collision configuration, coordinate frames, units, seed, action/observation schema, and reset state. Grading uses numerical state/trajectory invariants and a deterministic replay; rendered pixels alone are never the authoritative score.

Learner code cannot access simulator processes or files directly. The isolated worker calls a narrow simulator service/API with bounded steps, state size, wall time, output, and approved assets. The browser receives validated state/replay payloads or bounded encoded frames, not an unrestricted native simulator stream. MuJoCo/Isaac process crashes are platform failures, not learner failures.

### 6.4 Theory and mathematical explanation standard

Every problem must have a first-class Theory tab; a short prompt plus a citation is not sufficient. The required teaching sequence is:

1. **Intuition:** explain the mechanism without assuming the paper has been read.
2. **Physical contract:** name shapes, dtypes, coordinate frames, units, axes, timestamps, batching, and masks.
3. **Mathematics:** render inline math with `$...$` and display math with `$$...$$` using an accessible KaTeX/MathJax-compatible renderer. Define every symbol and connect equations to variable names in starter code.
4. **Visual explanation:** include at least one original, purposeful diagram, plot, animation, tensor-flow trace, geometry overlay, or interactive visualization. Equations must remain text/MathML-capable rather than raster images.
5. **Worked example:** step through small real numbers or tensor shapes to the expected output.
6. **Robot relevance and failure modes:** explain latency, calibration, distribution shift, numerical, safety, or deployment consequences.
7. **Sources and boundaries:** link to the canonical paper and clearly state what the exercise simplifies.

Theory copy, visual assets, examples, and code are independently authored. Paper text, figures, captions, tables, or source code are not copied. Direct quotation should be rare, short, and attributed. A text/table alternative is required for visuals, and animations respect reduced-motion settings.

### 6.5 Visualization contract

Problems may define a visualization adapter that receives bounded JSON/artifact output, never executable learner HTML. Initial adapters:

- 2D image overlays: boxes, masks, keypoints, tracks.
- 3D frame/point-cloud viewer with labeled axes and frame transforms.
- Time-series plots for sensors, actions, latency, and drift.
- Confusion/calibration curves and scenario matrices.
- Pipeline DAG with version/lineage annotations.
- Robot state/replay sidecar with MuJoCo and Isaac Sim adapters, frame/joint overlays, targets, contacts, and collision visualization.

## 7. Problem types and grading

### 7.1 Types

1. **Function:** implement a pure numerical operation.
2. **Component:** complete a module such as NMS, attention fusion, or policy head.
3. **Debug:** diagnose and repair a realistic faulty implementation or metadata contract.
4. **Pipeline:** connect versioned stages and satisfy functional plus lineage checks.
5. **Optimization:** meet correctness first, then documented latency/memory targets.
6. **Experiment:** reproduce a bounded result and submit metrics plus a reproducibility record.
7. **Incident:** analyze logs/telemetry and choose or implement mitigation/rollback.

### 7.2 Difficulty

- **Easy:** one core operation; 10–20 minutes.
- **Medium:** interacting shape/state/geometry requirements; 25–60 minutes.
- **Hard:** paper or systems component with performance and edge cases; 60–150 minutes.
- **Research:** multi-stage reproduction with a metric and written evidence; hours to days.

Difficulty is assigned using concept count, prerequisite depth, implementation surface, debugging ambiguity, compute, and evaluation complexity—not solution length alone.

### 7.3 Grading rules

- Public tests illustrate the contract; hidden tests cover additional valid cases.
- Correctness is pass/fail per case unless an explicit metric threshold is more appropriate.
- Floating-point checks declare absolute/relative tolerance and acceptable nondeterminism.
- Performance tests run only in calibrated worker classes and never fail due to queue time.
- Style is advisory unless the problem explicitly teaches vectorization, API design, or systems hygiene.
- A learner can see which grading dimension failed, but hidden inputs remain protected.
- Every score links to problem version, evaluator version, container digest, dependency lock, and seed.

## 8. Paper implementation tracks

Each track teaches a paper or related family through 5–12 testable steps:

1. Orientation and paper map.
2. Data/observation/action contract.
3. Atomic representations or geometry.
4. Model/policy components.
5. Losses and training/inference behavior.
6. Evaluation and failure analysis.
7. Small end-to-end reproduction.
8. Packaging, deployment, monitoring, or sim-to-real extension where applicable.
9. Reproducibility/model card.

The UI must distinguish:

- **Concept implementation:** faithful small implementation of a paper mechanism.
- **Scaled-down reproduction:** same evaluation intent on reduced data/compute.
- **Full reproduction:** only when hardware, data, code, and methodology justify the claim.

Every step declares what differs from the paper. Track progress is a dependency graph, although most launch tracks present a recommended linear path.

### 8.1 Paper explanation and execution flow

Use the interaction pattern of the [TensorTonic RAG project](https://www.tensortonic.com/projects/rag-from-scratch): orientation, ordered components, a system-flow overview, and composition/evaluation. All Joint Tonic explanations and diagrams are original and specific to the referenced robotics paper.

- Open with what the method does, its inputs/outputs, and what the learner can implement today.
- Pair the ordered component list with an execution graph. Nodes link to the corresponding explanation section; runnable problem links sit directly beneath the relevant stage and beside the component's math in the article.
- Show actual data/model dependencies, branching and conditioning inputs. Label edges with meaningful tensors, shapes or signals. Distinguish training, inference, evaluation and robot-time loops. Systems and dataset papers use their operational pipeline rather than an invented neural architecture.
- Explain each component with intuition, substantial essential LaTeX mathematics, locally defined symbols/shapes/units/frames, and a small numerical or tensor example where useful. State how the coding task differs from the full paper.
- End with integration, evaluation, failure modes, and reproduction limits. Paper stages without implemented exercises remain explanation links; planned problems never masquerade as runnable exercises.
- Store graph nodes/edges in `execution_flow` YAML frontmatter alongside the paper Markdown. Validate IDs, coordinates, edges, exact plain-text section headings, and actual problem slugs. See `research/templates/paper-card.md`. Invalid metadata must not remove the rest of the paper from the catalog.
- The graph supports keyboard links, all three themes, contained scrolling at narrow widths, and an equivalent text flow. No copying of source-site or paper figures is needed.

Roll out the new format in reviewed batches, beginning with Diffusion Policy. The existence of a library card does not mean its mathematical explanation and flow have already been reviewed.

## 9. Launch curriculum

`MVP_10.md` defines the original ten-problem vertical slice. `CURRICULUM.md` contains 190 named practical problems across shared foundations, vision/VLM/3D perception, VLA/embodied learning, and robotics MLOps/deployment/sim-to-real. The current implementation and review state of every entry is recorded in `content/AUTHORING_STATUS.md`. Additional paper-flow ideas require a reviewed blueprint before becoming new implementation commitments.

The local catalog now expands incrementally from that baseline. `content/AUTHORING_STATUS.md` records each named entry as queued, planned, drafted, reviewed, or runnable, generated from the curriculum and content files. Runnable entries have complete versioned packages and pass public Run plus hidden Submit in the existing isolated worker. Standalone theory may use a purposeful static table or shape trace with `visualization: markdown`; an unrelated interactive diagram must never substitute for a missing adapter. Reference verification discovers published metadata and supports focused slug selection instead of a fixed ten-problem count. Shared local runtime caps remain 18 seconds wall time, 10 CPU seconds, and 4 GiB address space per process; smaller authoring targets are not represented as enforced budgets.

### 9.1 Foundation problems

- Homogeneous transforms, quaternion normalization/interpolation, projection/unprojection.
- IoU, anchor generation, NMS/Soft-NMS, box encoding, Hungarian matching.
- Camera distortion, point-cloud voxelization, farthest-point sampling, BEV pooling.
- Timestamp interpolation, approximate synchronization, calibration validation.
- Kalman predict/update, particle resampling, occupancy-grid log odds.
- PID anti-windup, trajectory interpolation, collision checks, simple MPC cost.
- CLIP-style contrastive loss, image/text token alignment, action normalization.

### 9.2 MLOps/system problems

- Validate a multimodal episode schema and reject silent unit/frame mismatches.
- Hash and version dataset shards; compute deterministic train/validation splits by scene.
- Detect sensor dropout and timestamp drift from logs.
- Build a reproducible training manifest from config, code, data, and environment versions.
- Compare offline and online preprocessing graphs for skew.
- Quantize an edge model and evaluate accuracy/latency/memory tradeoffs.
- Define safe canary/shadow evaluation for a perception or policy update.
- Detect scenario drift and calibration degradation.
- Decide rollback from latency, collision-proxy, intervention, and OOD signals.
- Construct a sim-to-real evaluation matrix with coverage and confidence intervals.

### 9.3 First paper-track candidates

The checked-in manifests are the source of truth for the curated paper library. The first tracks should be chosen using educational value, open access, tractable compute, reusable prerequisites, and production relevance. Candidate families:

- YOLO/detection lineage and modern post-processing.
- Vision Transformer plus CLIP-style vision-language alignment.
- Segment Anything or related promptable segmentation.
- PointNet-style point-cloud representation and modern 3D perception.
- RT-1/RT-2-style tokenized robot policies.
- PaLM-E-style embodied multimodal inputs.
- Diffusion Policy and action-chunking transformer policies.
- OpenVLA/Octo-style generalist policy adaptation.
- Domain randomization and sim-to-real evaluation.
- Production ML/data validation, continuous delivery, and edge inference.

This is a curated roadmap, not an exhaustive statement of the field.

## 10. Content schema

Canonical content is repository-backed, reviewable, and versioned. A problem directory contains metadata plus starter/reference/test files. The exact serialization may evolve, but it must express:

```yaml
schema_version: 1
slug: se3-transform-points
version: 1.0.0
title: Apply an SE(3) Transform to Batched Points
type: function
difficulty: medium
domains: [geometry-calibration]
topics: [se3, homogeneous-coordinates, vectorization]
estimated_minutes: 35
runtime:
  language: python
  image: joint-tonic/python-numpy@sha256:<digest>
  python: "3.12"
  dependencies: {numpy: "2.1.*"}
  limits: {wall_seconds: 3, cpu_seconds: 2, memory_mb: 512, output_kb: 64}
contract:
  entrypoint: solution.transform_points
  input_schema: {...}
  output_schema: {...}
  numerical_tolerance: {rtol: 1.0e-6, atol: 1.0e-7}
physical_contract:
  frames: [world, camera]
  units: {translation: meters, rotation: radians}
  axes: right-handed-z-up
grading:
  public_tests: tests/public.py
  hidden_tests: tests/hidden.py
  seed: 20261113
provenance:
  papers: []
  datasets: []
  fixture_license: CC0-1.0
```

Required human-authored material: summary, prompt, theory, examples, hints, solution explanation, common failures, and citations. A publishing validator blocks missing contracts, floating dependencies, invalid citations, unlicensed fixtures, nondeterministic tests, or broken reference solutions.

## 11. Functional requirements

### 11.1 Identity and progress

- OIDC-capable authentication with email/social providers as configuration, not hard-coded product logic.
- Public catalog and paper pages.
- Private drafts, notes, submissions, progress, bookmarks, and settings.
- Idempotent progress updates and resumable tracks.
- Account export and deletion.

### 11.2 Content and authoring

- Repository ingestion validates schemas and builds immutable versions.
- Draft/preview/published/retired states.
- Retired versions remain attached to historical submissions.
- Preview environment for every content change.
- Editorial review must include subject correctness, evaluator quality, pedagogy, provenance, and license.

### 11.3 Execution

- Browser execution is allowed only for approved, bounded runtimes.
- All authoritative submissions run server-side in disposable isolated workers.
- No outbound network from learner workloads by default.
- Read-only base image, ephemeral writable layer, unprivileged user, seccomp-style syscall restrictions, and no host/container socket.
- Queue admission, per-user rate limits, concurrency quotas, cancellation, and dead-letter handling.
- Output/artifact allowlist with size limits and malware/content checks before serving.
- GPU workers are a later pool with explicit quotas and cost telemetry.

### 11.4 Search and recommendations

- Search index updates when content is published or retired.
- Recommendations begin as transparent prerequisite/topic rules.
- “Next problem” explains why it is recommended.
- No opaque personalization is required for MVP.

## 12. Technical architecture

The user has authorized the remaining release work, including Vercel web publishing and Supabase persistence migrations once an authenticated connection is available. The website may run locally or on Vercel. Prepare the separate Linux evaluator and MuJoCo deployment; the user will choose its hosting provider before those services are deployed. Learner code never executes in hosted web/database functions. Repository-root Vercel builds use apps/web/.next and the packaging contract in docs/vercel-web.md. The current release split and outstanding verification are in docs/RELEASE_PLAN.md and deploy/README.md.

### 12.1 Applications

- **Web/control plane:** Next.js with TypeScript, App Router, server-rendered catalog/paper pages, client editor workspace, accessible component system, and Monaco. Run with the local Next.js development server now; deploy to Vercel later.
- **API:** Next.js Route Handlers and Server Actions for the first-party control plane, with shared typed contracts. Keep evaluation execution behind a separate internal runner interface.
- **Database/auth:** Supabase PostgreSQL and Supabase Auth. Use the local Supabase CLI/container stack during local development; apply reviewed migrations to hosted Supabase only during an explicitly authorized deployment phase.
- **Storage/realtime:** Supabase Storage for bounded submission artifacts and Supabase Realtime for job/progress updates when needed. Use local emulation now.
- **Job state:** Begin with a PostgreSQL-backed job table and explicit claim/state transitions. Add a dedicated durable queue only when measured load or failure behavior requires it.
- **Workers:** A separate local Python evaluator/worker during the vertical slice, using OCI images pinned by digest. Before public untrusted traffic, deploy workers to a service with gVisor/Kata/Firecracker-class isolation. Do not execute untrusted learner code in Vercel Functions, Vercel Edge Functions, Supabase Edge Functions, or the database.
- **Simulator services:** Local MuJoCo service/process as the baseline and an optional Isaac Sim service on a compatible GPU machine. Both expose the versioned bounded simulator protocol and feed validated state/replay data to the web sidecar. They are worker-side services, not Vercel/Supabase runtimes.
- **Observability:** OpenTelemetry traces/metrics/log correlation, error reporting, and product events with data minimization.

Local development must be able to start without hosted credentials: local web server, local Supabase services, local content ingestion, and local isolated worker. Environment-specific adapters isolate Vercel/Supabase configuration from problem and evaluator logic.

### 12.2 Service boundaries

```text
Browser
  ├─ content/progress → Next.js control plane → Supabase PostgreSQL
  ├─ auth/drafts       → Next.js + Supabase Auth/DB
  ├─ bounded artifacts → signed access → Supabase Storage
  └─ run/submit        → runner interface → isolated Python worker
                                           ├─ evaluator image
                                           ├─ bounded artifact upload
                                           └─ result event → DB/Realtime → browser
```

The production worker never receives general database or service-role credentials. It gets a single-use job payload and narrow, expiring artifact permissions. Local development may use a local-only credential through the same narrow interface, never embedded in learner workloads.

The prepared initial transport uses an authenticated Next.js proxy: Supabase Auth verifies the session, the server replaces browser-supplied ownership with the account ID, and a separate server-only token authenticates the backend call over HTTPS. Completed evaluations return through a token-authenticated `/api/evaluations` callback; the Vercel control plane invokes the service-only `record_evaluation` database transaction. The worker has no general database credential. This shared service credential is an initial control-plane transport, not the future single-use job capability described above.

The new experimental `data-only-functions-v1` grader keeps test code and expected results outside the learner process. Its bounded numeric transport does not preserve native object identity, in-place effects or autograd. Existing native-function contracts must not silently be graded with weaker semantics: hosted qualification requires an explicitly reviewed compatible execution contract and matching immutable artifact hashes. The existing catalog remains on its local native runner until a contract-compatible production path is qualified. A Docker/gVisor build and actual host containment checks are deployment gates, not inferred from local bubblewrap tests.

### 12.2.1 Account workspace synchronization

`/api/workspace` verifies bearer sessions with Supabase Auth and uses row-level security for private drafts, notes and bookmarks. Writes use expected revisions; conflicting edits preserve both copies until the learner chooses. Browser caches are scoped to the authenticated account and remain separate from guest work. Account changes abort pending requests and remount the editor boundary. An unavailable backend retains local edits and exposes retry status.

The browser cannot upload solved flags or manufacture submission history. Those records come from server-owned immutable jobs, evaluations and progress. The evaluator callback checks published content/runtime/fixture identity before recording a solve. Hosted use requires applied migrations and real published catalog versions; the public URL and publishable key alone do not apply a schema or publish versions.

Account storage may precede evaluator hosting. A published catalog-only version has a null runtime image and explicit `grading_protocol: "unavailable"`; it supports owner-scoped drafts, notes and bookmarks while trusted evaluation remains disabled. Never invent an image digest to enable account storage. The existing evaluation RPC rejects unavailable/null-runtime versions. Assigning a qualified runtime later requires a new immutable semantic version, preserving the older version's text and provenance rather than rewriting its identity.

### 12.3 Core entities

- `User`, `Problem`, `ProblemVersion`, `Track`, `TrackVersion`, `TrackStep`.
- `Draft`, `Run`, `Submission`, `Evaluation`, `TestCaseResult`, `Artifact`.
- `Paper`, `Dataset`, `Citation`, `RuntimeImage`, `EvaluatorVersion`.
- `Progress`, `Bookmark`, `Note`, `Competency`, `AuditEvent`.

Published content and evaluators are immutable; corrections create new semantic versions. Migrations may mark compatible versions for progress continuity, but historical submissions never change meaning.

### 12.4 Initial API surface

- `GET /problems`, `GET /problems/{slug}`, `GET /problems/{slug}/versions/{version}`
- `GET /tracks`, `GET /tracks/{slug}`, `GET /papers`, `GET /papers/{slug}`
- `PUT /drafts/{problemVersion}`, `POST /runs`, `POST /submissions`
- `GET /jobs/{id}`, `DELETE /jobs/{id}`, `GET /submissions/{id}`
- `PUT /progress/{trackVersion}/{step}`, `GET /me/progress`, `GET/PUT /notes/{problemVersion}`

Use cursor pagination, typed error codes, idempotency keys for mutations, and authorization checks at the resource layer.

## 13. Non-functional requirements

### 13.1 Performance

- Catalog LCP p75 under 2.5 seconds on a typical mobile connection.
- Search/filter response under 300 ms p95 after index warm-up.
- Draft autosave acknowledgment under 500 ms p95.
- CPU run queue-to-result under 5 seconds p50 and 20 seconds p95 for launch problems, excluding declared long experiments.
- UI remains usable while a job runs; status is resumable after refresh.

### 13.2 Reliability and reproducibility

- 99.9% monthly availability target for read/catalog/progress APIs after beta.
- At-least-once job delivery with idempotent evaluation persistence.
- Nightly reference-solution run across all published problem/runtime pairs.
- Restore-tested database backups and lifecycle policies for artifacts.
- Evaluator/runtime digest retained for the lifetime of a submission record.

### 13.3 Security and privacy

- Threat model covers code execution, artifact serving, auth/session abuse, prompt/citation injection in authored content, and supply chain.
- Dependency/image scanning and signed build provenance.
- CSRF/XSS/SSRF controls, strict CSP, secure cookies, and rate limits.
- Minimize stored personal data; separate product analytics from solution code.
- Private learner code is not used for model training or public examples without explicit opt-in.

### 13.4 Accessibility

- WCAG 2.2 AA target for the learner-facing product.
- Complete keyboard workflow for catalog, tabs, editor actions, resizing, tests, and dialogs.
- Text alternative/table fallback for instructional visualizations.
- Reduced-motion support and no color-only result status.

## 14. MLOps and platform observability

Every run produces a structured lineage record:

```text
user/draft snapshot
  + problem and evaluator versions
  + runtime image digest and dependency lock
  + fixture/dataset versions
  + seed and resource class
  → result, metrics, logs, artifacts, timing, and failure category
```

Operational dashboards cover queue depth/age, worker startup, evaluator failures, flaky tests, timeouts, OOMs, cost per run, artifact rejection, and completion funnels. Alerts must distinguish platform failures from learner failures.

Content health reports track solve rate, time-to-first-pass, hint/solution reveals, test-case failure distribution, abandon points, learner reports, and version regressions. These signals trigger human review; they do not silently change difficulty or grading.

## 15. Research library

The local research library lives under `research/papers/` with a manifest per direction under `research/manifests/`. It is a curated authoring corpus for the team. Each topic folder contains paired files: the source `paper.pdf` and an agent-ready `paper.md` with the same basename. The Markdown card stores normalized metadata, an original concise summary, an implementation decomposition, and problem blueprints; it is not a wholesale transcription of the paper.

Required streams:

1. VLA and embodied robot learning.
2. Vision, VLM, detection/segmentation, and 3D perception.
3. Robotics MLOps, deployment, data, simulation, sim-to-real, evaluation, and safety.

The consolidated catalog in `research/README.md` identifies which papers are present, which should become tracks, and which are supporting references. `research/templates/paper-card.md` defines agent context, and `research/templates/problem-blueprint.md` defines the Markdown-first contract for every future problem. Product pages link to canonical public sources. Local PDFs are not automatically deployed.

User-provided discovery indexes are audited under `research/sources/`. They are used to find candidates and taxonomy gaps, never as the final authority for title, authorship, venue, license, claims, or PDF provenance. The dedicated research-curator agent must verify primary sources before creating a paper card or downloading a PDF.

## 16. Metrics

### 16.1 North-star metric

**Verified learning completions per weekly active learner:** first-pass completions of problems or track steps with a versioned evaluator, excluding repeats of the same version.

### 16.2 Supporting metrics

- Activation: first successful run and first solved problem within the first session/week.
- Learning: track step completion, prerequisite remediation, later unaided success.
- Quality: learner report rate, evaluator defect rate, flaky test rate, solution-reveal-before-pass rate.
- Reliability: run success, queue latency, sandbox failure, result recovery after refresh.
- Curriculum: coverage by domain/difficulty/runtime and percent of tracks with MLOps/evaluation steps.
- Retention: learners returning to continue a track at 1, 4, and 8 weeks.

Do not optimize raw submissions or time-on-site as success metrics.

## 17. Delivery plan

### Phase 0 — specification and corpus

- Approve this specification and project instructions.
- Curate/validate the initial open-access paper library and manifests.
- Define schema v1 and author three representative problems: geometry, perception, and MLOps.
- Threat-model the execution path before implementation.

### Phase 1 — local vertical slice

- Local Next.js dev server, local Supabase stack, local content ingestion, and a separate local isolated Python worker. No Vercel deployment or hosted Supabase mutation in this phase.
- Catalog, problem page, editor, public tests, local isolated worker, and result UI.
- Repository-backed content ingestion and validator.
- Implement the ten problems in `MVP_10.md`, with paper links, original Theory/LaTeX, safe visuals, reference solutions, and deterministic evaluators.
- Ship at least three visualization adapters: 2D geometry/image overlay, tensor/assignment view, and time-series/distribution plot.
- One five-step mini-track assembled from the ten problems.
- No public untrusted traffic until sandbox review passes.

### Phase 2 — authenticated beta

- Deploy the Next.js control plane to Vercel and provision the reviewed database/auth/storage migrations on hosted Supabase.
- Auth, drafts, submissions, notes, progress, search/filter URLs.
- Remote isolated CPU worker service, immutable evaluator lineage, Supabase artifact storage, job-state updates, and observability. The worker service remains outside Vercel/Supabase execution runtimes.
- Expand beyond the initial ten only after the complete vertical slice is usable and verified; target 30–50 original problems and two complete paper tracks for the broader beta.
- At least 30% of launch problems address data, systems, evaluation, deployment, or monitoring.

### Phase 3 — physical-AI depth

- MuJoCo robot sidecar for kinematics/control problems, followed by the optional Isaac Sim GPU adapter and recorded-replay fallbacks.
- 3D/time-series visualizations, bounded experiment problems, GPU worker pool.
- Four to six paper tracks spanning vision, VLM/VLA, policy learning, and sim-to-real/MLOps.
- Team/classroom pilot and competency reports.

## 18. MVP acceptance criteria

The MVP is acceptable when:

1. A signed-out learner can browse/filter/search problems and open a shareable problem URL.
2. A learner can edit starter code, run public tests, inspect useful diagnostics, and submit to hidden tests.
3. The authoritative run occurs in a disposable, network-restricted environment with enforced CPU/memory/time/output bounds.
4. Refreshing or reconnecting recovers draft and job state.
5. A signed-in learner can resume a multi-step track and inspect immutable submissions.
6. At least three domains and three difficulties are represented, including a geometry task, a visual task, and an MLOps task.
7. One 5–8 step paper track ends in a bounded integration and reproducibility note.
8. Every published item passes schema, reference-solution, public/hidden-test, provenance, license, and accessibility review.
9. Every score is traceable to content/evaluator/runtime/data versions and seed.
10. Platform errors are distinguishable from learner test failures and are visible in operational telemetry.

## 19. Decisions and defaults to validate

These are proposed defaults; change them deliberately with an architecture decision record:

| Decision | Default | Why |
|---|---|---|
| First language | Python 3.12 | Dominant research/robotics ML learning surface |
| First libraries | NumPy, then PyTorch | Fast fundamentals followed by realistic model work |
| Local development | Next.js dev server + local Supabase + local Python worker | Complete offline-first vertical slice without touching hosted services |
| Web/control plane | Next.js + TypeScript on Vercel | SEO catalog plus rich workspace and chosen deployment target |
| API | Next.js Route Handlers/Server Actions with shared types | Direct fit for Vercel and one control-plane stack |
| Database/auth/storage | Supabase PostgreSQL/Auth/Storage | Chosen managed backend with local development support |
| Editor | Monaco | Familiar multi-file experience |
| CPU execution | Separate isolated OCI worker service | Authoritative grading cannot safely run in Vercel/Supabase functions |
| Browser execution | Optional approved runtimes only | Responsiveness without trusting it for scores |
| GPU | Deferred quota-controlled pool | Cost/security/queue complexity |
| Recommendation | Rules/prerequisites first | Transparent and adequate for early corpus |

Locked implementation defaults: the working product name is Joint Tonic; local-server development comes first; the eventual control plane uses Vercel and Supabase; the first implementation scope is `MVP_10.md`; and solutions unlock after a successful solve or an explicit reveal confirmation. Business model, team/classroom priority, GPU budget, and the production sandbox host are deferred and do not block the local vertical slice.

## 20. Research sources

- [Tensor Tonic problem catalog](https://www.tensortonic.com/problems), accessed 2026-11-13.
- [Tensor Tonic research-paper tracks](https://www.tensortonic.com/research), accessed 2026-11-13.
- Primary paper/project/proceedings links are recorded in `research/manifests/` and consolidated in `research/README.md`.

## 21. Coding readiness

Specification work is complete for the local vertical slice. No unresolved product decision blocks coding.

- Product workflow and Theory/LaTeX/visual standards are defined.
- The first ten problems, order, contracts, paper connections, visuals, and evaluator families are defined in `MVP_10.md`.
- The larger 190-problem curriculum is named and grouped in `CURRICULUM.md`; current runnable coverage is recorded in `content/AUTHORING_STATUS.md`.
- Paper-card and problem-blueprint schemas are defined, with 32 verified PDF/Markdown pairs available for authoring.
- Local execution and the Vercel/Supabase production boundary are locked.
- Untrusted learner execution is separated from the web/control plane.
- Quality, provenance, accessibility, security, observability, and definition-of-done rules are in `AGENTS.md`.

The first coding milestone is: scaffold the local Next.js application and local Supabase migrations, define the versioned problem schema/content loader, establish the separate local Python evaluator interface, and implement Problems 1 and 3 from `MVP_10.md` as the end-to-end reference slice.


### Account Auth implementation

`/account` supports email/password signup, confirmation, sign-in, sign-out on this device, and an editable display name stored in Supabase Auth user metadata. `/auth/reset-password` handles recovery and authenticated password changes. PKCE email callbacks must open in the requesting browser. The Auth SDK refreshes and persists sessions; session errors are visible. Metadata is display-only, never an authorization source. This first account slice does not require the public.profiles database table or a remote migration. That table remains reserved for the later database persistence adapter.

The left navigation and Settings link to Account. Anonymous reading and the local evaluator remain usable. Existing drafts, notes, bookmarks, results, and progress remain shared device-local workspace data, clearly labeled; they are not silently imported or presented as cloud-synced/private account data. Never treat the browser workspace UUID or local solved flags as authenticated/verified learning records. Future account-owned APIs must validate Supabase identity server-side and enforce RLS before accepting those records.

Configuration uses only NEXT_PUBLIC_SUPABASE_URL and NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY (or legacy anonymous key), in ignored apps/web/.env.local. HTTPS hosted Auth and loopback local Auth are supported; secret keys are rejected. No service-role key is required. Supabase redirect allowlisting and email delivery remain project-dashboard setup; see docs/supabase-auth.md.

For the current testing phase, signup should not require email confirmation, as requested by the user. Set Confirm email OFF in the hosted Supabase Email provider settings; the public client cannot mutate that project configuration. The existing signup flow accepts an immediate Supabase session. If confirmation remains enabled remotely, the application must still report the real pending-confirmation state, never fabricate authentication or bypass it with a privileged browser key. Password recovery remains email-based. No MFA challenge is implemented in this slice.

### First MuJoCo problem: Franka Research 3 joint interpolation

`/problems/fr3-joint-interpolation` introduces linear interpolation between two seven-joint configurations in radians. The reference asset must be the actual Menagerie Franka Research 3, with pinned upstream commit, file hashes, license notices, and documented tool frame. This is joint-space kinematics, not Cartesian IK, closed-loop dynamics, collision checking, or a hardware safety guarantee.

Opening this problem requests the home pose from a separate loopback-only MuJoCo service. The service lazily initializes the approved model and returns a bounded rendered PNG, joint vector and tool pose. It never accepts code, paths, assets, arbitrary models, or remote URLs. The same right-hand pane has keyboard-accessible Code and Simulation tabs; changing tabs preserves code and notes. The left Theory remains available. Offline/rendering failures have a retry state and do not block coding or grading.

The isolated evaluator optionally executes an authored `preview.py` public demonstration fixture for this problem and returns at most101 seven-joint waypoints, with finite values and model-limit validation before native simulation. These data are explicitly untrusted visual output, independent of grading, never hidden-test trajectories or privileged execution instructions. The frontend labels the evaluated code snapshot and warns when the current draft differs. No reference trajectory replaces failed learner output. Reset returns to model home; waypoint selection and explicit Play/Pause provide replay without autoplay, including for reduced-motion users. The Simulation tab continuously requests live MuJoCo frames while visible. Mouse/touch drag or arrow keys orbit the camera; wheel, +/− and buttons zoom; Reset camera restores the default view. One request at a time reads the latest camera/pose, avoiding a backlog during dragging. Hidden browser tabs pause the stream; failures wait for user retry. Playback advances on a display clock and slow rendering can skip displayed waypoints; this does not claim physical timing. The FR3 demonstration editor is prefilled with its reference solution for new or untouched drafts, per the user’s request; Reset code restores the starter and custom drafts are preserved.

The existing worker caps still apply to preview generation (18s wall,10s CPU,4GiB address space,64KiB stdout); rendering uses its own bounded loopback protocol. MuJoCo native failures are platform/display errors, not learner grading failures. `docs/mujoco-fr3.md` describes reproducible setup and known limitations.

While simulation remains local, the hosted workspace reports a missing simulator deployment before checking login and offers a link to the localhost Franka demo. Signing in does not make an undeployed backend available. Local guest practice remains supported; configured hosted services retain their existing authenticated boundary.

The FR3 Simulation pane offers **Run and play** before any result exists or after an editor change. This explicit action evaluates the current code snapshot in the isolated worker and starts playback only when that job returns a valid bounded preview matching the current draft. Existing fresh results can be replayed without rerunning. Editing stops playback and disables scrubbing stale output until rerun. The view exposes the exact public function arguments and selected returned row. Valid bounded output remains inspectable even if numerical grading fails; invalid output never receives a reference fallback. Each explicit run/play request starts playback at most once, and changing tabs does not restart it.
