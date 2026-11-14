# Joint Tonic research library

This directory is the curated research corpus used to design Joint Tonic paper tracks and standalone physical-AI problems. It is intentionally organized for both humans and coding agents.

Current inventory: **156 distinct primary papers and 157 paired Markdown/PDF artifacts**. The pre-existing duplicate Open X-Embodiment topic card is preserved. The [balanced six-paper expansion](manifests/balanced-expansion-156.md) adds geometry, planning, perception, mobile manipulation, dataset infrastructure and evaluation uncertainty. These sources do not automatically expand the approved 190-problem curriculum. The [library integrity audit](manifests/library-integrity-2026-11-14.md) verifies all local PDF/card pairs against their recorded hashes, sizes and page counts.

## Library map

```text
research/
  papers/
    vision-vlm-3d/      # detection, segmentation, VLM, representation, 3D/multi-view
    vla-embodied/       # robot policies, embodied models, imitation, generalist VLAs
    mlops-sim2real/     # data/systems, inference, benchmarks, simulation, deployment
  manifests/
    vision-vlm-3d.md
    vla-embodied.md
    mlops-sim2real.md
  sources/
    awesome-robotics.md
    yanjieze-paper-list.md
  templates/
    paper-card.md
    problem-blueprint.md
```

Every paper has two adjacent artifacts with the same basename:

```text
YYYY-short-title.pdf    # open-access source artifact for research use
YYYY-short-title.md     # original paper explanation, math, execution flow, and problem map
```

PDFs remain in the local research library and are intentionally excluded from Git. Open access does not imply redistribution rights, and the full local corpus is too large for a normal source repository. GitHub contains the Markdown cards and provenance manifests, which link to canonical sources.

Agents should read the Markdown card first and open the PDF when they need to verify a detail, equation, figure, ablation, or limitation. The Markdown card is not a complete transcription and must not be treated as a substitute citation for the primary source.

All current cards have original learner-facing core explanations, mathematical notation and execution flows. The `execution_flow` frontmatter renders a clickable model/system graph and component list; each node associates runnable problem slugs or clearly marked planned component titles with the relevant explanation section. Follow the paper-card template and `SPEC.md` §8.1, and preserve provenance fields. [Explanation validation status](EXPLANATION_STATUS.md) and the [component implementation map](FLOW_PROBLEM_MAP.md) distinguish content coverage from runnable implementations and full-paper reproduction.

## Topic collections

| Topic | Manifest | Focus |
|---|---|---|
| Vision, VLM, and 3D perception | [`vision-vlm-3d.md`](manifests/vision-vlm-3d.md) | YOLO and detection, transformer vision, vision-language alignment, segmentation, point clouds, multi-view/BEV |
| VLA and embodied learning | [`vla-embodied.md`](manifests/vla-embodied.md) | tokenized/continuous actions, imitation, diffusion/flow policies, cross-embodiment data, generalist policies |
| MLOps and sim-to-real | [`mlops-sim2real.md`](manifests/mlops-sim2real.md) | production ML, data validation, reproducibility, edge inference, benchmarks, simulation, evaluation, safety |

These are broad curriculum streams. Finer-grained `topics` and `modalities` live in each paper card so one paper can participate in several future tracks without duplicating the source PDF.

## Discovery sources

The files under `sources/` audit user-provided secondary indexes and maintain a prioritized post-MVP discovery backlog:

- [`awesome-robotics.md`](sources/awesome-robotics.md) is strongest for robotics systems, calibration, SLAM, manipulation, datasets, middleware, and established tooling.
- [`yanjieze-paper-list.md`](sources/yanjieze-paper-list.md) is strongest for current robot learning, world/action models, human-video transfer, foundation policies, 3D policies, humanoids, and dexterity.

These indexes are leads, not bibliographic authorities. A paper or dataset enters `papers/` only after a research-curator agent verifies a primary landing page, open-access artifact, metadata, provenance/license status, and practical problem surface. The current first post-MVP recommendations are DROID, DP3, PointNet++, Transporter Networks/Ravens, Dex-Net 2.0, Kalibr, ORB-SLAM2, HIL-SERL/SERL, R3M or PerAct, and TD-MPC2.

## Markdown-first problem workflow

1. Select a paper card and verify the intended mechanism against the PDF and canonical source.
2. Copy `templates/problem-blueprint.md` into a future topic/problem folder using a stable problem slug.
3. Complete all metadata, especially paper/version provenance, shapes, frames, units, time assumptions, dependencies, evaluator plan, numerical tolerance, and fixture license.
4. Review the blueprint for pedagogy and scope before writing starter code, solutions, or tests.
5. Implement and publish only after the reference solution and evaluator pass the quality gates in `AGENTS.md`.

One paper normally produces several blueprints: atomic mechanism, integration, evaluation/failure analysis, and MLOps/deployment. A paper track links those blueprints in prerequisite order.

## Rights and provenance

- PDFs were selected from openly accessible primary sources. Open access does not automatically grant redistribution rights.
- Local PDFs are research inputs; they are neither committed to this repository nor shipped in the production site by default.
- Product pages should link to the canonical landing page and use original summaries.
- Paper cards record access/provenance status and a redistribution note. Do not guess a license.
- Do not bypass paywalls or access controls and do not copy large portions of paper text into Markdown.

## Validation

Before adding a paper to the catalog:

- Confirm the file begins with `%PDF` and is non-empty.
- Open it with a PDF parser and record pages, bytes, and SHA-256.
- Confirm the title/authors/year against the canonical landing page.
- Check that the `.md` card and topic manifest point to the correct local and canonical artifacts.
- Ensure proposed problems are implementable, original, and explicit about what a small exercise does not reproduce.
