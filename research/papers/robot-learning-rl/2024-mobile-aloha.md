---
{
  "schema_version": 1,
  "paper_id": "2024-mobile-aloha",
  "title": "Mobile ALOHA: Learning Bimanual Mobile Manipulation with Low-Cost Whole-Body Teleoperation",
  "authors": [
    "Zipeng Fu",
    "Tony Z. Zhao",
    "Chelsea Finn"
  ],
  "year": 2024,
  "venue_or_status": "arXiv2024 v1",
  "primary_url": "https://arxiv.org/abs/2401.02117",
  "pdf_url": "https://arxiv.org/pdf/2401.02117v1",
  "local_pdf": "./2024-mobile-aloha.pdf",
  "sha256": "ad457dae227c27b0c2a15badfea5abbc6b0802877b25feceedeb770f0ebdb604",
  "bytes": 4357808,
  "pages": 20,
  "topics": [
    "mobile manipulation",
    "bimanual imitation learning",
    "whole-body teleoperation"
  ],
  "modalities": [
    "multi-camera RGB",
    "joint states",
    "base commands",
    "action chunks"
  ],
  "track_role": "supporting",
  "open_access_status": "open-access-preprint",
  "redistribution_note": "Local research reference only. Open-access source verified; downstream redistribution rights have not been audited. The PDF is not a public product asset.",
  "acquired_on": "2026-11-13",
  "source_verification": "Primary title/authors and version checked; PDF signature, all-page parser readability, first-page visual render, count and SHA-256 validated.",
  "execution_flow": {
    "title": "Selected mechanism and implementation path",
    "description": "A whole-body teleoperation and imitation-learning system combining bimanual arm control with mobile-base commands, with co-training from stationary ALOHA demonstrations.",
    "nodes": [
      {
        "id": "align",
        "title": "Align whole-body demonstrations",
        "detail": "Align whole-body demonstrations. See the original explanation and component status below.",
        "column": 0,
        "row": 0,
        "section": "Align whole-body demonstrations",
        "problem_slugs": [
          "interpolate-joint-state",
          "validate-robot-episodes"
        ],
        "planned_problems": [
          "Normalize Heterogeneous Robot Observation Schemas"
        ]
      },
      {
        "id": "learn",
        "title": "Learn coordinated action chunks",
        "detail": "Learn coordinated action chunks. See the original explanation and component status below.",
        "column": 1,
        "row": 0,
        "section": "Learn coordinated action chunks",
        "problem_slugs": [
          "act-sliding-action-chunks",
          "act-cvae-loss"
        ],
        "planned_problems": [
          "Mix Static and Mobile Demonstration Batches"
        ]
      },
      {
        "id": "control",
        "title": "Execute coordinated feedback",
        "detail": "Execute coordinated feedback. See the original explanation and component status below.",
        "column": 2,
        "row": 0,
        "section": "Execute coordinated feedback",
        "problem_slugs": [
          "act-temporal-ensembling",
          "diffusion-receding-horizon-window"
        ],
        "planned_problems": [
          "Measure Closed-Loop Latency and Action Dropouts"
        ]
      }
    ],
    "edges": [
      {
        "from": "align",
        "to": "learn",
        "label": "validated component output"
      },
      {
        "from": "learn",
        "to": "control",
        "label": "validated component output"
      }
    ]
  }
}
---

## Core paper explanation

Mobile ALOHA extends bimanual demonstrations to tasks that require the base to move while the arms work. The learning problem includes coordinated observation/action records and transfer from existing stationary demonstrations. Its practical contribution combines hardware/data collection with imitation learning; an action-loss function alone is not a reproduction of the system.

## Execution flow

### Align whole-body demonstrations

Represent a synchronized demonstration at control tick t as observations $o_t$ and a structured action

$$
a_t=[a_t^{\mathrm{left}};\ a_t^{\mathrm{right}};\ a_t^{\mathrm{base}}].
$$

The blocks retain their distinct semantics: arm/gripper commands and base velocities are not interchangeable coordinates. A future dataset contract must state channel order, normalization, base frame, units and control period $\Delta t$ in seconds. This notation deliberately avoids inventing one universal action width for every dataset export.

[Interpolate Joint State at Camera Time](/problems/interpolate-joint-state) and [Validate a Multimodal Robot Episode Schema](/problems/validate-robot-episodes) are implemented data prerequisites. **Normalize Heterogeneous Robot Observation Schemas** is planned.

### Learn coordinated action chunks

For horizon H, targets group future structured actions:

$$
A_t=[a_t,a_{t+1},\ldots,a_{t+H-1}]\in\mathbb R^{H\times D}.
$$

D is the declared normalized action width, and missing episode-tail entries require a mask. [Sliding Action Chunks](/problems/act-sliding-action-chunks) and [Masked CVAE Reconstruction and KL Loss](/problems/act-cvae-loss) implement relevant ACT components used in this learning family.

An explicit teaching description of co-training is

$$
\mathbb E[L]=\rho\,\mathbb E_{D_{\mathrm{mobile}}}[L]
+(1-\rho)\,\mathbb E_{D_{\mathrm{static}}}[L].
$$

Here rho is the sampling probability of mobile examples, not a physical sensor weight. The manuscript's co-training table reports equal source sampling for the described setup. Dataset-specific unavailable channels still need defined treatment; copying zeros into a base-velocity target without declaring semantics can manufacture false supervision. **Mix Static and Mobile Demonstration Batches** is a planned research candidate.

### Execute coordinated feedback

Overlapping chunks can estimate the same future action tick. With eligible predictions ordered oldest to newest, the ACT temporal blend is

$$
\bar a_t=\frac{\sum_i e^{-mi}\widehat a_t^{(i)}}{\sum_i e^{-mi}},\qquad m\ge0.
$$

[Temporal Ensembling](/problems/act-temporal-ensembling) implements this selection/weighting component. [Receding-Horizon Window](/problems/diffusion-receding-horizon-window) is a related controller-buffer prerequisite, not a claim that every Mobile ALOHA baseline uses that exact API. **Measure Closed-Loop Latency and Action Dropouts** remains planned.

| Block | Recorded evidence | Deployment risk |
|---|---|---|
| Arms | Synchronized joint/gripper actions | Left/right channel swap |
| Base | Motion command and timing | Frame or velocity-unit mismatch |
| Cameras | Exposure time and calibration | Stale visual feedback |

## Why this matters on a robot

Replaying a velocity trace does not guarantee the same base path when ground contact changes. Feedback must correct deviations, and results must be reported by task and scene conditions. Preserve data source, robot configuration, calibration and controller versions when comparing co-training choices.

## Implement the components

The linked exercises cover data alignment and ACT primitives. Whole-body hardware, teleoperation, original demonstrations and the paper's physical evaluation remain outside this local educational implementation.


## Sources and scope

[Canonical primary record](https://arxiv.org/abs/2401.02117) · [Pinned openly accessible manuscript](https://arxiv.org/pdf/2401.02117v1). This is an original selected-mechanism explanation, not a full-text transcription. Linked exercises are identified as direct components or supporting prerequisites. Planned node titles are research/curriculum ideas, not published problems; new ideas require a reviewed blueprint before implementation. PDF provenance and reuse status are recorded above.
