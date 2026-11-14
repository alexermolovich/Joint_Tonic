# Name the GR00T action objective as flow matching

**Status:** Confirmed source-fidelity issue. Local issue/PR draft; GitHub publishing is blocked by the previously rejected credential-access route.

The GR00T N1 curriculum entry says “Compute a Diffusion-Transformer Action-Chunk Loss”, and its manifest uses architecture terminology without identifying the training target. This can lead a problem author to write a DDPM noise-prediction exercise for a flow-matching policy.

The primary manuscript describes the DiT action module as trained with action flow matching in the introduction and §2.1. A diffusion-transformer architecture does not determine a DDPM training objective. [GR00T N1 manuscript](https://arxiv.org/html/2503.14734v1#S2.SS1).

## Expected correction

- Name the problem **Compute a Masked Action Flow-Matching Loss**.
- Keep the diffusion-transformer architecture description, and explicitly state its flow-matching objective in the manifest.
- Preserve the paper ID, canonical URLs, PDF path, provenance, other problem names, and runtime behavior.

## Fix and review

- Branch: `codex/gr00t-flow-objective`.
- Isolated worktree: `.local/worktrees/gr00t-flow-objective`.
- Changed scope: one curriculum title and two manifest passages.
- Evidence checked against the primary paper and the corrected local paper explanation.
- No application/evaluator changes; no tests beyond the focused content diff are needed for this terminology correction.
- Merge remains pending an actual PR and final review. No GitHub issue number or PR number has been assigned.
