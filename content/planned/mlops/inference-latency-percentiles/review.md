# Author review — Compute p50, p90, and p99 Inference Latency

Status: reviewed draft; independent contract/content review approved. Author: code_issue_scout. Version: 0.1.0.

## Evidence and boundary

Checked the paired paper card, mlops-sim2real manifest, and primary source at Section IV inference scenarios and Table II; percentile calculation is a declared teaching convention. This is an original bounded decomposition, not a full reproduction. Worked outputs receive focused calculation checks; no runnable evaluator or simulator demonstration is claimed.

## Review focus

Percentiles are estimator-dependent; p50 is not the average of the central pair here. Mixing clocks or timing only launch submission undercounts actual robot latency.

Check agreement across statement/examples/theory, deterministic order and empty/error semantics, physical units and time, source scope, and hint progression. Confirm symbols and text alternatives are clear. Add reviewer, findings, disposition, and evidence after independent review.

## Pending

Runtime image and fixture hashes; reference/evaluator implementation; measured resource limits; rendered math/diagram accessibility; independent domain and evaluator reviews. No published meta.json exists for this package.

## Author verification checkpoint

Shared structural validation passed for this six-package batch (64 LaTeX expressions). Focused WSL numerical calculations passed for the skew, percentile, and dynamics examples. Graph outputs were manually traced against the stated edge directions and ordering. Independent cross-review remains pending; this is not implementation approval.


## Independent review — ui_issue_scout, 2026-11-13

Read all six package files plus source cards and primary-source landing pages. Independently derived both nearest-rank outputs using integer percentage arithmetic. Confirmed nanosecond subtraction before float conversion, one-based ranks, even-size p50, empty None outputs, and historical benchmark-versus-teaching distinction. No blocking content finding. Approved for implementation; pinned image, resource calibration, sandbox tests, and app rendering remain pending.
