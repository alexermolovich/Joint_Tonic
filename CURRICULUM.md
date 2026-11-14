# Joint Tonic curriculum tree

**Status:** Original 190 problems and four bounded capstones implemented; paper-library expansion underway
**Version:** 1.0.0
**Legend:** `[foundation]` is paper-independent, `[paper]` is derived from a checked-in paper card, and `[systems]` is an operational scenario. Every named problem in sections 1–4 now maps to a reviewed runnable package in [the implementation index](content/AUTHORING_STATUS.md). Section 5 has four bounded runnable integrations. Reviewed paper-library additions appear in section 7; other proposed flow ideas remain in the explicit backlog.

This is the single navigational tree for topics, tracks, and named problems. It describes practical components to implement; it does not imply full reproduction of every paper. Each future problem begins as a Markdown file based on `research/templates/problem-blueprint.md`.

Baseline inventory: **190 implemented named problems** across **38 topic/track groups**, plus three supporting exercises. The catalog has grown to **372 runnable packages** at this release checkpoint: 175 reviewed paper additions and four bounded capstone integrations extend the baseline. `MVP_10.md` retains the original vertical-slice commitment. See [baseline verification](content/CURRICULUM_COMPLETION.md) and [release work](docs/RELEASE_PLAN.md).

The original ten launch problems are grouped in three local learning paths: **Build YOLO Detection Components** (five geometry/perception problems), **Build VLM & VLA Components** (three alignment/action/diffusion problems), and **Validate Robot Datasets & Edge Models** (two MLOps problems). These names describe implemented components; they do not imply full model training or paper reproduction. Stable route slugs remain `robot-perception-foundations`, `vision-to-action`, and `robot-mlops`.

The learner-facing **Projects** catalog presents the paper corpus in nine topic sheets: Computer vision & perception; Vision-language-action models; Robotics MLOps & datasets; Geometry, calibration & SLAM; Planning, control & kinematics; Robot learning & reinforcement learning; Vision-language grounding; Manipulation, humanoids & touch; and Simulation & sim-to-real. These are navigation groups over the existing paper folders, not additional implemented tracks. Each project retains its source paper ID and links to the available component problems. Cards without a reviewed model explanation remain marked in preparation.

## 1. Shared physical-AI foundations

### 1.1 Tensors, numerics, and evaluation

- `[foundation]` Broadcast Batched Sensor Features
- `[foundation]` Stable Softmax for Masked Sequences
- `[foundation]` Finite-Difference Gradient Check
- `[foundation]` Seed a Deterministic Evaluation Run
- `[foundation]` Compute Confidence Intervals Across Robot Episodes
- `[foundation]` Compare Slice Metrics Without Hiding Regressions

### 1.2 Geometry and calibration

- `[foundation]` Apply an SE(3) Transform to Batched Points
- `[foundation]` Compose and Invert Coordinate Transforms
- `[foundation]` Normalize and Multiply Quaternions
- `[foundation]` Interpolate a Pose with SLERP
- `[foundation]` Project Camera Points into Pixels
- `[foundation]` Unproject a Depth Map into a Point Cloud
- `[foundation]` Apply Radial and Tangential Lens Distortion
- `[foundation]` Validate a Camera Calibration Matrix
- `[foundation]` Solve a Small Hand-Eye Calibration Residual
- `[foundation]` Trace Frames Through a Robot Perception Graph

### 1.3 Kinematics and inverse kinematics

Simulator problems in this group use the Robot View contract in `SPEC.md`, with MuJoCo as the local baseline and Isaac Sim as an optional higher-fidelity backend.

- `[foundation]` Interpolate Franka FR3 Joint Waypoints
- `[foundation]` Compute Forward Kinematics for a Serial Chain
- `[foundation]` Solve Closed-Form IK for a Planar Two-Link Arm
- `[foundation]` Compute a Geometric Jacobian from Joint Axes
- `[foundation]` Solve IK with a Jacobian Pseudoinverse
- `[foundation]` Stabilize Singular IK with Damped Least Squares
- `[foundation]` Enforce Joint Limits and Collision Constraints in IK

### 1.4 Time and multimodal sensor alignment

- `[foundation]` Interpolate Joint State at Camera Time
- `[foundation]` Match Approximate Sensor Timestamps
- `[foundation]` Detect Dropped and Duplicated Sensor Frames
- `[foundation]` Estimate Clock Offset from Paired Events
- `[foundation]` Window an Episode Without Crossing Boundaries
- `[foundation]` Build Padding and Validity Masks for Robot Sequences

