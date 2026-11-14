# Awesome Robotics discovery audit

- **Discovery repository:** [https://github.com/ahundt/awesome-robotics](https://github.com/ahundt/awesome-robotics)
- **Accessed:** 2026-11-13
- **Role:** Secondary discovery index for papers, datasets, libraries, simulators, and robotics infrastructure. It is not a bibliographic or licensing authority.
- **Corpus comparison:** Leads below were checked by title against the current 32 local paper cards. None is already represented as a paper card.

## Useful taxonomy

The repository's most useful contribution is its broad robotics-systems taxonomy:

- simulators and physics;
- visualization, logging, and messaging;
- tracking and Robot Operating System infrastructure;
- kinematics, dynamics, constrained optimization, and trajectory generation;
- camera/IMU and hand-eye calibration;
- reinforcement learning and guided policy search;
- sensor/device/arm drivers;
- robotics, grasping, and perception datasets;
- dataset collection and label-generation pipelines;
- linear algebra, Lie groups, geometry, and point-cloud tooling;
- dense, object-aware, and classical SLAM;
- a separate paper index spanning manipulation, grasping, reinforcement learning, and language-conditioned robots.

This taxonomy fills practical gaps in Joint Tonic's initial paper-centric corpus. Its weakness is that papers, author projects, third-party implementations, datasets, and generic libraries are mixed at the same level.

## Discovery backlog

Priority meanings: **P1** = first post-MVP card candidates; **P2** = next expansion; **P3** = useful later; **ecosystem** = link from theory/problems but normally do not make a paper card unless a canonical paper is identified.

### Manipulation, grasping, and geometric perception

| Lead | Link exactly as listed | Why it fills a gap | Verification | Suggested priority |
|---|---|---|---|---|
| Transporter Networks | [https://transporternets.github.io/](https://transporternets.github.io/) | Teachable pick/place correlation, spatial action maps, closed-loop manipulation, and Ravens tasks. | **Primary-source verified:** official project page links the CoRL 2020 paper and author code. | **P1 paper card** |
| Ravens simulator code | [https://github.com/google-research/google-research/tree/master/ravens](https://github.com/google-research/google-research/tree/master/ravens) | Small manipulation-task suite with scripted demonstrations and rewards; useful fixtures for problem evaluation. | **Needs primary-source verification:** verify the maintained code location, license, and dataset/task versions before adoption. | **ecosystem, P1 fixture review** |
| Dex-Net 2.0 | [https://arxiv.org/pdf/1703.09312.pdf](https://arxiv.org/pdf/1703.09312.pdf) | Connects synthetic depth data, analytic grasp labels, grasp-quality prediction, and sim-to-real evaluation. | **Primary-source verified:** official arXiv record independently checked. | **P1 paper card** |
| PointNet++ | [http://stanford.edu/~rqi/pointnet2/](http://stanford.edu/~rqi/pointnet2/) | Extends the existing PointNet card with local neighborhoods, hierarchical sampling, and density robustness. | **Primary-source verified:** author/Stanford project page links paper, code, and data. | **P1 paper card** |
| Dense Object Nets | [https://github.com/RobotLocomotion/pytorch-dense-correspondence](https://github.com/RobotLocomotion/pytorch-dense-correspondence) | Dense descriptors and correspondence are a useful bridge from perception to manipulation. | **Needs primary-source verification:** confirm the canonical paper, author ownership, release status, and license. | **P2 paper card** |
| Good Robot! | [https://arxiv.org/abs/1909.11730](https://arxiv.org/abs/1909.11730) | Adds long-horizon visual RL, progress reversal, safety zones, and direct sim-to-real transfer. | **Primary-source verified:** official arXiv record independently checked. | **P2 paper card** |
| Concept2Robot | [http://www.roboticsproceedings.org/rss16/p082.pdf](http://www.roboticsproceedings.org/rss16/p082.pdf) | Earlier language/instruction-to-manipulation work complements the VLA track historically. | **Needs primary-source verification:** verify proceedings metadata, the final version, and any official code/data. | **P3 historical card** |

### Data and label pipelines

| Lead | Link exactly as listed | Why it fills a gap | Verification | Suggested priority |
|---|---|---|---|---|
| LabelFusion code | [https://github.com/RobotLocomotion/LabelFusion](https://github.com/RobotLocomotion/LabelFusion) | A concrete RGB-D ground-truth generation pipeline; strong material for lineage and annotation QA problems. | **Primary-source verified:** project repository independently checked; still verify the canonical paper/version before making a card. | **P1 pipeline/card** |
| CoSTAR Block Stacking Dataset | [https://sites.google.com/site/costardataset](https://sites.google.com/site/costardataset) | Robot stacking demonstrations can support small manipulation fixtures and sequence-evaluation tasks. | **Needs primary-source verification:** confirm availability, schema, license, and citation. | **P2 dataset review** |
| ShapeStacks | [http://shapestacks.robots.ox.ac.uk/#paper](http://shapestacks.robots.ox.ac.uk/#paper) | Adds physical stability reasoning and simulated stacks beyond generic vision datasets. | **Needs primary-source verification:** confirm current hosting, canonical paper, terms, and downloadable artifacts. | **P2 dataset/card** |
| Google Brain Robot Data | [https://sites.google.com/site/brainrobotdata/home](https://sites.google.com/site/brainrobotdata/home) | Historical grasping, pushing, and pouring data may help show dataset evolution. | **Needs primary-source verification:** confirm exact constituent datasets, licenses, and whether the link remains complete. | **P3 historical dataset review** |

### State estimation, calibration, and mapping

| Lead | Link exactly as listed | Why it fills a gap | Verification | Suggested priority |
|---|---|---|---|---|
| Kalibr | [https://github.com/ethz-asl/kalibr](https://github.com/ethz-asl/kalibr) | Camera/IMU calibration is a prerequisite for multi-camera BEV, SLAM, and robot sensor reproducibility. | **Primary-source verified:** official ETH ASL toolbox repository independently checked. | **P1 systems card** |
| ORB-SLAM2 | [https://github.com/raulmur/ORB_SLAM2](https://github.com/raulmur/ORB_SLAM2) | Adds feature tracking, map points, loop closure, relocalization, and multi-sensor evaluation. | **Primary-source verified:** author repository independently checked. | **P1 paper/system card** |
| ElasticFusion | [https://github.com/mp3guy/ElasticFusion](https://github.com/mp3guy/ElasticFusion) | Adds real-time dense RGB-D mapping and surfel fusion, missing from the NeRF-oriented 3D set. | **Primary-source verified:** author repository independently checked; verify final paper record before card creation. | **P2 paper/system card** |
| Co-Fusion | [https://github.com/martinruenz/co-fusion](https://github.com/martinruenz/co-fusion) | Dynamic multi-object segmentation, tracking, and reconstruction extend static-scene assumptions. | **Needs primary-source verification:** confirm official authorship, canonical paper, buildability, and dataset licenses. | **P2 paper card** |
| OctoMap | [https://github.com/OctoMap/octomap](https://github.com/OctoMap/octomap) | Probabilistic octree occupancy is highly teachable and useful for planning/perception interfaces. | **Needs primary-source verification:** verify the canonical paper and official release documentation. | **P2 paper/system card** |

### RL infrastructure and production-facing robotics

| Lead | Link exactly as listed | Why it fills a gap | Verification | Suggested priority |
|---|---|---|---|---|
| Acme | [https://arxiv.org/abs/2006.00979](https://arxiv.org/abs/2006.00979) | Adds modular distributed actor/learner design, reproducible RL components, and scale-aware experimentation. | **Primary-source verified:** official arXiv record independently checked. | **P2 MLOps paper card** |
| RL Unplugged | [https://arxiv.org/pdf/2006.13888.pdf](https://arxiv.org/pdf/2006.13888.pdf) | Adds offline-RL dataset protocols and reproducible benchmark design, useful for safe physical-AI evaluation. | **Primary-source verified:** official arXiv record independently checked. | **P2 benchmark card** |
| ROS 2 design | [https://github.com/ros2/design](https://github.com/ros2/design) | Useful reference for middleware QoS, distributed nodes, and deployment contracts. | **Needs primary-source verification:** confirm which design documents are current and normative. | **ecosystem** |
| LCM | [https://github.com/lcm-proj/lcm](https://github.com/lcm-proj/lcm) | Lightweight typed messaging and log replay can support deterministic robotics data-pipeline exercises. | **Needs primary-source verification:** verify maintained docs, schema guarantees, and licensing. | **ecosystem** |
| PlotJuggler | [https://github.com/facontidavide/PlotJuggler](https://github.com/facontidavide/PlotJuggler) | Practical time-series inspection for robot telemetry and incident analysis. | **Needs primary-source verification:** verify maintained project/release and supported data sources. | **ecosystem** |
| Ruckig | [https://github.com/pantor/ruckig](https://github.com/pantor/ruckig) | Jerk-constrained online trajectory generation is a strong deterministic optimization/problem track. | **Needs primary-source verification:** confirm canonical paper, current API, and licensing. | **P2 system/problem track** |

## Recommended additions after the 10-problem MVP

Do not expand all of these at once. The first post-MVP wave should add five complementary surfaces:

1. **PointNet++** - local 3D grouping and sampling problems that naturally follow the existing PointNet track.
2. **Transporter Networks + Ravens review** - a compact, visually teachable manipulation track.
3. **Dex-Net 2.0** - synthetic data generation, analytic labels, and grasp-quality evaluation.
4. **Kalibr** - calibration and sensor-data validation problems that strengthen BEV/3D work.
5. **ORB-SLAM2** - tracking, pose, loop-closure, and map-evaluation components.

After that, add LabelFusion and one offline/distributed RL card (RL Unplugged or Acme). Keep ROS 2, LCM, PlotJuggler, and similar libraries as ecosystem references unless a problem track is explicitly about system integration.

## What not to treat as authoritative

- Do not cite this awesome list for technical claims, metrics, publication status, author lists, dates, or licenses.
- A GitHub link is not proof that a repository is the official implementation; some entries are forks or third-party ports.
- The repository explicitly warns that implementations may not be actively developed and may not be author-maintained.
- Several links are bare domains, HTTP-only pages, old TensorFlow-era tooling, or historical sites; availability and security must be rechecked.
- The repository's CC BY 4.0 license covers the list, not the linked papers, datasets, models, or code.
- Descriptions such as “state of the art,” dataset sizes, and performance numbers must be verified in the canonical paper/project.
- Before creating a paper card, resolve a canonical landing page, final publication/preprint version, license/redistribution terms, and an unambiguous title/author record.

