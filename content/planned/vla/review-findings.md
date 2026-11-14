# VLA source and review findings

This is the local issue trail for curriculum section3. Drafts are not approved for publication until independent subject-matter and evaluator review is recorded in their package.

## First batch

| Curriculum item | Draft folder | Review state |
|---|---|---|
| Select Compact Visual Tokens with Learned Attention | [rt1-compact-visual-tokens](rt1-compact-visual-tokens/blueprint.md) | Author draft; independent review pending |
| Build a Causal Action-Token Mask | [rt1-causal-action-token-mask](rt1-causal-action-token-mask/blueprint.md) | Author draft; independent review pending |
| Build Sliding Action Chunks with Padding Masks | [act-sliding-action-chunks](act-sliding-action-chunks/blueprint.md) | Author draft; independent review pending |
| Blend Overlapping Action Chunks with Temporal Ensembling | [act-temporal-ensembling](act-temporal-ensembling/blueprint.md) | Author draft; independent review pending |
| Compute a Conditional Noise-Prediction Loss | [diffusion-conditional-noise-loss](diffusion-conditional-noise-loss/blueprint.md) | Author draft; independent review pending |
| Sample Flow-Matching Action Interpolants and Targets | [pi0-flow-action-interpolants](pi0-flow-action-interpolants/blueprint.md) | Author draft; independent review pending |

## SRC-VLA-001: GR00T objective terminology

