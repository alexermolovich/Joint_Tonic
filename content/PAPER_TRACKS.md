# Paper implementation tracks

Every canonical paper in the current research library has an original implementation plan. The plans reuse the reviewed explanation flows and component mappings; they do not add unreviewed problem names to the approved curriculum roadmap automatically.

**156 paper tracks from 157 source cards; 475 source-flow stages and 319 connections represented.** The duplicate Open X-Embodiment topic card is retained inside one canonical track.

Runnable exercises already have published problem packages. Supporting prerequisites are labeled separately. Proposed component names, synthetic integrations and assessments remain unavailable until blueprints, implementations and isolated grading are complete. Counts are a planning snapshot; live pages resolve current published problem status.

[Curriculum](../CURRICULUM.md) · [Research library](../research/README.md) · [Paper component map](../research/FLOW_PROBLEM_MAP.md)

## Track completion contract

1. Read the original explanation, define the physical/data contract and pass the prerequisite diagnostic.
2. Implement atomic mechanisms in the source flow, preserving the input/output and dependency semantics.
3. Compose the proposed small synthetic integration after its own blueprint review.
4. Evaluate an independent oracle and at least one attributed failure case.
5. Produce a reproducibility/model card with lineage, compute, data, versions and deviations.

## Tracks by topic

### Geometry, calibration and SLAM — 16

| Paper track | Runnable components | Supporting prerequisites | Proposed components | Source stages |
|---|---:|---:|---:|---:|
| [A General Optimization-based Framework for Global Pose Estimation with Multiple Sensors](tracks/papers/paper-2019-vins-fusion.md) | 0 | 0 | 4 | 3 |
| [A micro Lie theory for state estimation in robotics](tracks/papers/paper-2018-micro-lie-theory.md) | 1 | 5 | 0 | 3 |
| [BundleFusion: Real-time Globally Consistent 3D Reconstruction using On-the-fly Surface Re-integration](tracks/papers/paper-2016-bundlefusion.md) | 0 | 0 | 4 | 3 |
| [Direct Sparse Odometry](tracks/papers/paper-2016-direct-sparse-odometry.md) | 3 | 0 | 0 | 3 |
| [DROID-SLAM: Deep Visual SLAM for Monocular, Stereo, and RGB-D Cameras](tracks/papers/paper-2021-droid-slam.md) | 0 | 0 | 4 | 3 |
| [FAST-LIO2: Fast Direct LiDAR-inertial Odometry](tracks/papers/paper-2021-fast-lio-2.md) | 2 | 0 | 2 | 3 |
| [iMAP: Implicit Mapping and Positioning in Real-Time](tracks/papers/paper-2021-imap.md) | 0 | 1 | 4 | 3 |
| [LIO-SAM: Tightly-coupled Lidar Inertial Odometry via Smoothing and Mapping](tracks/papers/paper-2020-lio-sam.md) | 2 | 2 | 2 | 3 |
| [LoFTR: Detector-Free Local Feature Matching with Transformers](tracks/papers/paper-2021-loftr.md) | 4 | 0 | 0 | 3 |
| [NICE-SLAM: Neural Implicit Scalable Encoding for SLAM](tracks/papers/paper-2021-nice-slam.md) | 0 | 0 | 4 | 3 |
| [On-Manifold Preintegration for Real-Time Visual-Inertial Odometry](tracks/papers/paper-2015-on-manifold-preintegration.md) | 3 | 2 | 1 | 3 |
| [ORB-SLAM2: an Open-Source SLAM System for Monocular, Stereo and RGB-D Cameras](tracks/papers/paper-2016-orb-slam-2.md) | 0 | 0 | 3 | 3 |
| [ORB-SLAM3: An Accurate Open-Source Library for Visual, Visual-Inertial and Multi-Map SLAM](tracks/papers/paper-2020-orb-slam-3.md) | 0 | 0 | 4 | 3 |
| [SuperGlue: Learning Feature Matching with Graph Neural Networks](tracks/papers/paper-2019-superglue.md) | 4 | 0 | 0 | 3 |
| [SuperPoint: Self-Supervised Interest Point Detection and Description](tracks/papers/paper-2017-superpoint.md) | 4 | 0 | 0 | 3 |
| [VINS-Mono: A Robust and Versatile Monocular Visual-Inertial State Estimator](tracks/papers/paper-2017-vins-mono.md) | 0 | 2 | 4 | 3 |

