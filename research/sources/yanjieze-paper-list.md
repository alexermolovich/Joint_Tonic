# YanjieZe Paper-List discovery audit

- **Discovery repository:** [https://github.com/YanjieZe/Paper-List](https://github.com/YanjieZe/Paper-List)
- **Accessed:** 2026-11-13
- **Role:** High-volume, topic-curated discovery feed for robot learning, physical AI, vision, generative modeling, and recent conference/preprint activity. It is not a bibliographic or licensing authority.
- **Corpus comparison:** Leads below were checked by title against the current 32 local paper cards. None is already represented as a paper card.

## Useful taxonomy

The repository maintains topic views on top of a large chronological inbox. The most useful physical-AI branches are:

- self-improving robots and agents: agentic failure recovery, real-world RL, autonomous data collection, generated rewards/environments, curiosity, and data engines;
- world models and world-action models: joint world/action prediction, interactive simulators, latent model-based control, and video prediction for policies/rewards;
- human video to robot learning: egocentric/third-person data, retargeting, teleoperation, and internet-video transfer;
- robot foundation models and generalist policies;
- humanoid, dexterous, bimanual, mobile-manipulation, locomotion, and general robotic-manipulation tracks;
- 3D robot learning and 4D/geometry-aware representations;
- visual RL, imitation learning, representation pretraining, model-based RL, reward learning, language grounding, and benchmarks;
- diffusion for policy learning, offline/online RL, task-and-motion planning, and tactile/pose estimation;
- adjacent 3D vision, Gaussian splatting, graphics, generative models, self-supervised learning, and visual recognition;
- year/conference discovery views plus a very fresh “Recent Random Papers” inbox.

Compared with Awesome Robotics, this taxonomy is much denser for current learning research and far less complete for middleware, calibration, classical SLAM, low-level control, and deployment tooling.

## Discovery backlog

Priority meanings: **P1** = first post-MVP card candidates; **P2** = next expansion; **P3** = useful later; **dataset/fixture** = validate for evaluation use even if it does not become a paper card.

### Robot data, benchmarks, and human-video transfer

| Lead | Link exactly as listed | Why it fills a gap | Verification | Suggested priority |
|---|---|---|---|---|
| DROID | [https://droid-dataset.github.io/](https://droid-dataset.github.io/) | Large, multi-site in-the-wild manipulation data exposes schema, calibration, language annotation, diversity, and OOD evaluation issues absent from the corpus. | **Primary-source verified:** official project page independently checked; it links paper, dataset, setup, and policy code. | **P1 dataset + paper card** |
| Ego-Exo4D | [https://ego-exo4d-data.org/](https://ego-exo4d-data.org/) | Adds synchronized first/third-person skilled activity, camera geometry, temporal alignment, and human-to-robot representation questions. | **Primary-source verified:** official dataset/project page independently checked. | **P2 dataset/card** |
| Universal Manipulation Interface (UMI) | [https://umi-gripper.github.io/](https://umi-gripper.github.io/) | Bridges portable in-the-wild demonstration capture, calibration, action representation, and downstream policy training. | **Primary-source verified:** official project page independently checked. | **P1 data-engine card** |
| RLBench | [https://sites.google.com/view/rlbench](https://sites.google.com/view/rlbench) | Provides a standardized task/environment surface for manipulation policies and deterministic evaluator fixtures. | **Primary-source verified:** official project page independently checked; still pin simulator/task versions and license before use. | **P2 benchmark/fixture** |

### 3D, spatial, and language-grounded manipulation

| Lead | Link exactly as listed | Why it fills a gap | Verification | Suggested priority |
|---|---|---|---|---|
| 3D Diffusion Policy (DP3) | [https://3d-diffusion-policy.github.io/](https://3d-diffusion-policy.github.io/) | Combines sparse point-cloud encoders with action diffusion and explicitly evaluates spatial/view/appearance generalization. | **Primary-source verified:** official project page independently checked; links RSS 2024 paper, code, and data. | **P1 paper card** |
| PointVLA | [https://pointvla.github.io/](https://pointvla.github.io/) | A post-OpenVLA lead for injecting 3D features into a pretrained action expert with few-shot and real-vs-photo safety tests. | **Primary-source verified:** official project page independently checked; RA-L 2025 status stated there. | **P2 advanced VLA card** |
| PerAct | [https://peract.github.io/](https://peract.github.io/) | Teachable 3D voxel/Q-attention action prediction for multi-task manipulation. | **Primary-source verified:** official project page independently checked. | **P1 paper card** |
| CLIPort | [https://cliport.github.io/](https://cliport.github.io/) | Combines semantic “what” and spatial “where” pathways for language-conditioned manipulation; complements CLIP and Transporter Networks. | **Primary-source verified:** official project page independently checked. | **P1/P2 paper card** |

### Representations and world models for control

| Lead | Link exactly as listed | Why it fills a gap | Verification | Suggested priority |
|---|---|---|---|---|
| R3M | [https://arxiv.org/abs/2203.12601](https://arxiv.org/abs/2203.12601) | Adds robot-specific visual pretraining and frozen representation evaluation beyond CLIP/DINOv2. | **Primary-source verified:** official arXiv record independently checked. | **P1 paper card** |
| TD-MPC2 | [https://arxiv.org/abs/2310.16828](https://arxiv.org/abs/2310.16828) | Adds scalable latent world-model planning, continuous control, and robustness/evaluation surfaces. | **Primary-source verified:** official arXiv record independently checked. | **P1/P2 paper card** |
| DreamerV3 | [https://arxiv.org/abs/2301.04104](https://arxiv.org/abs/2301.04104) | A general world-model baseline for latent dynamics, imagined rollouts, and cross-domain evaluation. | **Primary-source verified:** official arXiv record independently checked. | **P2 paper card** |
| UniSim | [https://openreview.net/forum?id=sFyTZEqmUY](https://openreview.net/forum?id=sFyTZEqmUY) | Interactive real-world simulation is a key conceptual bridge between generative world models and policy evaluation. | **Needs primary-source verification:** OpenReview challenge page prevented independent content verification in this audit; confirm title, version, authors, and artifacts. | **P2 paper card after verification** |

### Real-world RL, self-improvement, and sim-to-real operations

| Lead | Link exactly as listed | Why it fills a gap | Verification | Suggested priority |
|---|---|---|---|---|
| HIL-SERL | [https://hil-serl.github.io/](https://hil-serl.github.io/) | Human interventions, resets, online improvement, safety, and high-precision manipulation are ideal production-loop topics. | **Primary-source verified:** official project page independently checked. | **P1 paper/operations card** |
| SERL | [https://serl-robot.github.io/](https://serl-robot.github.io/) | A software-suite view of sample-efficient real-robot RL adds replay, distributed collection, logging, evaluation, and recovery concerns. | **Primary-source verified:** official project page independently checked. | **P1 MLOps/system card** |
| DrEureka | [https://eureka-research.github.io/dr-eureka/](https://eureka-research.github.io/dr-eureka/) | Adds LLM-generated reward/domain-randomization curricula and sim-to-real validation beyond classic randomization papers. | **Primary-source verified:** official project page independently checked. | **P2 paper card** |

## Recommended additions after the 10-problem MVP

The first post-MVP wave should be small and operationally diverse:

1. **DROID** - one data-centric card covering episode schema, calibration, language labels, splits, lineage, and OOD evaluation.
2. **3D Diffusion Policy** - a natural synthesis of the existing PointNet/3D and Diffusion Policy tracks.
3. **HIL-SERL + SERL** - one paired research/system track for human intervention, online collection, replay, safety, and reproducibility.
4. **R3M or PerAct** - choose R3M for representation learning, PerAct for executable 3D action prediction; do not add both in the same sprint.
5. **TD-MPC2** - introduce world-model control only after basic policy/evaluation problems are stable.

The second wave can add UMI, CLIPort, Ego-Exo4D, DreamerV3, DrEureka, and PointVLA. Keep UniSim blocked until its canonical record and artifacts are independently verified.

## Freshness and coverage versus Awesome Robotics

| Dimension | YanjieZe Paper-List | Awesome Robotics |
|---|---|---|
| Freshness observed on 2026-11-13 | Very high: active topic views, conference/year indexes, and a recent-paper inbox reaching the current month/year. | Mostly historical/practical material, with many paper entries concentrated around 2014-2020 and older TensorFlow-era tools. |
| Best coverage | Robot foundation models, self-improvement, world-action models, human video, dexterity, visual RL, 3D robot learning, and diffusion. | Middleware, calibration, SLAM, classical geometry/control, drivers, logging, simulators, datasets, and early grasping/manipulation. |
| Main risk | High-volume inbox, duplicates across topic views, volatile preprints, websites without paper metadata, and unreviewed very recent claims. | Stale or inactive projects, mixed official/third-party links, broken/bare URLs, and uneven paper metadata. |
| Best use | Discover current research candidates and emerging topic clusters. | Discover durable systems prerequisites and historical implementation surfaces. |

Use the two sources together: Paper-List proposes new research directions; Awesome Robotics checks whether the curriculum is neglecting the systems, calibration, geometry, and tooling needed to make those methods work on robots.

## What not to treat as authoritative

- Do not cite this list for technical claims, benchmark numbers, publication status, authors, dates, or licenses.
- “Recent Random Papers” is an inbox, not a quality ranking; recency and inclusion are not evidence of importance or correctness.
- Topic membership and ordering are curator judgments, not a formal ontology.
- A project website may omit peer-review status, negative results, licensing, or later corrections; resolve the canonical paper record separately.
- arXiv labels and listed years can become stale after revisions or publication; verify the current record and final venue.
- Websites, code, datasets, and model weights may have different licenses. Verify every artifact independently before download or redistribution.
- Duplicate entries across topic files should become one canonical backlog record, not multiple cards.
- For 2026-era or otherwise very recent leads, require an extra verification gate: paper identity, author/project ownership, artifact availability, evaluation protocol, and reproducibility evidence.