### 1.5 State estimation

- `[foundation]` One Kalman Filter Predict Step
- `[foundation]` One Kalman Filter Measurement Update
- `[foundation]` Gate Measurements with Mahalanobis Distance
- `[foundation]` Normalize and Resample Particle Weights
- `[foundation]` Update Occupancy Grid Log Odds
- `[foundation]` Fuse Asynchronous Position and Velocity Sensors

### 1.6 Planning and control

- `[foundation]` PID with Integral Anti-Windup
- `[foundation]` Interpolate a Time-Parameterized Trajectory
- `[foundation]` Check a Segment Against Occupancy Cells
- `[foundation]` Compute a Differential-Drive Rollout
- `[foundation]` Evaluate an MPC Tracking Cost
- `[foundation]` Enforce Velocity and Acceleration Limits

## 2. Vision, VLM, and 3D perception

### 2.1 Detection foundations — YOLO v1

Paper card: `research/papers/vision-vlm-3d/2016-yolo-v1.md`

- `[paper]` Decode YOLO Grid Predictions into Image Boxes
- `[paper]` Assign Ground-Truth Objects to Responsible Cells
- `[paper]` Compute YOLO Coordinate, Objectness, and Class Losses
- `[paper]` Run Class-Aware Non-Maximum Suppression
- `[paper]` Evaluate Detection with IoU, Precision-Recall, and mAP
- `[systems]` Benchmark Detector Accuracy Against Edge Latency

### 2.2 Set prediction — DETR

Paper card: `research/papers/vision-vlm-3d/2020-detr.md`

- `[paper]` Build a Detection Bipartite-Matching Cost Matrix
- `[paper]` Match Object Queries with the Hungarian Algorithm
- `[paper]` Compute DETR Classification, L1, and GIoU Losses
- `[paper]` Handle the No-Object Class and Padding Masks
- `[systems]` Diagnose Query Collapse and Missed Small Objects

### 2.3 Tokenized vision — Vision Transformer

Paper card: `research/papers/vision-vlm-3d/2021-vision-transformer.md`

- `[paper]` Patchify and Reconstruct an Image Tensor
- `[paper]` Build Learned Patch and Class Tokens
- `[paper]` Interpolate 2D Positional Embeddings
- `[paper]` Assemble a Pre-Norm Vision Transformer Block
- `[systems]` Profile Token Count, Memory, and Latency by Resolution

### 2.4 Vision-language alignment — CLIP

Paper card: `research/papers/vision-vlm-3d/2021-clip.md`

- `[paper]` Normalize Image and Text Embeddings
- `[paper]` Compute Symmetric Contrastive Loss
- `[paper]` Build a Prompt-Ensembled Zero-Shot Classifier
- `[paper]` Evaluate Cross-Modal Retrieval Recall at K
- `[systems]` Detect Prompt and Class Distribution Drift

### 2.5 Promptable and open-world perception — SAM and Grounding DINO

Paper cards: `research/papers/vision-vlm-3d/2023-segment-anything.md`, `research/papers/vision-vlm-3d/2023-grounding-dino.md`

- `[paper]` Encode Positive and Negative Point Prompts
- `[paper]` Encode a Box Prompt with Positional Features
- `[paper]` Rank Candidate Masks with Predicted IoU
- `[paper]` Filter Automatic Masks by Stability and Overlap
- `[paper]` Map Text Tokens to Grounded Phrases
- `[paper]` Select Language-Guided Object Queries
- `[paper]` Decode Phrase-Labeled Boxes
- `[systems]` Build a Grounded Segmentation Pipeline and Trace Failures

### 2.6 Self-supervised visual features — DINOv2

Paper card: `research/papers/vision-vlm-3d/2023-dinov2.md`

- `[paper]` Update a Teacher Encoder with Exponential Moving Average
- `[paper]` Center and Sharpen Teacher Probabilities
- `[paper]` Combine Class-Token and Masked-Patch Objectives
- `[paper]` Evaluate Frozen Features with k-NN
- `[systems]` Monitor Frozen-Feature Drift Across Camera Domains

### 2.7 Point-cloud learning — PointNet

Paper card: `research/papers/vision-vlm-3d/2017-pointnet.md`

