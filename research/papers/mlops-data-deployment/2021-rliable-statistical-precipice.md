---
{
  "schema_version": 1,
  "paper_id": "2021-rliable-statistical-precipice",
  "title": "Deep Reinforcement Learning at the Edge of the Statistical Precipice",
  "authors": [
    "Rishabh Agarwal",
    "Max Schwarzer",
    "Pablo Samuel Castro",
    "Aaron Courville",
    "Marc G. Bellemare"
  ],
  "year": 2021,
  "venue_or_status": "NeurIPS2021; arXiv v4 (2022 revision)",
  "primary_url": "https://arxiv.org/abs/2108.13264",
  "pdf_url": "https://arxiv.org/pdf/2108.13264v4",
  "local_pdf": "./2021-rliable-statistical-precipice.pdf",
  "sha256": "a6a5abb49e58a9e4a0be8556c8351ce8c3b52e70216bffc9fa80eac0823ec5ed",
  "bytes": 22838819,
  "pages": 28,
  "topics": [
    "evaluation uncertainty",
    "stratified bootstrap",
    "interquartile mean",
    "performance profiles"
  ],
  "modalities": [
    "benchmark scores",
    "training seeds",
    "task-level results"
  ],
  "track_role": "supporting",
  "open_access_status": "open-access-preprint",
  "redistribution_note": "Local research reference only. Open-access source verified; downstream redistribution rights have not been audited. The PDF is not a public product asset.",
  "acquired_on": "2026-11-13",
  "source_verification": "Primary title/authors and version checked; PDF signature, all-page parser readability, first-page visual render, count and SHA-256 validated.",
  "execution_flow": {
    "title": "Selected mechanism and implementation path",
    "description": "Reliable comparison of reinforcement-learning systems using uncertainty intervals, robust aggregates and performance profiles rather than only a few point estimates.",
    "nodes": [
      {
        "id": "collect",
        "title": "Preserve task and seed strata",
        "detail": "Preserve task and seed strata. See the original explanation and component status below.",
        "column": 0,
        "row": 0,
        "section": "Preserve task and seed strata",
        "problem_slugs": [],
        "planned_problems": [
          "Compute Confidence Intervals Across Robot Episodes"
        ]
      },
      {
        "id": "aggregate",
        "title": "Aggregate robustly across runs",
        "detail": "Aggregate robustly across runs. See the original explanation and component status below.",
        "column": 1,
        "row": 0,
        "section": "Aggregate robustly across runs",
        "problem_slugs": [],
        "planned_problems": [
          "Compute an Interquartile Mean Benchmark Score"
        ]
      },
      {
        "id": "compare",
        "title": "Compare distributions and uncertainty",
        "detail": "Compare distributions and uncertainty. See the original explanation and component status below.",
        "column": 2,
        "row": 0,
        "section": "Compare distributions and uncertainty",
        "problem_slugs": [
          "edge-inference-release-gate"
        ],
        "planned_problems": [
          "Compare Slice Metrics Without Hiding Regressions",
          "Bootstrap a Stratified Performance Profile"
        ]
      }
    ],
    "edges": [
      {
        "from": "collect",
        "to": "aggregate",
        "label": "validated component output"
      },
      {
        "from": "aggregate",
        "to": "compare",
        "label": "validated component output"
      }
    ]
  }
}
---

## Core paper explanation

An apparent benchmark improvement may come from a small number of random training runs rather than a consistently better algorithm. The paper studies uncertainty in deep-RL comparisons and recommends reporting interval estimates and distributional summaries. Its methodology is useful for robot evaluation, but adaptation must preserve the correct sampling unit and task structure.

## Execution flow

### Preserve task and seed strata

Let $x_{m,n}$ be a normalized score for task m and independent training run n, with M tasks and N runs per task. The array $X\in\mathbb R^{M\times N}$ has dimensionless normalized entries; raw reward units differ across benchmarks. A stratified bootstrap resamples runs within each task:

$$
X^{*(b)}_{m,n}=X_{m,I^{(b)}_{m,n}},
\qquad I^{(b)}_{m,n}\sim\operatorname{Uniform}\{1,\ldots,N\}.
$$

b indexes bootstrap replicates. This describes run-stratified uncertainty for a fixed task suite. A different target population may require resampling tasks too. Do not treat correlated frames from one rollout as independent training seeds. **Compute Confidence Intervals Across Robot Episodes** is a planned prerequisite with a distinct sampling-unit contract.

### Aggregate robustly across runs

The interquartile mean averages the middle half of pooled scores. A population definition in terms of quantile function $F^{-1}$ is

$$
\operatorname{IQM}(F)=2\int_{0.25}^{0.75}F^{-1}(p)\,dp.
$$

Finite-sample trimming and boundary rounding must be pinned in a coding contract. For sorted scores [0,1,2,3,4,5,6,100], dropping two from each end leaves [2,3,4,5], whose mean is3.5; the ordinary mean is15.125. **Compute an Interquartile Mean Benchmark Score** is a planned candidate, not an existing grader.

### Compare distributions and uncertainty

For threshold tau in normalized-score units, a run-score performance profile is

$$
\widehat P(\tau)=\frac1{MN}\sum_{m,n}\mathbf1[x_{m,n}>\tau].
$$

It reports how often performance exceeds a threshold instead of hiding all task/run variation in one number. Apply the same summary to bootstrap replicates to form an interval under the declared bootstrap method.

For two algorithms with scores $a_{m,i}$ and $b_{m,j}$, a probability-of-improvement statistic can use

$$
\widehat p=\frac1M\sum_m\frac1{N_A N_B}\sum_{i,j}
\left(\mathbf1[a_{m,i}>b_{m,j}]+\tfrac12\mathbf1[a_{m,i}=b_{m,j}]\right).
$$

The half-tie convention is explicit here. Paired experimental designs require corresponding paired resampling rather than silently assuming independent runs.

| Report | Reveals | Does not establish |
|---|---|---|
| IQM | Robust central performance | Every task improved |
| Profile | Fraction above thresholds | Physical safety |
| Bootstrap interval | Sampling uncertainty under assumptions | Absence of dataset bias |

**Compare Slice Metrics Without Hiding Regressions** and **Bootstrap a Stratified Performance Profile** are planned. [Edge Release Gate](/problems/edge-inference-release-gate) is a related operational prerequisite; its deterministic threshold checks are not these statistical procedures.

## Why this matters on a robot

Training seeds, rollout episodes and scene conditions are different experimental units. Preserve these identifiers and report difficult task slices. A narrow confidence interval can still describe a biased or unrepresentative evaluation set. This card supplies no new benchmark scores or statistical claim about a deployed policy.


## Sources and scope

[Canonical primary record](https://arxiv.org/abs/2108.13264) · [Pinned openly accessible manuscript](https://arxiv.org/pdf/2108.13264v4). This is an original selected-mechanism explanation, not a full-text transcription. Linked exercises are identified as direct components or supporting prerequisites. Planned node titles are research/curriculum ideas, not published problems; new ideas require a reviewed blueprint before implementation. PDF provenance and reuse status are recorded above.