**Finding:** Curriculum section3.10 originally named “Compute a Diffusion-Transformer Action-Chunk Loss.” The manifest repeated that objective wording and described the capstone as action diffusion. The diffusion-transformer architecture does not imply a DDPM noise-prediction loss: [GR00T N1](https://arxiv.org/abs/2503.14734), Section2.1, explicitly uses action flow matching.

**Affected locations at discovery:** `CURRICULUM.md:273`; `research/manifests/vla-embodied.md:24` and `:50`. Line numbers can move as other work lands.

**Agreed correction:** “Compute a Masked Action Flow-Matching Loss.” Keep diffusion-transformer as the architecture description and identify masks as the future educational contract.

**Independent source review:** paper_explanations reviewed exact commit `12fb5c3cea64cfa8e3f9ef2c0b4edc6f4f5629e1` in the `codex/gr00t-flow-objective` worktree. Its two-file, three-insertion/three-deletion diff correctly separates architecture and objective. No source objection. Root owns integration and publication; this note does not assert that the commit is merged.

## SRC-VLA-002: RT-1 mask semantics

**Resolved before drafting:** The pinned [official mask implementation](https://github.com/google-research/robotics_transformer/blob/4569641b8111f3f402c32d8e24becd2a6e952ecc/transformer_network.py#L161-L196) uses a causal relation and removes action-query/action-key pairs. A visual query can still attend to an earlier action placeholder. The same source [zeroes input action embeddings](https://github.com/google-research/robotics_transformer/blob/4569641b8111f3f402c32d8e24becd2a6e952ecc/transformer_network.py#L585-L600).

**Draft decision:** Reproduce the raw structural mask and explicitly exclude teacher-forced action labels and shifted prediction readouts. Do not claim the mask alone prevents indirect target leakage. The second public example distinguishes this rule from clearing all action-key columns.

## SRC-VLA-003: ACT temporal weight direction

**Resolved before drafting:** [ACT](https://arxiv.org/abs/2304.13705), SectionIV.A, assigns index0 to the oldest prediction in its exponential weighting. Larger decay therefore favors older predictions. The draft uses oldest-first rank among eligible predictions and states that rank is not elapsed time. Explicit masks replace any inference of availability from nonzero action values.

## SRC-VLA-004: pi0 interpolation and target sign

**Resolved before drafting:** The checked-in [pi0 manuscript](https://arxiv.org/abs/2410.24164), SectionIV, constructs the interpolant as tau times actions plus one-minus-tau times noise, targets actions-minus-noise, and integrates forward from noise at0 to actions at1. The draft follows those explicit formulas. Scaling standard Gaussian noise by one-minus-tau implies covariance proportional to its square; the theory states that consequence rather than reproducing ambiguous Gaussian-parameter notation.

## Follow-up source wording outside this batch

- The OpenVLA roadmap/manifest phrase “training-set quantiles” must not be interpreted as equal-frequency quantile bins. The checked-in OpenVLA explanation correctly describes uniform bins between per-channel first/99th percentile bounds. Resolve the future problem title/contract before authoring it.
- The RT-1 paper card has a spacing typo, “into256uniform,” in its codec paragraph. No paper-card edit is made in this draft-only scope.

## Approved draft — rt1-compact-visual-tokens

Reviewer: code_issue_scout. Read all six files, the RT-1 card and manifest, and pinned official TokenLearner code. Confirmed spatial normalization and aggregation of original features. Independently recomputed both examples in WSL PyTorch, checked masked feature/logit gradients are zero, and verified the first attention row logit gradient against the analytic derivative. Supplied logits and padding are honestly scoped; no blocking contract issue. Implementation/evaluator checks remain separate.

## Approved draft — rt1-causal-action-token-mask

Reviewer: code_issue_scout. Read all six files, the RT-1 card and manifest, and pinned official mask/input-assembly code. Independently enumerated every cell of both examples. Confirmed action/action exclusion, retained causal action-placeholder access by visual queries, zeroed official input action embeddings, and explicit exclusion of teacher-forced-label safety claims. No blocking contract issue. Implementation/evaluator checks remain separate.

## Approved draft — act-sliding-action-chunks

Reviewer: code_issue_scout. Read all six files and ACT card/primary paper. Independently generated both window examples by direct index lookup. Confirmed terminal padding, valid zeros, ordered duplicate starts, empty start batch, exact copy semantics, input storage independence, channel units/frame preservation and documented TypeError/ValueError split. This is the explicit teaching data contract, not a claim to reproduce the full ACT loader. No blocking contract finding. Implementation/evaluator review remains separate.

## Approved draft — act-temporal-ensembling

Reviewer: code_issue_scout. Read all six files and ACT card/primary paper, sectionIV.A page5. Confirmed oldest-first exponential rank in the paper and same-target-time aggregation. Independently checked weights4/7,2/7,1/7 and action24/7 plus the zero-valued eligible candidate example. Reviewed compressed rank, masking, gapped ticks, no-eligible errors, float64 accumulation and exclusion of non-Euclidean action channels. No blocking contract finding. Implementation/evaluator review remains separate.

## Approved draft — diffusion-conditional-noise-loss

Reviewer: code_issue_scout. Read all six files and Diffusion Policy card/primary manuscript. Verified conditional noise-regression objective; masking/global scalar reduction are explicit teaching additions. Independently recomputed losses2.5 and8, checked prediction and target gradients including masked zeros in WSL PyTorch, and confirmed the all-padding rejection and tensor/shape contracts. No blocking contract finding. Implementation/evaluator review remains separate.

## Approved draft — pi0-flow-action-interpolants

Reviewer: code_issue_scout. Read all six files, paired card and primary manuscript. Independently recomputed both worked pairs and analytic gradients in WSL PyTorch. Confirmed noise-at0/action-at1 endpoints, actions-minus-noise derivative, per-item time broadcasting, zeroed padding, and acceptance of all-padding construction. Found a version-specific source discrepancy: v1 prints the opposite target sign; canonical v4 SectionIV page5 corrects it. Author pinned v4 in blueprint, statement and theory; independently rechecked those edits. No blocking contract issue remains.

## Approved draft — act-cvae-loss

Reviewer: code_issue_scout. Confirmed reconstruction-plus-KL scope against ACT sectionIV.B and the explicit L1 choice in sectionIV.C page6. Recomputed both examples, including (3-ln4)/4 KL; checked analytical prediction/mean/log-variance gradients on the first example. Global valid-scalar L1 and batch-mean latent sum are explicit teaching reductions. All-padding, posterior rows, noncontiguous data and scalar beta boundaries are clear. No blocking contract issue.

## Approved draft — palm-e-project-sensor-features

Reviewer: code_issue_scout. Read paired card and verified PaLM-E primary HTML/proceedings. Affine projection is correctly scoped as a supplied component, not the entire modality encoder. Independently recomputed both examples and masked feature/bias gradients. Shapes, row preservation, empty tokens, finite padding and no downstream attention-mask guarantee are explicit. No blocking contract issue.

## Approved draft — diffusion-receding-horizon-window

Reviewer: code_issue_scout. Confirmed receding-horizon intent against Diffusion Policy primary manuscript. Independently recomputed both windows, checked no storage alias, and verified that one unavailable selected tick rejects the entire batch. Alignment offset is supplied, invalid unselected rows remain permitted, and actual robot execution is explicitly out of scope. No blocking contract issue.

## Approved draft — rt2-serialize-action-tokens

Reviewer: code_issue_scout. Verified RT-2 primary section3.2 and paired card. Nonmonotone vocabulary examples independently map to [0,41,99] and [1,7,41], and [0,3]. Injective supplied mapping, reserved flag grammar and fixed field width are explicitly original. Empty batch, whole-batch rejection, dtype/range and storage contracts are clear. Integer grading metadata corrected to exact/0/0 before approval. No blocking contract issue remains.

## Approved draft — rt2-parse-action-grammar

Reviewer: code_issue_scout. Verified source token-assignment distinction and exact inverse mapping. Independently reconstructed both valid examples and confirmed reserved token1 is rejected in an action field. Input order, zero batch, unknown tokens, vocabulary uniqueness and independent returned storage are explicit. Integer grading metadata corrected to exact/0/0 before approval. No blocking contract issue remains.

## Approved draft — pi0-euler-action-flow

Reviewer: code_issue_scout. Verified pi0v4 sectionIV and AppendixA-D forward Euler, noise-at0 to actions-at1 convention. Independently computed constant-field nonuniform trace[2,3,6] and state-dependent trace[1,1.5,2.25]. Current-state left-endpoint evaluation, exactlyK calls, callback exception propagation, finite bounds and independent final/trace ownership are explicit. Physical control ticks and generative flow time remain separate. No blocking contract issue remains.