- `[paper]` Prove Permutation Invariance with Symmetric Pooling
- `[paper]` Build a Shared Point MLP and Global Feature
- `[paper]` Concatenate Local and Global Features for Segmentation
- `[paper]` Regularize a Learned Feature Transform
- `[systems]` Validate Point-Cloud Density and Coordinate Conventions

### 2.8 Neural rendering — NeRF

Paper card: `research/papers/vision-vlm-3d/2020-nerf.md`

- `[paper]` Generate Calibrated Camera Rays
- `[paper]` Stratify Samples Along Near and Far Bounds
- `[paper]` Encode 3D Positions with Fourier Features
- `[paper]` Compute Transmittance and Alpha Compositing Weights
- `[paper]` Render Color and Expected Depth Along a Ray
- `[systems]` Detect Bad Poses with Reprojection and Render Residuals

### 2.9 Multi-camera BEV — BEVFormer

Paper card: `research/papers/vision-vlm-3d/2022-bevformer.md`

- `[paper]` Project BEV Reference Points into Calibrated Cameras
- `[paper]` Mask Out-of-View and Behind-Camera Samples
- `[paper]` Aggregate Multi-Camera Features with Attention Weights
- `[paper]` Warp a Previous BEV with Ego Motion
- `[paper]` Fuse Temporal BEV State
- `[systems]` Diagnose Camera Dropout and Calibration Drift in BEV

## 3. VLA and embodied robot learning

### 3.1 Tokenized robot policies — RT-1

Paper card: `research/papers/vla-embodied/2022-rt-1.md`

- `[paper]` Quantize and Dequantize Continuous Robot Actions
- `[paper]` Select Compact Visual Tokens with Learned Attention
- `[paper]` Build a Causal Action-Token Mask
- `[paper]` Sample a Task-Balanced Trajectory Batch
- `[systems]` Measure Closed-Loop Latency and Action Dropouts

### 3.2 Action chunking — ACT/ALOHA

Paper card: `research/papers/vla-embodied/2023-aloha-act.md`

- `[paper]` Build Sliding Action Chunks with Padding Masks
- `[paper]` Compute a Masked CVAE Reconstruction and KL Loss
- `[paper]` Blend Overlapping Action Chunks with Temporal Ensembling
- `[paper]` Evaluate Chunk Length Against Compounding Error
- `[systems]` Detect Teleoperation Demonstration Quality Failures

### 3.3 Diffusion actions — Diffusion Policy

Paper card: `research/papers/vla-embodied/2023-diffusion-policy.md`

- `[paper]` Add Noise to an Action Sequence
- `[paper]` Compute a Conditional Noise-Prediction Loss
- `[paper]` Sample an Action Trajectory with DDPM Steps
- `[paper]` Execute a Receding-Horizon Action Window
- `[systems]` Budget Denoising Steps Against Control Frequency

### 3.4 Embodied multimodal tokens — PaLM-E

Paper card: `research/papers/vla-embodied/2023-palm-e.md`

- `[paper]` Project Continuous Sensor Features into Language Width
- `[paper]` Interleave Image, State, and Text Tokens
- `[paper]` Build a Multimodal Causal Attention Mask
- `[paper]` Collate Variable Multimodal Sequences
- `[systems]` Validate Missing-Modality and Stale-Sensor Inputs

### 3.5 Actions as language — RT-2

Paper card: `research/papers/vla-embodied/2023-rt-2.md`

- `[paper]` Serialize Robot Actions as Discrete Tokens
- `[paper]` Parse and Validate an Action-Token Grammar
- `[paper]` Mix Web and Robot Batches at a Target Ratio
- `[paper]` Constrain Autoregressive Decoding to Valid Actions
- `[systems]` Monitor Invalid Actions and Semantic Generalization Slices

### 3.6 Cross-embodiment data — Open X-Embodiment / RT-X

Paper card: `research/papers/vla-embodied/2023-open-x-embodiment.md`

- `[paper]` Normalize Heterogeneous Robot Observation Schemas
- `[paper]` Normalize and Mask Embodiment-Specific Action Spaces
- `[paper]` Sample a Balanced Multi-Dataset Mixture
- `[paper]` Compute Per-Embodiment and Transfer Metrics
- `[systems]` Version a Cross-Robot Dataset Manifest

### 3.7 Adaptable generalist policy — Octo

Paper card: `research/papers/vla-embodied/2024-octo.md`

