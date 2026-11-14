# MLOps authoring and cross-review findings

This file records reproducible content issues and dispositions. It does not close runtime GitHub issues or claim that drafted content is published. Remote issue posting remains blocked through the previously rejected credential route.

## Batch 1 — author checkpoint

Six packages: dependency-graph-blast-radius; training-pipeline-topological-order; invalidate-downstream-cache; training-serving-transform-skew; inference-latency-percentiles; sample-dynamics-distributions.

- Shared structural validator passed: six packages, 64 LaTeX expressions.
- Focused WSL calculations confirmed both transform mismatch masks, both nearest-rank traces, and the log/discrete dynamics sampling outputs.
- Checked existing cards and the mlops-sim2real manifest against primary papers. Graph/cache contracts are original operational decompositions; latency is not an official MLPerf checker; integer fixed-episode delay deliberately differs from the dynamics paper's action-timestep process.
- Runtime images, implementation, hidden/public grading, measured resource budgets, and rendered accessibility remain pending.

## Author correction A1 — exact mismatch locations

The transform-skew output consists only of integer/name pairs. Its draft inherited unused numerical grading tolerances from a NumPy template. Set grading rtol/atol to zero to make exact location comparison explicit. Input tolerance parameters retain their stated mathematical role; no worked output changed.

## Independent findings

Pending reviewers. Record ID, affected file/contract, reproduction, expected/actual behavior, author correction, and independent recheck before marking a blueprint reviewed.

## Independent first-batch disposition — ui_issue_scout

All six packages approved as reviewed drafts on 2026-11-13. Read each six-file package and relevant source cards/pages; no blocking content finding.

- dependency-graph-blast-radius: both fixed-point closures independently recomputed; cycles, duplicate roots, and root exclusion agree across files.
- training-pipeline-topological-order: both schedules equal the minimum of all exhaustively enumerated feasible permutations; newly ready lexical priority and disconnected-cycle errors are explicit.
- invalidate-downstream-cache: Independently recomputed both downstream/cache intersections. Confirmed incoming parent-map orientation, cached-root inclusion, uncached-intermediate traversal, full-graph DAG validation, and honest TFX teaching scope.
- training-serving-transform-skew: Independently recomputed both mismatch masks using scalar comparisons. Confirmed strict equality boundary, asymmetric reference, row/column output ordering, shape validation before broadcasting, unit-alignment assumptions, and exact tuple grading after author correction A1.
- inference-latency-percentiles: Independently derived both nearest-rank outputs using integer percentage arithmetic. Confirmed nanosecond subtraction before float conversion, one-based ranks, even-size p50, empty None outputs, and historical benchmark-versus-teaching distinction.
- sample-dynamics-distributions: Independently checked both examples using the alternate a*(b/a)**u expression, integer buckets, and tick-to-second conversion. Confirmed fixed-range behavior, half-open draws, log-support positivity, declared per-episode semantics, and the explicit deviation from paper action-timestep randomization.

A1 is correctly resolved: transform-skew output locations use exact grading while input tolerances retain their stated numerical meaning. Content approval is separate from runnable evaluator and sandbox approval.

## Independent implementation finding M1 — oversized scalar errors

Reviewer: perception_implementation. Reproduction: supply built-in integer 10**1000 as transform_skew rtol or sample_dynamics dt_s. Actual: math.isfinite raised OverflowError before the documented bounds check. Expected: ValueError for out-of-range settings. Author moved bounded comparisons before math.isfinite and added a huge-integer regression to each existing validation family. Updated both evaluator hashes. Focused actual sandbox Run and Submit passed both packages (16 Submit checks plus six public Run checks). Independent correction recheck is pending.

### M1 independently resolved

perception_implementation independently rechecked both oversized integers and confirmed ValueError, reviewed corrected guards/tests, and approved all six MLOps reference implementations with the recorded actual sandbox evidence. No blocking implementation finding remains.

## Batch 2 — contracts and isolated implementation evidence

Six reviewed drafts: detect-pipeline-feedback-loops; robot-ml-readiness-score; slice-infrastructure-release-gate; physical-ai-incident-triage; record-artifact-lineage; verify-immutable-run-manifest. perception_implementation independently read all six packages, recomputed twelve worked outputs and verified the ML Test Score aggregation against sectionVI.A. No blocking contract finding. Shared structural check passed six packages/26 LaTeX expressions.

Staged references passed actual WSL bubblewrap Run and Submit:39Submit cases plus18publicRun cases. All six starter negative controls failed their three public cases. Publication waits for the final independent implementation recheck below.

## Independent implementation finding M2 — categorical arrays accepted as strings

Reviewer: perception_implementation. A one-element NumPy array containing pass was accepted as a release status, and a one-element array containing model was returned as an artifact kind. Python tuple membership coerced the array comparison to a truth value. Both contracts require strings. Added explicit isinstance(value,str) validation before membership and a regression using each exact supplied array. The two affected packages passed focused actual sandbox Run/Submit (13Submit plus6Run cases). Metadata and blueprint evaluator hashes were refreshed. Independent correction recheck pending.

## Paper-flow mapping checkpoint

Mapped56cards/168nodes across mlops-data-deployment, mlops-sim2real, simulation-sim2real and planning-control-ik, including curator-added TrajOpt, RLDS and rliable cards. Every node has a published primitive or explicitly planned problem title; stage text scopes supporting prerequisites. Checked runnable slug existence and exact section matches. Stage-specific titles distinguish reviewed drafts from unreviewed ideas. No source paper result, full reproduction or dataset redistribution is claimed.

Independent semantic review of root's27cards in humanoid-dexterity-tactile and robot-learning-rl (excluding newMobileALOHA) found no blocking mismatch. Reviewed all81node mappings and prioritized DP3/UMI/dexterity/DrEureka/SAC prose against primitive contracts: pooling follows per-point features, diffusion losses use epsilon targets, execution-window selection excludes reverse sampling, SE3 is point-frame practice, randomization is bounded, and SAC temperature tuning is labeled a later extension. No unrelated CLIP or R3M loss was mapped as a runnable implementation.

### M2 independently resolved and batch2 published locally

perception_implementation independently reproduced both corrected array inputs and confirmed ValueError. All six reference implementations approved. Published local problem packages307–312 after39Submit/18Run sandbox checks and six starter negative controls. Each package records its precise evaluator digest; no broader worker/runtime change was made.

## Batch3 independently approved and published locally

Six contracts313-318: infer-robot-episode-schema; robot-feature-anomalies; compare-training-serving-distributions; sensor-timestamp-calibration-skew; critical-data-anomaly-gate; scene-safe-trajectory-split. perception_implementation independently reviewed all36 draft files, recomputed12 worked outputs and approved all references/cases. No blocking findings. Shared validator passed6packages/29LaTeX. Actual WSL bubblewrap passed39Submit plus18Run cases; all six starters failed their three public cases. Publication uses actual shared worker limits and exact evaluator hashes. OCI digest and rendered accessibility remain pending. No shared UI/worker changes.

## Batch4 independently approved and published locally

Six contracts319-324: batch-variable-robot-episodes; validation-loss-rollout-ranking; demonstration-quality-performance; offline-rollout-checkpoint-gate; map-shared-robot-episode; balance-multidataset-batch. perception_implementation independently approved contracts and reference implementations, including exact rational gates and unit-family boundaries. Author recomputed12 worked examples. Shared validator passed6packages/35LaTeX. Actual WSL bubblewrap passed37Submit plus18Run cases; all six starters failed their three public cases. No blocking findings. Metadata pins evaluator hashes and actual worker limits; OCI digest and rendered accessibility remain pending.
