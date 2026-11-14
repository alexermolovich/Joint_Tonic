# Joint Tonic curriculum tree

**Status:** Named implementation roadmap  
**Version:** 0.1.0  
**Legend:** `[foundation]` is paper-independent, `[paper]` is derived from a checked-in paper card, `[systems]` is an operational scenario, and all entries are **planned** until a completed problem blueprint says otherwise.

This is the single navigational tree for topics, tracks, and named problems. It describes practical components to implement; it does not imply full reproduction of every paper. Each future problem begins as a Markdown file based on `research/templates/problem-blueprint.md`.

Current inventory: **189 named problems** across **38 topic/track groups**, plus four ordered cross-paper capstone sequences. The immediate implementation subset is defined in `MVP_10.md`.

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
- `[paper]` Compute a Diffusion-Transformer Action-Chunk Loss
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

### 5.1 Grounded robot perception

1. `[foundation]` Calibrated image and transform contracts.
2. `[paper]` Open-vocabulary boxes from Grounding DINO.
3. `[paper]` Promptable masks from SAM.
4. `[paper]` Temporal/multi-camera fusion into BEV.
5. `[systems]` Latency, calibration-drift, and scenario-slice evaluation.
6. `[systems]` Package, canary, monitor, and rollback the perception graph.

### 5.2 Production-ready VLA

1. `[foundation]` Validate and window multimodal robot episodes.
2. `[paper]` Normalize cross-embodiment observations and actions.
3. `[paper]` Implement discrete-token or continuous-flow action generation.
4. `[paper]` Adapt a frozen policy with a bounded trainable module.
5. `[systems]` Evaluate per-task, per-embodiment, latency, and invalid-action slices.
6. `[systems]` Build an immutable release manifest and monitored canary gate.

### 5.3 Edge perception deployment

1. `[paper]` Define a valid latency/quality benchmark.
2. `[paper]` Optimize compute graph and buffer reuse.
3. `[paper]` Select a hardware-aware subnet/model configuration.
4. `[systems]` Package a signed model and preprocessing contract.
5. `[systems]` Trace a robotics graph for latency and jitter.
6. `[systems]` Detect drift and roll back safely.

### 5.4 Sim-to-real reliability

1. `[paper]` Version visual and dynamics factor distributions.
2. `[paper]` Generate stratified, deterministic scenarios.
3. `[paper]` Evaluate mean, tail, worst-case, and confidence intervals.
4. `[systems]` Compare simulator, replay, shadow, and real-robot slices.
5. `[systems]` Produce a release evidence report with known gaps.

## 6. Maintenance rules

- Add a named problem here when its paper card contains enough evidence to define a practical contract.
- A name becomes an implementation commitment only after a problem-blueprint Markdown file is reviewed.
- Keep problem names verb-led and concrete; avoid generic titles such as “Implement Paper X.”
- Prefer small reusable components that can compose into capstones.
- Every paper track includes at least one evaluation/failure-analysis problem and one MLOps/deployment problem.
- The research-curator agent updates this tree when adding or retiring paper cards.