- `[paper]` Assemble Observation and Task Token Groups
- `[paper]` Build Block Masks for Missing Sensors and Goals
- `[paper]` Route Tokens into Dataset-Specific Action Heads
- `[paper]` Add a Frozen-Backbone Adaptation Module
- `[systems]` Verify Trainable Parameters and Fine-Tuning Artifacts

### 3.8 Open VLA engineering — OpenVLA

Paper card: `research/papers/vla-embodied/2024-openvla.md`

- `[paper]` Fuse Two Visual Feature Streams Safely
- `[paper]` Quantize Actions from Training-Set Quantiles
- `[paper]` Build a VLA Action-Token Training Batch
- `[paper]` Add Low-Rank Adaptation to a Policy Layer
- `[systems]` Estimate Memory, Latency, and Quantized Serving Budgets

### 3.9 Continuous flow actions — $\pi_0$

Paper card: `research/papers/vla-embodied/2024-pi0.md`

- `[paper]` Sample Flow-Matching Action Interpolants and Targets
- `[paper]` Build Block Attention for VLM and Action Expert Tokens
- `[paper]` Integrate an Action Flow with Euler Steps
- `[paper]` Evaluate Solver Steps Against Trajectory Error
- `[systems]` Monitor Continuous-Action Range and Smoothness Drift

### 3.10 Humanoid foundation policy — GR00T N1

Paper card: `research/papers/vla-embodied/2025-gr00t-n1.md`

- `[paper]` Route Inputs Through a Dual-System Policy Interface
- `[paper]` Build a Heterogeneous Real, Video, and Synthetic Batch
- `[paper]` Compute a Masked Action Flow-Matching Loss
- `[paper]` Report Metrics by Source and Embodiment
- `[systems]` Gate a Humanoid Policy Release on Safety Slices

## 4. Robotics MLOps, deployment, and sim-to-real

### 4.1 ML systems debt and production readiness

Paper cards: `research/papers/mlops-sim2real/2015-hidden-technical-debt.md`, `research/papers/mlops-sim2real/2017-ml-test-score.md`

- `[paper]` Compute Dependency-Graph Blast Radius
- `[paper]` Detect Feedback Loops in an ML Pipeline
- `[paper]` Score a Robot ML System for Production Readiness
- `[paper]` Gate a Release on Slice and Infrastructure Tests
- `[systems]` Triage a Physical-AI Deployment Incident

### 4.2 Continuous training and artifact lineage — TFX

Paper card: `research/papers/mlops-sim2real/2017-tfx-production-ml-platform.md`

- `[paper]` Topologically Schedule a Training Pipeline DAG
- `[paper]` Record Dataset, Transform, Model, and Evaluator Lineage
- `[paper]` Invalidate Cached Artifacts After an Upstream Change
- `[paper]` Detect Training-Serving Transform Skew
- `[systems]` Reproduce a Model from an Immutable Run Manifest

### 4.3 Robot data validation

Paper card: `research/papers/mlops-sim2real/2019-data-validation-for-ml.md`

- `[paper]` Infer a Schema from Robot Episodes
- `[paper]` Detect Missing, Range, Domain, and Shape Anomalies
- `[paper]` Compare Training and Serving Distributions
- `[paper]` Detect Sensor Timestamp and Calibration Skew
- `[systems]` Block a Pipeline on Critical Data Anomalies

### 4.4 Offline demonstrations — robomimic

Paper card: `research/papers/mlops-sim2real/2021-robomimic.md`

- `[paper]` Split Robot Trajectories Without Scene Leakage
- `[paper]` Batch Variable-Length Episodes with Masks
- `[paper]` Compare Validation Loss with Rollout Success
- `[paper]` Report Performance by Demonstration Quality
- `[systems]` Select a Checkpoint with Offline and Rollout Gates

### 4.5 Cross-robot data operations — Open X-Embodiment

Paper card: `research/papers/mlops-sim2real/2024-open-x-embodiment.md`

- `[paper]` Map Robot-Specific Data into a Shared Episode Schema
- `[paper]` Balance a Multi-Dataset Training Mixture
- `[paper]` Mask Unavailable Action Dimensions
- `[paper]` Build a Per-Embodiment Transfer Matrix
- `[systems]` Detect Dataset-Version and Schema Drift

### 4.6 Inference benchmarking — MLPerf and RobotPerf

Paper cards: `research/papers/mlops-sim2real/2019-mlperf-inference.md`, `research/papers/mlops-sim2real/2023-robotperf.md`