### Planning, control and inverse kinematics — 13

| Paper track | Runnable components | Supporting prerequisites | Proposed components | Source stages |
|---|---:|---:|---:|---:|
| [Continuous-Time Gaussian Process Motion Planning via Probabilistic Inference](tracks/papers/paper-2017-gaussian-process-motion-planning.md) | 3 | 0 | 0 | 3 |
| [cuRobo: Parallelized Collision-Free Minimum-Jerk Robot Motion Generation](tracks/papers/paper-2023-curobo.md) | 2 | 2 | 1 | 3 |
| [Diffusion-ES: Gradient-free Planning with Diffusion for Autonomous Driving and Zero-Shot Instruction Following](tracks/papers/paper-2024-diffusion-es.md) | 0 | 0 | 4 | 3 |
| [IK-Geo: Unified Robot Inverse Kinematics Using Subproblem Decomposition](tracks/papers/paper-2022-ik-geo.md) | 0 | 3 | 4 | 3 |
| [IKFlow: Generating Diverse Inverse Kinematics Solutions](tracks/papers/paper-2021-ikflow.md) | 0 | 0 | 5 | 3 |
| [Incremental Sampling-based Algorithms for Optimal Motion Planning](tracks/papers/paper-2010-rrt-star.md) | 4 | 0 | 0 | 3 |
| [Jerk-limited Real-time Trajectory Generation with Arbitrary Target States](tracks/papers/paper-2021-ruckig.md) | 2 | 2 | 1 | 3 |
| [Model Predictive Path Integral Control using Covariance Variable Importance Sampling](tracks/papers/paper-2015-path-integral-mpc.md) | 3 | 0 | 0 | 3 |
| [Motion Planning Diffusion: Learning and Planning of Robot Motions with Diffusion Models](tracks/papers/paper-2023-motion-planning-diffusion.md) | 0 | 1 | 2 | 3 |
| [Motion Planning Networks](tracks/papers/paper-2018-motion-planning-networks.md) | 0 | 0 | 3 | 3 |
| [Motion Planning with Sequential Convex Optimization and Convex Collision Checking](tracks/papers/paper-2014-trajopt.md) | 3 | 2 | 0 | 3 |
| [Planning with Diffusion for Flexible Behavior Synthesis](tracks/papers/paper-2022-diffuser.md) | 0 | 3 | 3 | 3 |
| [RMPflow: A Computational Graph for Automatic Motion Policy Generation](tracks/papers/paper-2018-rmpflow.md) | 3 | 0 | 0 | 3 |

### Vision, VLM and 3D foundations — 10

