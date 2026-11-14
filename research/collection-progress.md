# Paper collection progress

Updated: 2026-11-13 (America/Denver)

**Status: complete — collection stopped at 150 distinct canonical papers.**

## Final counts

- Starting corpus: 32 PDFs representing 31 distinct papers.
- Added: 119 distinct primary-source PDFs and 119 paired original Markdown acquisition cards.
- Final library: 151 PDFs and 151 paired paper cards, representing 150 distinct canonical papers and 150 distinct PDF hashes.
- Existing duplicate preserved: Open X-Embodiment appears in the original VLA and MLOps topic folders. It counts once in the totals.
- Added PDF pages: 2,639.
- Added PDF bytes: 1,288,454,085 (about 1.20 GiB).
- Final catalog: [`manifests/expansion-150.md`](manifests/expansion-150.md).
- Scope: research files only; application, content, specification, and the ten-problem implementation scope were not changed by the collector.

## Topic balance

Each canonical paper counts once in one primary bucket. A paper may still be used across multiple future tracks. Existing Open X-Embodiment counts under VLA/generalist policies, robomimic under data/evaluation, and GR00T N1 under humanoids/dexterity.

| Primary topic | Existing distinct | Added distinct | Final distinct |
|---|---:|---:|---:|
| Perception and 3D | 8 | 12 | 20 |
| VLM and grounding | 2 | 13 | 15 |
| VLA and generalist policies | 7 | 11 | 18 |
| Imitation, RL, and world-model robot learning | 2 | 18 | 20 |
| MLOps, data, evaluation, and deployment | 9 | 16 | 25 |
| Simulation and sim-to-real | 2 | 13 | 15 |
| Geometry, calibration, SLAM, and state estimation | 0 | 15 | 15 |
| Planning, control, and inverse kinematics | 0 | 12 | 12 |
| Humanoids, locomotion, dexterity, and tactile sensing | 1 | 9 | 10 |
| **Total** | **31** | **119** | **150** |

## Validation completed

- All 119 added PDFs have the `%PDF-` signature, open with Poppler `pdfinfo`, and have positive page counts.
- Every added PDF has a same-basename card; declared paths, paper IDs, byte counts, pages, and SHA-256 match the artifact.
- All new cards contain the normalized 17-field front matter, 11 required body sections, three practical component candidates, original summaries, visual teaching plans, and operational extensions.
- The expansion manifest's local links resolve.
- Duplicate detection found exactly the one pre-existing duplicate hash group; no expansion duplicate was added.
- Seven initial title/identifier mismatches were corrected against canonical primary records before unrelated artifacts could enter the library; details are in the manifest. No unresolved download failure counts toward the total.

## Review boundary

The new Markdown files are **acquisition cards**: primary identity/abstract metadata and local artifacts were checked, and the proposed implementation ideas are original. Full-text mathematical, architectural, dataset/license, and evaluator review remains necessary when a paper is selected for a reviewed problem blueprint. Published performance claims and final venues are deliberately not guessed. No datasets, model weights, hosted resources, or code archives were collected.