- `[paper]` Compute p50, p90, and p99 Inference Latency
- `[paper]` Simulate Single-Stream and Server Load
- `[paper]` Reject Invalid Benchmark Runs
- `[paper]` Derive End-to-End Latency from Robotics Trace Events
- `[paper]` Measure Throughput and Jitter Across a ROS-Style Graph
- `[systems]` Compare Black-Box and Grey-Box Pipeline Measurements

### 4.7 Portable edge optimization — TVM and Once-for-All

Paper cards: `research/papers/mlops-sim2real/2018-tvm.md`, `research/papers/mlops-sim2real/2020-once-for-all.md`

- `[paper]` Fuse Compatible Operators in a Compute Graph
- `[paper]` Search Tensor Tile Sizes with a Toy Cost Model
- `[paper]` Reuse Tensor Buffers with Liveness Analysis
- `[paper]` Extract a Depth, Width, and Kernel Subnetwork
- `[paper]` Sample a Progressive-Shrinking Curriculum
- `[paper]` Select a Pareto Model Under Accuracy and Latency Limits
- `[systems]` Package and Verify an Edge Model Artifact

### 4.8 Visual domain randomization

Paper card: `research/papers/mlops-sim2real/2017-domain-randomization.md`

- `[paper]` Build a Seeded Visual Randomization Sampler
- `[paper]` Stratify Texture, Lighting, Camera, and Distractor Factors
- `[paper]` Measure Performance Across Shift Buckets
- `[paper]` Estimate Scenario Coverage and Confidence Intervals
- `[systems]` Version a Simulation Scenario Distribution

### 4.9 Dynamics randomization

Paper card: `research/papers/mlops-sim2real/2018-dynamics-randomization.md`

- `[paper]` Sample Mass, Friction, Delay, and Gain Distributions
- `[paper]` Aggregate Mean and Worst-Case Policy Returns
- `[paper]` Quantify Calibration Sensitivity
- `[paper]` Choose Randomization Bounds from Safety Constraints
- `[systems]` Gate Sim-to-Real Release with Robustness Evidence

## 5. Cross-paper capstone tracks

All four now have runnable bounded integrations, evaluation cases and reproducibility templates. Open [the capstone catalog](/projects/capstones). These synthetic projects do not reproduce the full underlying trained models or establish real-robot release safety.

### 5.1 Grounded robot perception

Integration: [Build a Grounded Robot Perception Pipeline](content/problems/capstone-grounded-perception/problem.md).

1. `[foundation]` Calibrated image and transform contracts.
2. `[paper]` Open-vocabulary boxes from Grounding DINO.
3. `[paper]` Promptable masks from SAM.
4. `[paper]` Temporal/multi-camera fusion into BEV.
5. `[systems]` Latency, calibration-drift, and scenario-slice evaluation.
6. `[systems]` Package, canary, monitor, and rollback the perception graph.

### 5.2 Production-ready VLA

Integration: [Build and Evaluate a Bounded VLA Release](content/problems/capstone-vla-release/problem.md). The title of this track describes the learning path; its fixture is a small frozen-feature adapter and action-codec exercise.

1. `[foundation]` Validate and window multimodal robot episodes.
2. `[paper]` Normalize cross-embodiment observations and actions.
3. `[paper]` Implement discrete-token or continuous-flow action generation.
4. `[paper]` Adapt a frozen policy with a bounded trainable module.
5. `[systems]` Evaluate per-task, per-embodiment, latency, and invalid-action slices.
6. `[systems]` Build an immutable release manifest and monitored canary gate.

### 5.3 Edge perception deployment

Integration: [Package and Gate an Edge Perception Release](content/problems/capstone-edge-deployment/problem.md).

1. `[paper]` Define a valid latency/quality benchmark.
2. `[paper]` Optimize compute graph and buffer reuse.
3. `[paper]` Select a hardware-aware subnet/model configuration.
4. `[systems]` Package a signed model and preprocessing contract.
5. `[systems]` Trace a robotics graph for latency and jitter.
6. `[systems]` Detect drift and roll back safely.

### 5.4 Sim-to-real reliability

Integration: [Evaluate Sim-to-Real Release Evidence](content/problems/capstone-sim-to-real/problem.md).

1. `[paper]` Version visual and dynamics factor distributions.
2. `[paper]` Generate stratified, deterministic scenarios.
3. `[paper]` Evaluate mean, tail, worst-case, and confidence intervals.
4. `[systems]` Compare simulator, replay, shadow, and real-robot slices.
5. `[systems]` Produce a release evidence report with known gaps.