| Paper track | Runnable components | Supporting prerequisites | Proposed components | Source stages |
|---|---:|---:|---:|---:|
| [An Image is Worth 16x16 Words: Transformers for Image Recognition at Scale](tracks/papers/paper-2021-vision-transformer.md) | 6 | 0 | 0 | 3 |
| [BEVFormer: Learning Bird's-Eye-View Representation from Multi-Camera Images via Spatiotemporal Transformers](tracks/papers/paper-2022-bevformer.md) | 7 | 2 | 0 | 3 |
| [DINOv2: Learning Robust Visual Features without Supervision](tracks/papers/paper-2023-dinov2.md) | 6 | 0 | 0 | 3 |
| [End-to-End Object Detection with Transformers](tracks/papers/paper-2020-detr.md) | 7 | 0 | 0 | 3 |
| [Grounding DINO: Marrying DINO with Grounded Pre-Training for Open-Set Object Detection](tracks/papers/paper-2023-grounding-dino.md) | 6 | 0 | 0 | 3 |
| [Learning Transferable Visual Models From Natural Language Supervision](tracks/papers/paper-2021-clip.md) | 5 | 0 | 0 | 3 |
| [NeRF: Representing Scenes as Neural Radiance Fields for View Synthesis](tracks/papers/paper-2020-nerf.md) | 9 | 0 | 0 | 3 |
| [PointNet: Deep Learning on Point Sets for 3D Classification and Segmentation](tracks/papers/paper-2017-pointnet.md) | 5 | 0 | 0 | 3 |
| [Segment Anything](tracks/papers/paper-2023-segment-anything.md) | 7 | 0 | 0 | 3 |
| [You Only Look Once: Unified, Real-Time Object Detection](tracks/papers/paper-2016-yolo-v1.md) | 7 | 0 | 0 | 3 |

### Perception and 3D representations — 13

| Paper track | Runnable components | Supporting prerequisites | Proposed components | Source stages |
|---|---:|---:|---:|---:|
| [3D Gaussian Splatting for Real-Time Radiance Field Rendering](tracks/papers/paper-2023-3d-gaussian-splatting.md) | 0 | 0 | 4 | 3 |
| [Depth Anything V2](tracks/papers/paper-2024-depth-anything-v2.md) | 0 | 0 | 4 | 3 |
| [Faster R-CNN: Towards Real-Time Object Detection with Region Proposal Networks](tracks/papers/paper-2015-faster-r-cnn.md) | 0 | 2 | 4 | 3 |
| [Feature Pyramid Networks for Object Detection](tracks/papers/paper-2016-feature-pyramid-networks.md) | 0 | 0 | 4 | 3 |
| [Focal Loss for Dense Object Detection](tracks/papers/paper-2017-focal-loss-retinanet.md) | 0 | 0 | 4 | 3 |
| [Mask R-CNN](tracks/papers/paper-2017-mask-r-cnn.md) | 0 | 0 | 4 | 3 |
| [Masked Autoencoders Are Scalable Vision Learners](tracks/papers/paper-2021-masked-autoencoders.md) | 0 | 2 | 3 | 3 |
| [PointNet++: Deep Hierarchical Feature Learning on Point Sets in a Metric Space](tracks/papers/paper-2017-pointnet-plus-plus.md) | 0 | 0 | 3 | 3 |
| [RAFT: Recurrent All-Pairs Field Transforms for Optical Flow](tracks/papers/paper-2020-raft.md) | 0 | 0 | 3 | 3 |
| [SAM 2: Segment Anything in Images and Videos](tracks/papers/paper-2024-sam-2.md) | 0 | 0 | 4 | 3 |
| [SSD: Single Shot MultiBox Detector](tracks/papers/paper-2015-ssd.md) | 0 | 2 | 3 | 3 |
| [Vision Transformers for Dense Prediction](tracks/papers/paper-2021-dense-prediction-transformers.md) | 0 | 0 | 4 | 3 |
| [YOLOv3: An Incremental Improvement](tracks/papers/paper-2018-yolov3.md) | 0 | 4 | 3 | 3 |

### Vision-language models and grounding — 13

| Paper track | Runnable components | Supporting prerequisites | Proposed components | Source stages |
|---|---:|---:|---:|---:|
| [BLIP-2: Bootstrapping Language-Image Pre-training with Frozen Image Encoders and Large Language Models](tracks/papers/paper-2023-blip-2.md) | 0 | 0 | 3 | 3 |
| [BLIP: Bootstrapping Language-Image Pre-training for Unified Vision-Language Understanding and Generation](tracks/papers/paper-2022-blip.md) | 0 | 1 | 3 | 3 |
| [Flamingo: a Visual Language Model for Few-Shot Learning](tracks/papers/paper-2022-flamingo.md) | 0 | 0 | 3 | 3 |
| [Florence-2: Advancing a Unified Representation for a Variety of Vision Tasks](tracks/papers/paper-2023-florence-2.md) | 0 | 0 | 3 | 3 |
| [Grounded Language-Image Pre-training](tracks/papers/paper-2021-glip.md) | 0 | 0 | 4 | 3 |
| [Kosmos-2: Grounding Multimodal Large Language Models to the World](tracks/papers/paper-2023-kosmos-2.md) | 0 | 0 | 3 | 3 |
| [PaLI-3 Vision Language Models: Smaller, Faster, Stronger](tracks/papers/paper-2023-pali-3.md) | 0 | 0 | 4 | 3 |
| [PaLI: A Jointly-Scaled Multilingual Language-Image Model](tracks/papers/paper-2022-pali.md) | 0 | 0 | 3 | 3 |
| [PaliGemma: A versatile 3B VLM for transfer](tracks/papers/paper-2024-paligemma.md) | 0 | 0 | 4 | 3 |
| [Scaling Up Visual and Vision-Language Representation Learning With Noisy Text Supervision](tracks/papers/paper-2021-align.md) | 0 | 3 | 3 | 3 |
| [Sigmoid Loss for Language Image Pre-Training](tracks/papers/paper-2023-siglip.md) | 0 | 0 | 3 | 3 |
| [Simple Open-Vocabulary Object Detection with Vision Transformers](tracks/papers/paper-2022-owl-vit.md) | 0 | 0 | 4 | 3 |
| [Visual Instruction Tuning](tracks/papers/paper-2023-llava.md) | 0 | 0 | 4 | 3 |

### VLA and embodied policy foundations — 9

| Paper track | Runnable components | Supporting prerequisites | Proposed components | Source stages |
|---|---:|---:|---:|---:|
| [$\pi_0$: A Vision-Language-Action Flow Model for General Robot Control](tracks/papers/paper-2024-pi0.md) | 5 | 0 | 0 | 3 |
| [Diffusion Policy: Visuomotor Policy Learning via Action Diffusion](tracks/papers/paper-2023-diffusion-policy.md) | 7 | 0 | 0 | 6 |
| [GR00T N1: An Open Foundation Model for Generalist Humanoid Robots](tracks/papers/paper-2025-gr00t-n1.md) | 5 | 1 | 0 | 3 |
| [Learning Fine-Grained Bimanual Manipulation with Low-Cost Hardware](tracks/papers/paper-2023-aloha-act.md) | 5 | 0 | 0 | 3 |
| [Octo: An Open-Source Generalist Robot Policy](tracks/papers/paper-2024-octo.md) | 5 | 2 | 0 | 3 |
| [OpenVLA: An Open-Source Vision-Language-Action Model](tracks/papers/paper-2024-openvla.md) | 5 | 2 | 0 | 3 |
| [PaLM-E: An Embodied Multimodal Language Model](tracks/papers/paper-2023-palm-e.md) | 5 | 0 | 0 | 3 |
| [RT-1: Robotics Transformer for Real-World Control at Scale](tracks/papers/paper-2022-rt-1.md) | 5 | 0 | 0 | 3 |
| [RT-2: Vision-Language-Action Models Transfer Web Knowledge to Robotic Control](tracks/papers/paper-2023-rt-2.md) | 5 | 1 | 0 | 3 |

### Generalist VLA policies and interfaces — 11

| Paper track | Runnable components | Supporting prerequisites | Proposed components | Source stages |
|---|---:|---:|---:|---:|
| [$\pi_{0.5}$: a Vision-Language-Action Model with Open-World Generalization](tracks/papers/paper-2025-pi0-5.md) | 0 | 0 | 3 | 3 |
| [A Generalist Agent](tracks/papers/paper-2022-gato.md) | 0 | 0 | 3 | 3 |
| [Code as Policies: Language Model Programs for Embodied Control](tracks/papers/paper-2022-code-as-policies.md) | 0 | 1 | 3 | 3 |
| [Do As I Can, Not As I Say: Grounding Language in Robotic Affordances](tracks/papers/paper-2022-saycan.md) | 0 | 0 | 4 | 3 |
| [FAST: Efficient Action Tokenization for Vision-Language-Action Models](tracks/papers/paper-2025-fast-action-tokenization.md) | 0 | 0 | 3 | 3 |
| [Fine-Tuning Vision-Language-Action Models: Optimizing Speed and Success](tracks/papers/paper-2025-openvla-oft.md) | 0 | 1 | 3 | 3 |
| [RoboCat: A Self-Improving Generalist Agent for Robotic Manipulation](tracks/papers/paper-2023-robocat.md) | 0 | 1 | 3 | 3 |
| [RT-H: Action Hierarchies Using Language](tracks/papers/paper-2024-rt-h.md) | 0 | 0 | 3 | 3 |
| [SmolVLA: A Vision-Language-Action Model for Affordable and Efficient Robotics](tracks/papers/paper-2025-smolvla.md) | 0 | 1 | 4 | 3 |
| [TinyVLA: Towards Fast, Data-Efficient Vision-Language-Action Models for Robotic Manipulation](tracks/papers/paper-2024-tinyvla.md) | 0 | 1 | 3 | 3 |
| [VIMA: General Robot Manipulation with Multimodal Prompts](tracks/papers/paper-2022-vima.md) | 0 | 0 | 3 | 3 |

### Robot learning, imitation and reinforcement learning — 19

| Paper track | Runnable components | Supporting prerequisites | Proposed components | Source stages |
|---|---:|---:|---:|---:|
| [3D Diffusion Policy: Generalizable Visuomotor Policy Learning via Simple 3D Representations](tracks/papers/paper-2024-3d-diffusion-policy.md) | 0 | 5 | 3 | 3 |
| [CLIPort: What and Where Pathways for Robotic Manipulation](tracks/papers/paper-2021-cliport.md) | 0 | 0 | 5 | 3 |
| [Conservative Q-Learning for Offline Reinforcement Learning](tracks/papers/paper-2020-conservative-q-learning.md) | 3 | 1 | 0 | 3 |
| [Dex-Net 2.0: Deep Learning to Plan Robust Grasps with Synthetic Point Clouds and Analytic Grasp Metrics](tracks/papers/paper-2017-dex-net-2.md) | 0 | 0 | 5 | 3 |
| [DrEureka: Language Model Guided Sim-To-Real Transfer](tracks/papers/paper-2024-dr-eureka.md) | 2 | 3 | 0 | 3 |
| [Eureka: Human-Level Reward Design via Coding Large Language Models](tracks/papers/paper-2023-eureka.md) | 3 | 1 | 0 | 3 |
| [Image Augmentation Is All You Need: Regularizing Deep Reinforcement Learning from Pixels](tracks/papers/paper-2020-data-regularized-q.md) | 3 | 1 | 0 | 3 |
| [Mastering Diverse Domains through World Models](tracks/papers/paper-2023-dreamerv3.md) | 4 | 0 | 0 | 3 |
| [Mobile ALOHA: Learning Bimanual Mobile Manipulation with Low-Cost Whole-Body Teleoperation](tracks/papers/paper-2024-mobile-aloha.md) | 0 | 8 | 1 | 3 |
| [Offline Reinforcement Learning with Implicit Q-Learning](tracks/papers/paper-2021-implicit-q-learning.md) | 4 | 0 | 0 | 3 |
| [Perceiver-Actor: A Multi-Task Transformer for Robotic Manipulation](tracks/papers/paper-2022-peract.md) | 0 | 0 | 3 | 3 |
| [Precise and Dexterous Robotic Manipulation via Human-in-the-Loop Reinforcement Learning](tracks/papers/paper-2024-hil-serl.md) | 0 | 1 | 3 | 3 |
| [Proximal Policy Optimization Algorithms](tracks/papers/paper-2017-proximal-policy-optimization.md) | 5 | 0 | 0 | 4 |
| [R3M: A Universal Visual Representation for Robot Manipulation](tracks/papers/paper-2022-r3m.md) | 0 | 0 | 3 | 3 |
| [SERL: A Software Suite for Sample-Efficient Robotic Reinforcement Learning](tracks/papers/paper-2024-serl.md) | 0 | 1 | 4 | 3 |
| [Soft Actor-Critic: Off-Policy Maximum Entropy Deep Reinforcement Learning with a Stochastic Actor](tracks/papers/paper-2018-soft-actor-critic.md) | 4 | 0 | 0 | 3 |
| [TD-MPC2: Scalable, Robust World Models for Continuous Control](tracks/papers/paper-2023-td-mpc2.md) | 5 | 0 | 0 | 3 |
| [Transporter Networks: Rearranging the Visual World for Robotic Manipulation](tracks/papers/paper-2020-transporter-networks.md) | 0 | 0 | 3 | 3 |
| [Universal Manipulation Interface: In-The-Wild Robot Teaching Without In-The-Wild Robots](tracks/papers/paper-2024-umi.md) | 0 | 1 | 3 | 3 |

### Locomotion, dexterity and tactile sensing — 9

| Paper track | Runnable components | Supporting prerequisites | Proposed components | Source stages |
|---|---:|---:|---:|---:|
| [AMP: Adversarial Motion Priors for Stylized Physics-Based Character Control](tracks/papers/paper-2021-adversarial-motion-priors.md) | 3 | 0 | 0 | 3 |
| [DeepMimic: Example-Guided Deep Reinforcement Learning of Physics-Based Character Skills](tracks/papers/paper-2018-deepmimic.md) | 4 | 0 | 0 | 3 |
| [DexMV: Imitation Learning for Dexterous Manipulation from Human Videos](tracks/papers/paper-2021-dexmv.md) | 0 | 0 | 5 | 3 |
| [DexPoint: Generalizable Point Cloud Reinforcement Learning for Sim-to-Real Dexterous Manipulation](tracks/papers/paper-2022-dexpoint.md) | 0 | 2 | 3 | 3 |
| [DIGIT: A Novel Design for a Low-Cost Compact High-Resolution Tactile Sensor with Application to In-Hand Manipulation](tracks/papers/paper-2020-digit-tactile-sensor.md) | 5 | 2 | 0 | 3 |
| [Learning Dexterous In-Hand Manipulation](tracks/papers/paper-2018-learning-dexterous-manipulation.md) | 0 | 1 | 3 | 3 |
| [Learning robust perceptive locomotion for quadrupedal robots in the wild](tracks/papers/paper-2022-perceptive-locomotion.md) | 0 | 0 | 5 | 3 |
| [Learning to Walk in Minutes Using Massively Parallel Deep Reinforcement Learning](tracks/papers/paper-2021-learning-to-walk-in-minutes.md) | 0 | 3 | 3 | 3 |
| [RMA: Rapid Motor Adaptation for Legged Robots](tracks/papers/paper-2021-rapid-motor-adaptation.md) | 5 | 0 | 0 | 3 |

### Data, deployment and evaluation systems — 18

| Paper track | Runnable components | Supporting prerequisites | Proposed components | Source stages |
|---|---:|---:|---:|---:|
| [AWQ: Activation-aware Weight Quantization for LLM Compression and Acceleration](tracks/papers/paper-2023-awq.md) | 2 | 2 | 0 | 3 |
| [BridgeData V2: A Dataset for Robot Learning at Scale](tracks/papers/paper-2023-bridgedata-v2.md) | 0 | 2 | 2 | 3 |
| [CALVIN: A Benchmark for Language-Conditioned Policy Learning for Long-Horizon Robot Manipulation Tasks](tracks/papers/paper-2021-calvin.md) | 0 | 1 | 3 | 3 |
| [Datasheets for Datasets](tracks/papers/paper-2018-datasheets-for-datasets.md) | 2 | 3 | 1 | 3 |
| [Deep Compression: Compressing Deep Neural Networks with Pruning, Trained Quantization and Huffman Coding](tracks/papers/paper-2015-deep-compression.md) | 3 | 1 | 0 | 3 |
| [Deep Reinforcement Learning at the Edge of the Statistical Precipice](tracks/papers/paper-2021-rliable-statistical-precipice.md) | 0 | 3 | 2 | 3 |
| [DROID: A Large-Scale In-The-Wild Robot Manipulation Dataset](tracks/papers/paper-2024-droid.md) | 2 | 1 | 1 | 3 |
| [Ego-Exo4D: Understanding Skilled Human Activity from First- and Third-Person Perspectives](tracks/papers/paper-2023-ego-exo4d.md) | 0 | 2 | 4 | 3 |
| [Ego4D: Around the World in 3,000 Hours of Egocentric Video](tracks/papers/paper-2021-ego4d.md) | 0 | 0 | 3 | 3 |
| [LIBERO: Benchmarking Knowledge Transfer for Lifelong Robot Learning](tracks/papers/paper-2023-libero.md) | 0 | 0 | 4 | 3 |
| [Model Cards for Model Reporting](tracks/papers/paper-2018-model-cards.md) | 1 | 2 | 1 | 3 |
| [Ray: A Distributed Framework for Emerging AI Applications](tracks/papers/paper-2017-ray.md) | 2 | 1 | 0 | 3 |
| [RLDS: an Ecosystem to Generate, Share and Use Datasets in Reinforcement Learning](tracks/papers/paper-2021-rlds.md) | 0 | 6 | 0 | 3 |
| [RLlib: Abstractions for Distributed Reinforcement Learning](tracks/papers/paper-2017-rllib.md) | 2 | 4 | 2 | 3 |
| [RoboCasa: Large-Scale Simulation of Everyday Tasks for Generalist Robots](tracks/papers/paper-2024-robocasa.md) | 0 | 2 | 4 | 3 |
| [RoboNet: Large-Scale Multi-Robot Learning](tracks/papers/paper-2019-robonet.md) | 0 | 5 | 3 | 3 |
| [RoboTurk: A Crowdsourcing Platform for Robotic Skill Learning through Imitation](tracks/papers/paper-2018-roboturk.md) | 1 | 6 | 3 | 3 |
| [SmoothQuant: Accurate and Efficient Post-Training Quantization for Large Language Models](tracks/papers/paper-2022-smoothquant.md) | 5 | 1 | 0 | 3 |

### Robotics MLOps and sim-to-real foundations — 12

| Paper track | Runnable components | Supporting prerequisites | Proposed components | Source stages |
|---|---:|---:|---:|---:|
| [Data Validation for Machine Learning](tracks/papers/paper-2019-data-validation-for-ml.md) | 6 | 0 | 0 | 3 |
| [Domain Randomization for Transferring Deep Neural Networks from Simulation to the Real World](tracks/papers/paper-2017-domain-randomization.md) | 5 | 0 | 1 | 3 |
| [Hidden Technical Debt in Machine Learning Systems](tracks/papers/paper-2015-hidden-technical-debt.md) | 2 | 2 | 0 | 3 |
| [MLPerf Inference Benchmark](tracks/papers/paper-2019-mlperf-inference.md) | 4 | 0 | 1 | 3 |
| [Once-for-All: Train One Network and Specialize it for Efficient Deployment](tracks/papers/paper-2020-once-for-all.md) | 4 | 1 | 0 | 3 |
| [Open X-Embodiment: Robotic Learning Datasets and RT-X Models](tracks/papers/paper-2024-open-x-embodiment.md) | 11 | 0 | 0 | 6 |
| [RobotPerf: An Open-Source, Vendor-Agnostic, Benchmarking Suite for Evaluating Robotics Computing System Performance](tracks/papers/paper-2023-robotperf.md) | 3 | 2 | 1 | 3 |
| [Sim-to-Real Transfer of Robotic Control with Dynamics Randomization](tracks/papers/paper-2018-dynamics-randomization.md) | 5 | 1 | 0 | 3 |
| [TFX: A TensorFlow-Based Production-Scale Machine Learning Platform](tracks/papers/paper-2017-tfx-production-ml-platform.md) | 5 | 4 | 0 | 3 |
| [The ML Test Score: A Rubric for ML Production Readiness and Technical Debt Reduction](tracks/papers/paper-2017-ml-test-score.md) | 4 | 1 | 0 | 3 |
| [TVM: An Automated End-to-End Optimizing Compiler for Deep Learning](tracks/papers/paper-2018-tvm.md) | 3 | 0 | 1 | 3 |
| [What Matters in Learning from Offline Human Demonstrations for Robot Manipulation](tracks/papers/paper-2021-robomimic.md) | 5 | 2 | 1 | 3 |

### Simulation, benchmarks and transfer — 13

| Paper track | Runnable components | Supporting prerequisites | Proposed components | Source stages |
|---|---:|---:|---:|---:|
| [AI2-THOR: An Interactive 3D Environment for Visual AI](tracks/papers/paper-2017-ai2thor.md) | 0 | 2 | 3 | 3 |
| [Brax -- A Differentiable Physics Engine for Large Scale Rigid Body Simulation](tracks/papers/paper-2021-brax.md) | 0 | 0 | 3 | 3 |
| [DeepMind Control Suite](tracks/papers/paper-2018-deepmind-control-suite.md) | 0 | 0 | 4 | 3 |
| [Habitat 2.0: Training Home Assistants to Rearrange their Habitat](tracks/papers/paper-2021-habitat-2.md) | 0 | 2 | 4 | 3 |
| [Habitat 3.0: A Co-Habitat for Humans, Avatars and Robots](tracks/papers/paper-2023-habitat-3.md) | 0 | 2 | 3 | 3 |
| [Habitat: A Platform for Embodied AI Research](tracks/papers/paper-2019-habitat.md) | 0 | 1 | 3 | 3 |
| [iGibson 1.0: a Simulation Environment for Interactive Tasks in Large Realistic Scenes](tracks/papers/paper-2020-igibson.md) | 0 | 3 | 3 | 3 |
| [Isaac Gym: High Performance GPU-Based Physics Simulation For Robot Learning](tracks/papers/paper-2021-isaac-gym.md) | 0 | 2 | 3 | 3 |
| [ManiSkill: Generalizable Manipulation Skill Benchmark with Large-Scale Demonstrations](tracks/papers/paper-2021-maniskill.md) | 0 | 2 | 4 | 3 |
| [ManiSkill2: A Unified Benchmark for Generalizable Manipulation Skills](tracks/papers/paper-2023-maniskill-2.md) | 0 | 4 | 4 | 3 |
| [RLBench: The Robot Learning Benchmark & Learning Environment](tracks/papers/paper-2019-rlbench.md) | 0 | 4 | 3 | 3 |
| [robosuite: A Modular Simulation Framework and Benchmark for Robot Learning](tracks/papers/paper-2020-robosuite.md) | 0 | 1 | 4 | 3 |
| [SAPIEN: A SimulAted Part-based Interactive ENvironment](tracks/papers/paper-2020-sapien.md) | 0 | 5 | 4 | 3 |

## Maintenance

A paper is deduplicated by its trimmed canonical primary URL with one trailing slash removed, matching the website catalog. Source-card aliases remain linked from the canonical plan. Each source-flow node appears under its stable card/node ID so later implementation can promote an exact proposed task without losing paper-to-code traceability.

These plans and this index are generated. Edit source-card flows for component mappings and the original proposal recipes in [generate-paper-tracks.ts](../scripts/generate-paper-tracks.ts) for integration/assessment changes before refreshing. Preserve authored changes by incorporating them into the generator first.

Refresh with: node --experimental-strip-types scripts/generate-paper-tracks.ts

Validate coverage, stage associations, status labels and links with: node --experimental-strip-types scripts/validate-paper-tracks.ts

Refresh plans when a source flow or published component changes. New independent problems still require the repository blueprint and review gates; a plan is not permission to skip provenance, theory, fixture or evaluator requirements.
