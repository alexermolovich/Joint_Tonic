---
schema_version: 1
paper_id: 2023-ego-exo4d
title: >-
  Ego-Exo4D: Understanding Skilled Human Activity from First- and Third-Person
  Perspectives
authors:
  - 'Grauman, Kristen'
  - 'Westbury, Andrew'
  - 'Torresani, Lorenzo'
  - 'Kitani, Kris'
  - 'Malik, Jitendra'
  - 'Afouras, Triantafyllos'
  - 'Ashutosh, Kumar'
  - 'Baiyya, Vijay'
  - 'Bansal, Siddhant'
  - 'Boote, Bikram'
  - 'Byrne, Eugene'
  - 'Chavis, Zach'
  - 'Chen, Joya'
  - 'Cheng, Feng'
  - 'Chu, Fu-Jen'
  - 'Crane, Sean'
  - 'Dasgupta, Avijit'
  - 'Dong, Jing'
  - 'Escobar, Maria'
  - 'Forigua, Cristhian'
  - 'Gebreselasie, Abrham'
  - 'Haresh, Sanjay'
  - 'Huang, Jing'
  - 'Islam, Md Mohaiminul'
  - 'Jain, Suyog'
  - 'Khirodkar, Rawal'
  - 'Kukreja, Devansh'
  - 'Liang, Kevin J'
  - 'Liu, Jia-Wei'
  - 'Majumder, Sagnik'
  - 'Mao, Yongsen'
  - 'Martin, Miguel'
  - 'Mavroudi, Effrosyni'
  - 'Nagarajan, Tushar'
  - 'Ragusa, Francesco'
  - 'Ramakrishnan, Santhosh Kumar'
  - 'Seminara, Luigi'
  - 'Somayazulu, Arjun'
  - 'Song, Yale'
  - 'Su, Shan'
  - 'Xue, Zihui'
  - 'Zhang, Edward'
  - 'Zhang, Jinxu'
  - 'Castillo, Angela'
  - 'Chen, Changan'
  - 'Fu, Xinzhu'
  - 'Furuta, Ryosuke'
  - 'Gonzalez, Cristina'
  - 'Gupta, Prince'
  - 'Hu, Jiabo'
  - 'Huang, Yifei'
  - 'Huang, Yiming'
  - 'Khoo, Weslie'
  - 'Kumar, Anush'
  - 'Kuo, Robert'
  - 'Lakhavani, Sach'
  - 'Liu, Miao'
  - 'Luo, Mi'
  - 'Luo, Zhengyi'
  - 'Meredith, Brighid'
  - 'Miller, Austin'
  - 'Oguntola, Oluwatumininu'
  - 'Pan, Xiaqing'
  - 'Peng, Penny'
  - 'Pramanick, Shraman'
  - 'Ramazanova, Merey'
  - 'Ryan, Fiona'
  - 'Shan, Wei'
  - 'Somasundaram, Kiran'
  - 'Song, Chenan'
  - 'Southerland, Audrey'
  - 'Tateno, Masatoshi'
  - 'Wang, Huiyu'
  - 'Wang, Yuchen'
  - 'Yagi, Takuma'
  - 'Yan, Mingfei'
  - 'Yang, Xitong'
  - 'Yu, Zecheng'
  - 'Zha, Shengxin Cindy'
  - 'Zhao, Chen'
  - 'Zhao, Ziwei'
  - 'Zhu, Zhifan'
  - 'Zhuo, Jeff'
  - 'Arbelaez, Pablo'
  - 'Bertasius, Gedas'
  - 'Crandall, David'
  - 'Damen, Dima'
  - 'Engel, Jakob'
  - 'Farinella, Giovanni Maria'
  - 'Furnari, Antonino'
  - 'Ghanem, Bernard'
  - 'Hoffman, Judy'
  - 'Jawahar, C. V.'
  - 'Newcombe, Richard'
  - 'Park, Hyun Soo'
  - 'Rehg, James M.'
  - 'Sato, Yoichi'
  - 'Savva, Manolis'
  - 'Shi, Jianbo'
  - 'Shou, Mike Zheng'
  - 'Wray, Michael'
year: 2023
venue_or_status: >-
  Author-deposited arXiv manuscript; final venue not asserted by this
  acquisition card.
primary_url: 'https://arxiv.org/abs/2311.18259'
pdf_url: 'https://arxiv.org/pdf/2311.18259'
local_pdf: ./2023-ego-exo4d.pdf
sha256: 15e31586e111eb32fe54131840b7733b095fb3b20bebb14be9610d11967e26a8
bytes: 44082158
pages: 99
topics:
  - mlops-data-deployment
  - ego-exo4d
modalities:
  - datasets
  - model-artifacts
  - logs
  - metrics