## 6. Paper-specific implementation tracks

The Tracks catalog now includes a track plan for every canonical paper in the research library, alongside the three introductory paths. The complete topic-grouped tree is maintained in [Paper tracks](content/PAPER_TRACKS.md); each entry links to its original Markdown plan in `content/tracks/papers/` and its local website route `/tracks/paper-{paper-id}`.

Tracks follow the paper's explained execution stages. Runnable exercises link to versioned coding problems; proposed components remain visibly pending until their contracts and evaluators are reviewed. Every plan identifies prerequisites, an ordered component sequence, a small proposed integration, evaluation/failure analysis, and a reproducibility/MLOps deliverable. Completing available components does not imply completing the planned integration or reproducing headline paper results.

Coverage spans perception, vision-language grounding, VLA, geometry/SLAM, planning/control, robot learning, manipulation/tactile sensing, MLOps/data, and simulation. The component inventory and associations are in [the full paper-to-code map](research/FLOW_PROBLEM_MAP.md). These track plans organize the existing research backlog; proposed ideas do not silently become additions to the 190 approved roadmap candidates above.

<!-- reviewed-expansion:start -->

## 7. Reviewed paper-library expansion

The user authorized the remaining paper backlog after the original 190-problem curriculum. This generated section lists reviewed additions with published evaluators. The complete proposed inventory and source associations remain in [the implementation backlog](research/IMPLEMENTATION_BACKLOG.md); a proposed title is not a completed exercise.

### 7.1 Robot Learning

- `[paper]` Compute the Clipped Policy Surrogate
- `[paper]` Normalize Batched Advantages
- `[paper]` Report Policy Update Clip Fractions
- `[paper]` Compute Value Targets Across Episode Boundaries
- `[paper]` Compute an Entropy-Regularized State Value
- `[paper]` Compute an Entropy-Regularized Bellman Target
- `[paper]` Apply Tanh Action Log-Probability Correction
- `[paper]` Update a Temperature Objective (later SAC extension)
- `[paper]` Compute an Expectile Regression Loss
- `[paper]` Build Advantage-Weighted Action Weights
- `[paper]` Validate an Offline Dataset Split
- `[paper]` Train and Evaluate a Tiny PPO Joint Controller
- `[paper]` Compute a Conservative Q Penalty
- `[paper]` Compare Logged and Sampled Action Values
- `[paper]` Evaluate Offline Policy Support
- `[paper]` Apply a Seeded Random-Shift Augmentation
- `[paper]` Average Augmented Bellman Targets
- `[paper]` Compute a Multi-View Critic Regression Loss
- `[paper]` Interpolate a Reference Motion Pose
- `[paper]` Detect Phase Misalignment in a Motion Clip
- `[paper]` Compute Pose and Velocity Imitation Rewards
- `[paper]` Combine Motion and Task Rewards
- `[paper]` Construct Motion Discriminator Features
- `[paper]` Compute an Adversarial Style Reward
- `[paper]` Build Privileged Dynamics-Latent Supervision
- `[paper]` Window Proprioceptive History
- `[paper]` Estimate a Latent Dynamics Context
- `[paper]` Track the Age of an Asynchronous Adaptation Latent
- `[paper]` Evaluate Policy Recovery After a Parameter Change
- `[paper]` Validate a Reward Function Contract
- `[paper]` Aggregate Reward-Component Diagnostics
- `[paper]` Rank Reward Candidates by Rollout Evidence
- `[paper]` Validate a Generated Reward Program
- `[paper]` Compare Robustness Across Randomization Settings
- `[paper]` Compute a Balanced Latent-Model Loss
- `[paper]` Encode Symlog Two-Hot Reward Targets
- `[paper]` Build Lambda-Return Targets
- `[paper]` Roll Out Imagined Latent Trajectories
- `[paper]` Apply Groupwise SimNorm to Latent States
- `[paper]` Roll Out a Latent Dynamics Sequence
- `[paper]` Build Distributional Reward and Ensemble-Value Targets
- `[paper]` Score Candidate Action Trajectories
- `[paper]` Update a Sampling-Based Planner
- `[paper]` Validate Success-Classifier Rewards on Robot Failures
- `[paper]` Merge Online and Demonstration Replay
- `[paper]` Schedule Actor-Learner Updates
- `[paper]` Label Human Intervention Segments
- `[paper]` Mix Intervention and Autonomous Replay
- `[paper]` Gate an Online Policy Update
- `[paper]` Record Intervention and Reset Statistics
- `[paper]` Sample Time-Contrastive Video Triplets
- `[paper]` Combine Temporal and Language Alignment Losses
- `[paper]` Evaluate Frozen Features in a Small Policy
- `[paper]` Compute Gait Tracking and Stability Metrics
- `[paper]` Reset Failed Locomotion Environments
- `[paper]` Sample Terrain Difficulty by Policy Progress
- `[paper]` Compute Belief Reconstruction and Teacher-Action Losses
- `[paper]` Evaluate Foot Clearance Across Terrain Slices

### 7.2 Tactile Manipulation

- `[paper]` Validate a Tactile Image Capture Contract
- `[paper]` Subtract a Tactile Reference Image
- `[paper]` Estimate Contact Patch Statistics
- `[paper]` Align Tactile Frames with Robot Actions
- `[paper]` Score Predicted Tactile Contact Outcomes

### 7.3 Planning, control and geometry

- `[paper]` Integrate a Constant-Jerk Motion Segment
- `[paper]` Validate a Trajectory Against Derivative Limits
- `[paper]` Build a Joint-Space Smoothness Cost
- `[paper]` Compute a Signed-Distance Collision Cost
- `[paper]` Linearize a Signed-Distance Collision Penalty
- `[paper]` Bound a Sequential Convex Trust-Region Step
- `[paper]` Normalize Exponential Trajectory Cost Weights
- `[paper]` Update a Receding-Horizon Control Sequence
- `[paper]` Find Nearby Planning Tree Vertices
- `[paper]` Choose a Collision-Free Minimum-Cost Tree Parent
- `[paper]` Roll Out Perturbed Control Sequences
- `[paper]` Rewire a Tree Without Creating Cycles
- `[paper]` Compare Path Cost Across Sampling Budgets
- `[paper]` Build a Gaussian-Process Smoothness Factor
- `[paper]` Assemble Obstacle and Prior Residuals
- `[paper]` Interpolate a Trajectory Between Support States
- `[paper]` Push Robot State into a Task Space
- `[paper]` Pull Back a Local Motion Metric
- `[paper]` Combine Competing Task-Space Accelerations
- `[paper]` Rank Multi-Seed Motion Trajectories

### 7.4 Geometry and state estimation

- `[paper]` Select High-Gradient Image Points
- `[paper]` Warp a Point Between Calibrated Frames
- `[paper]` Compute an Exposure-Corrected Photometric Residual
- `[paper]` Compute Point-to-Line and Point-to-Plane Scan Residuals
- `[paper]` Associate Scan Points with Local Map Planes
- `[paper]` Deskew a Lidar Scan with Motion Estimates
- `[paper]` Apply SE(3) Exponential and Logarithm Maps
- `[paper]` Integrate IMU Rotation Increments on SO3
- `[paper]` Preintegrate Bias-Corrected IMU Velocity and Position
- `[paper]` Apply a First-Order Bias Correction
- `[paper]` Apply Homographic Keypoint Adaptation
- `[paper]` Evaluate Keypoint Repeatability
- `[paper]` Build Homography-Supervised Descriptor Correspondence Targets
- `[paper]` Sample Descriptors at Keypoint Coordinates
- `[paper]` Build a Feature-Matching Score Matrix
- `[paper]` Normalize Assignments with Sinkhorn Iterations
- `[paper]` Reject Unmatched Features with Dustbins
- `[paper]` Extract Mutual Matches and Unmatched Labels from Transport Scores
- `[paper]` Apply Paired-Image Self and Cross Attention
- `[paper]` Construct Coarse Correspondence Candidates
- `[paper]` Refine a Match in a Local Window
- `[paper]` Filter Geometrically Inconsistent Matches
- `[paper]` Detect Unobservable Initialization Motion
- `[paper]` Preintegrate a Short IMU Window
- `[paper]` Build a Visual-Inertial Residual
- `[paper]` Marginalize a Visual-Inertial Window with a Schur Complement
- `[paper]` Associate Map Points with Image Features
- `[paper]` Select Geometric Pose Inliers
- `[paper]` Evaluate a Relocalization Candidate
- `[paper]` Evaluate Trajectory Error After Alignment
- `[paper]` Construct Relative Pose Measurements from Local Odometry
- `[paper]` Assemble Sensor-Specific Pose Factors
- `[paper]` Compare Drift Across Sensor Configurations
- `[paper]` Propagate Preintegration Covariance
- `[paper]` Assemble an IMU-Lidar Pose Constraint
- `[paper]` Reject Inconsistent Loop Closures
- `[paper]` Update an Incremental Local Map
- `[paper]` Validate a Visual-Inertial Initialization