track_role: supporting
open_access_status: open-access-preprint
redistribution_note: Research copy only; verify the source license before redistribution.
execution_flow:
  title: Core execution flow
  description: >-
    Follow the data through the mechanism. Training objectives and inference
    behavior are distinguished in the linked explanations.
  nodes:
    - id: stage-1
      title: Align time and calibration
      detail: Connect multiple camera streams to a common reference.
      column: 0
      row: 0
      section: Align time and calibration
      problem_slugs: []
      planned_problems:
        - Synchronize Ego and Exo Camera Events
        - Validate Multi-View Calibration Metadata
    - id: stage-2
      title: Relate views geometrically
      detail: Project common 3D structure into each camera.
      column: 1
      row: 0
      section: Relate views geometrically
      problem_slugs:
        - project-camera-points
        - se3-transform-points
      planned_problems:
        - Project a Tracked Point Across Views
    - id: stage-3
      title: Evaluate skilled activity tasks
      detail: 'Use benchmark-specific language, pose, and procedural annotations.'
      column: 2
      row: 0
      section: Evaluate skilled activity tasks
      problem_slugs:
        - egocentric-activity-confusion-report
      planned_problems: []
  edges:
    - from: stage-1
      to: stage-2
      label: synchronized frames
    - from: stage-2
      to: stage-3
      label: aligned multimodal evidence
---

## Core paper explanation

Ego-Exo4D records skilled human activity with synchronized first-person and third-person views, calibrated geometry, and multimodal annotations. It supports studying how complementary viewpoints explain an activity.

## Execution flow

Follow the data through the mechanism. Training objectives and inference behavior are distinguished in the linked explanations.

### Align time and calibration

A teaching clock model is $t_j=a_jt_{\mathrm{ref}}+b_j$, allowing drift and offset. Use provided synchronization/calibration products rather than assuming identical frame indices imply simultaneity. Camera poses and sensor calibration can vary over a recording.


**Component practice**

- Synchronize Ego and Exo Camera Events — unreviewed idea; contract and evaluator required.
- Validate Multi-View Calibration Metadata — unreviewed idea; contract and evaluator required.

### Relate views geometrically

For world point $P_W$,
$$u_j=\pi_j(T_{C_jW}P_W).$$
$T_{C_jW}$ maps world to camera coordinates; $\pi_j$ includes the appropriate intrinsics and lens model. Pixel reprojection error and timestamp mismatch are different failure sources.


**Component practice**

- Supporting prerequisite: [Project Camera Points into Pixels](/problems/project-camera-points). Practices the stated data or mathematical operation; it does not implement this paper-specific stage in full.
- Supporting prerequisite: [Apply an SE(3) Transform to Batched Points](/problems/se3-transform-points). Practices the stated data or mathematical operation; it does not implement this paper-specific stage in full.
- Project a Tracked Point Across Views — unreviewed idea; contract and evaluator required.

### Evaluate skilled activity tasks

A pose error such as $N^{-1}\sum_i\|\hat P_i-P_i\|_2$ is meaningful only with matching joints, units, alignment, and visibility rules. This is a teaching diagnostic; official benchmark protocols differ by task. Human performance annotations do not directly define robot actions.


**Component practice**

- [Aggregate Evaluation by Activity Slice](/problems/egocentric-activity-confusion-report).

## Implement the components

Each execution-flow node links the matching runnable component or names its planned problem. Planned titles are not runnable; labels distinguish reviewed drafts from unreviewed ideas.

- **Supporting prerequisite:** [Project Camera Points into Pixels](/problems/project-camera-points).
- **Supporting prerequisite:** [Apply an SE(3) Transform to Batched Points](/problems/se3-transform-points).

**Component status:**

- Synchronize Ego and Exo Camera Events — unreviewed idea; contract and evaluator required.
- Validate Multi-View Calibration Metadata — unreviewed idea; contract and evaluator required.
- Project a Tracked Point Across Views — unreviewed idea; contract and evaluator required.
- [Aggregate Evaluation by Activity Slice](/problems/egocentric-activity-confusion-report).

These bounded exercises do not claim to reproduce the complete paper or its benchmark results.

## Scope of the runnable components

The shared activity-slice exercise is explicitly classification-only: it keeps dataset identity and true-class support, then reports recall over supported classes. It does not implement the pose, proficiency, synchronization or other task-specific official benchmark metrics.

## Why this matters on a robot

Multiple viewpoints can clarify occluded hand–object interactions. Camera calibration uncertainty and human-to-robot embodiment differences must remain visible when using such evidence for manipulation learning.

## Sources and scope

[Primary paper](https://arxiv.org/abs/2311.18259) · [Open-access manuscript](https://arxiv.org/pdf/2311.18259)

This is an original explanation of selected mechanisms. Equations use the notation defined here; simplified teaching models are identified explicitly. Small component exercises do not reproduce the paper's full experiments. The local PDF is a research reference; its redistribution terms remain those recorded in the metadata.