### 7.5 Robotics MLOps

- `[paper]` Measure Per-Channel Activation and Weight Ranges
- `[paper]` Apply an Equivalent Channel Rescaling
- `[paper]` Quantize Weights and Activations to Int8
- `[paper]` Validate Layer Output Error After Smoothing
- `[paper]` Apply a Weight-Pruning Mask
- `[paper]` Quantize Shared Weight Centroids
- `[paper]` Compute a Compressed Model Storage Budget
- `[paper]` Compare Activation-Weighted Quantization Error
- `[paper]` Compute Group-Wise Quantization Parameters
- `[paper]` Calibrate and Evaluate a Smoothed Int8 Layer
- `[paper]` Recover Failed Worker Tasks Idempotently
- `[paper]` Track Immutable Artifact References
- `[paper]` Track Policy Version Staleness
- `[paper]` Aggregate Weighted Learner Gradients
- `[paper]` Split Demonstrations by Scene and Collector
- `[paper]` Audit Data and Calibration Lineage
- `[paper]` Validate a Robot Dataset Datasheet
- `[paper]` Generate a Data-Use Risk Report
- `[paper]` Validate a Model Card Schema
- `[paper]` Detect Paused or Corrupted Action Segments
- `[paper]` Compute an Interquartile Mean Benchmark Score
- `[paper]` Bootstrap a Stratified Performance Profile
- `[paper]` Validate a Continuous-Control Time Step
- `[paper]` Implement Action Repeat Correctly
- `[paper]` Evaluate a Bounded Continuous-Control Reward
- `[paper]` Aggregate Seeded Benchmark Returns
- `[paper]` Batch Independent Simulator States
- `[paper]` Reset Completed Environments Selectively
- `[paper]` Measure Simulation and Learning Throughput
- `[paper]` Implement a Functional Physics Step Contract
- `[paper]` Build a Continual-Learning Task Sequence
- `[paper]` Separate Task Semantics from Scene Variation
- `[paper]` Record a Continual-Learning Evaluation Matrix
- `[paper]` Compute a Forward and Backward Transfer Matrix
- `[paper]` Align Actions and Images in a Video Window
- `[paper]` Compute a Masked Video-Prediction Loss
- `[paper]` Measure Cross-Robot Prediction Error
- `[paper]` Align Egocentric Video Annotations
- `[paper]` Build Leakage-Safe Temporal Splits
- `[paper]` Aggregate Evaluation by Activity Slice

### 7.6 Perception

- `[paper]` Decode Normalized Boxes and Classes from Object Queries
- `[paper]` Flatten Spatial Features with Position and Padding Metadata
- `[paper]` Read a Normalized Class Token with a Linear Head
- `[paper]` Transform Prompt Coordinates Through Image Preprocessing
- `[paper]` Reuse Image Embeddings Without Stale-Cache Errors
- `[paper]` Sample Calibrated Multi-Camera Feature Maps
- `[paper]` Sample Hierarchical Depth Intervals
- `[paper]` Differentiate Rendered Color on a Small Synthetic Field
- `[paper]` Implement Nearest-Neighbor Feature-Spreading Regularization
- `[paper]` Fit a Tiny Coordinate-Feature Radiance Field

### 7.7 VLM & VLA

- `[paper]` Fuse Masked Image and Text Tokens with Bidirectional Cross-Attention
- `[paper]` Evaluate Localization and Phrase Grounding Separately
- `[paper]` Encode Synchronized Observations for an Action Denoiser
- `[paper]` Build a Conditional Action Denoiser

<!-- reviewed-expansion:end -->

## 8. Maintenance rules

- Add a named problem here when its paper card contains enough evidence to define a practical contract.
- A name becomes an implementation commitment only after a problem-blueprint Markdown file is reviewed.
- Keep problem names verb-led and concrete; avoid generic titles such as “Implement Paper X.”
- Prefer small reusable components that can compose into capstones.
- Every paper track includes at least one evaluation/failure-analysis problem and one MLOps/deployment problem.
- The research-curator agent updates this tree when adding or retiring paper cards.
