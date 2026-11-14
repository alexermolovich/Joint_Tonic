# Curriculum authoring status

Generated from `CURRICULUM.md`, published metadata, and existing draft folders. Refresh with `node scripts/update-authoring-status.mjs`. A complete file package is **not** an independent review or a published evaluator.

Scope: **190 named curriculum problems**, plus the four integration capstone sequences. The corpus has 156 distinct papers; not every collected paper has an approved problem in this roadmap. Additional ideas attached to paper flow nodes remain unreviewed until promoted through a blueprint.

Coverage: 75 named entries map directly to published tasks; 2 have independently reviewed drafts; 6 have draft packages awaiting review; 1 have earlier plans; 106 remain queued. The application has 78 published problems; some are supporting components rather than identical named roadmap entries.

## Work and review lanes

| Lane | Author | Independent reviewer |
|---|---|---|
| Foundations and integration | Main agent | Robotics/perception author |
| Vision, VLM, 3D perception | Robotics/perception author | VLA research curator |
| VLA and embodied learning | VLA research curator | MLOps/evaluator author |
| MLOps, deployment, sim-to-real | MLOps/evaluator author | Robotics/perception author |

Authors start with six concrete components per lane. Reviewers check source fidelity, numerical examples, physical contracts, edge cases, and theory clarity. Confirmed findings receive reproducible issue drafts; fixes return to the independent reviewer before integration. The main agent reviews the resulting changes and merges ready PRs when publishing is available.

GitHub publishing currently lacks an available authenticated interface; an earlier credential-access attempt was rejected by automatic approval review. Local issue drafts and fix branches are retained without retrying that method.

Drafts live under `content/planned/` with `blueprint.md`, `statement.md`, `theory.md`, `hints.md`, `examples.md`, and `review.md`. They must not receive published `meta.json` or runnable links until their reference solutions, public/hidden tests, and isolated evaluators are verified.

## 1. Shared physical-AI foundations

| Problem | Group | State |
|---|---|---|
| Broadcast Batched Sensor Features | 1.1 | Queued |
| Stable Softmax for Masked Sequences | 1.1 | Queued |
| Finite-Difference Gradient Check | 1.1 | Queued |
| Seed a Deterministic Evaluation Run | 1.1 | Queued |
| Compute Confidence Intervals Across Robot Episodes | 1.1 | Queued |
| Compare Slice Metrics Without Hiding Regressions | 1.1 | Queued |
| [Apply an SE(3) Transform to Batched Points](problems/se3-transform-points/) | 1.2 | Runnable |
| [Compose and Invert Coordinate Transforms](problems/compose-frame-transforms/) | 1.2 | Runnable |
| [Normalize and Multiply Quaternions](problems/normalize-multiply-quaternions/) | 1.2 | Runnable |
| Interpolate a Pose with SLERP | 1.2 | Queued |
| [Project Camera Points into Pixels](problems/project-camera-points/) | 1.2 | Runnable |
| [Unproject a Depth Map into a Point Cloud](problems/unproject-depth-map/) | 1.2 | Runnable |
| Apply Radial and Tangential Lens Distortion | 1.2 | Queued |
| Validate a Camera Calibration Matrix | 1.2 | Queued |
| Solve a Small Hand-Eye Calibration Residual | 1.2 | Queued |
| Trace Frames Through a Robot Perception Graph | 1.2 | Queued |
| [Interpolate Franka FR3 Joint Waypoints](problems/fr3-joint-interpolation/) | 1.3 | Runnable |
| [Compute Forward Kinematics for a Serial Chain](planned/kinematics/serial-chain-forward-kinematics/) | 1.3 | Existing plan; contract review pending |
| [Solve Closed-Form IK for a Planar Two-Link Arm](problems/planar-two-link-ik/) | 1.3 | Runnable |
| Compute a Geometric Jacobian from Joint Axes | 1.3 | Queued |
| Solve IK with a Jacobian Pseudoinverse | 1.3 | Queued |
| Stabilize Singular IK with Damped Least Squares | 1.3 | Queued |
| Enforce Joint Limits and Collision Constraints in IK | 1.3 | Queued |
| [Interpolate Joint State at Camera Time](problems/interpolate-joint-state/) | 1.4 | Runnable |
| Match Approximate Sensor Timestamps | 1.4 | Queued |
| Detect Dropped and Duplicated Sensor Frames | 1.4 | Queued |
| Estimate Clock Offset from Paired Events | 1.4 | Queued |
| Window an Episode Without Crossing Boundaries | 1.4 | Queued |
| Build Padding and Validity Masks for Robot Sequences | 1.4 | Queued |
| One Kalman Filter Predict Step | 1.5 | Queued |
| One Kalman Filter Measurement Update | 1.5 | Queued |
| Gate Measurements with Mahalanobis Distance | 1.5 | Queued |
| Normalize and Resample Particle Weights | 1.5 | Queued |
| Update Occupancy Grid Log Odds | 1.5 | Queued |
| Fuse Asynchronous Position and Velocity Sensors | 1.5 | Queued |
| [PID with Integral Anti-Windup](problems/pid-anti-windup/) | 1.6 | Runnable |
| Interpolate a Time-Parameterized Trajectory | 1.6 | Queued |
| Check a Segment Against Occupancy Cells | 1.6 | Queued |
| Compute a Differential-Drive Rollout | 1.6 | Queued |
| Evaluate an MPC Tracking Cost | 1.6 | Queued |
| Enforce Velocity and Acceleration Limits | 1.6 | Queued |

## 2. Vision, VLM, and 3D perception

| Problem | Group | State |
|---|---|---|
| [Decode YOLO Grid Predictions into Image Boxes](problems/decode-yolo-grid/) | 2.1 | Runnable |
| Assign Ground-Truth Objects to Responsible Cells | 2.1 | Queued |
| Compute YOLO Coordinate, Objectness, and Class Losses | 2.1 | Queued |
| [Run Class-Aware Non-Maximum Suppression](problems/class-aware-nms/) | 2.1 | Runnable |
| Evaluate Detection with IoU, Precision-Recall, and mAP | 2.1 | Queued |
| Benchmark Detector Accuracy Against Edge Latency | 2.1 | Queued |
| [Build a Detection Bipartite-Matching Cost Matrix](problems/detr-matching-cost/) | 2.2 | Runnable |
| [Match Object Queries with the Hungarian Algorithm](problems/detr-hungarian-assignment/) | 2.2 | Runnable |
| Compute DETR Classification, L1, and GIoU Losses | 2.2 | Queued |
| [Handle the No-Object Class and Padding Masks](problems/detr-no-object-targets/) | 2.2 | Runnable |
| Diagnose Query Collapse and Missed Small Objects | 2.2 | Queued |
| [Patchify and Reconstruct an Image Tensor](problems/vit-patchify-reconstruct/) | 2.3 | Runnable |
| [Build Learned Patch and Class Tokens](problems/vit-patch-class-tokens/) | 2.3 | Runnable |
| [Interpolate 2D Positional Embeddings](problems/vit-position-interpolation/) | 2.3 | Runnable |
| Assemble a Pre-Norm Vision Transformer Block | 2.3 | Queued |
| Profile Token Count, Memory, and Latency by Resolution | 2.3 | Queued |
| [Normalize Image and Text Embeddings](problems/clip-normalize-embeddings/) | 2.4 | Runnable |
| [Compute Symmetric Contrastive Loss](problems/clip-symmetric-loss/) | 2.4 | Runnable |
| [Build a Prompt-Ensembled Zero-Shot Classifier](problems/clip-prompt-ensemble/) | 2.4 | Runnable |
| [Evaluate Cross-Modal Retrieval Recall at K](problems/clip-retrieval-recall/) | 2.4 | Runnable |
| Detect Prompt and Class Distribution Drift | 2.4 | Queued |
| Encode Positive and Negative Point Prompts | 2.5 | Queued |
| Encode a Box Prompt with Positional Features | 2.5 | Queued |
| [Rank Candidate Masks with Predicted IoU](problems/sam-mask-ranking/) | 2.5 | Runnable |
| [Filter Automatic Masks by Stability and Overlap](problems/sam-stability-overlap-filter/) | 2.5 | Runnable |
| Map Text Tokens to Grounded Phrases | 2.5 | Queued |
| Select Language-Guided Object Queries | 2.5 | Queued |
| Decode Phrase-Labeled Boxes | 2.5 | Queued |
| Build a Grounded Segmentation Pipeline and Trace Failures | 2.5 | Queued |
| [Update a Teacher Encoder with Exponential Moving Average](problems/dinov2-teacher-ema/) | 2.6 | Runnable |
| [Center and Sharpen Teacher Probabilities](problems/dinov2-center-sharpen/) | 2.6 | Runnable |
| [Combine Class-Token and Masked-Patch Objectives](problems/dinov2-class-patch-objectives/) | 2.6 | Runnable |
| [Evaluate Frozen Features with k-NN](problems/dinov2-knn-evaluation/) | 2.6 | Runnable |
| Monitor Frozen-Feature Drift Across Camera Domains | 2.6 | Queued |
| [Prove Permutation Invariance with Symmetric Pooling](problems/pointnet-symmetric-pooling/) | 2.7 | Runnable |
| Build a Shared Point MLP and Global Feature | 2.7 | Queued |
| [Concatenate Local and Global Features for Segmentation](problems/pointnet-local-global-features/) | 2.7 | Runnable |
| [Regularize a Learned Feature Transform](problems/pointnet-transform-regularizer/) | 2.7 | Runnable |
| Validate Point-Cloud Density and Coordinate Conventions | 2.7 | Queued |
| Generate Calibrated Camera Rays | 2.8 | Queued |
| [Stratify Samples Along Near and Far Bounds](problems/nerf-stratified-samples/) | 2.8 | Runnable |
| [Encode 3D Positions with Fourier Features](problems/nerf-fourier-features/) | 2.8 | Runnable |
| [Compute Transmittance and Alpha Compositing Weights](problems/nerf-alpha-compositing/) | 2.8 | Runnable |
| [Render Color and Expected Depth Along a Ray](problems/nerf-render-color-depth/) | 2.8 | Runnable |
| Detect Bad Poses with Reprojection and Render Residuals | 2.8 | Queued |
| Project BEV Reference Points into Calibrated Cameras | 2.9 | Queued |
| Mask Out-of-View and Behind-Camera Samples | 2.9 | Queued |
| [Aggregate Multi-Camera Features with Attention Weights](problems/bev-weighted-camera-features/) | 2.9 | Runnable |
| [Warp a Previous BEV with Ego Motion](problems/bev-ego-motion-warp/) | 2.9 | Runnable |
| Fuse Temporal BEV State | 2.9 | Queued |
| Diagnose Camera Dropout and Calibration Drift in BEV | 2.9 | Queued |

## 3. VLA and embodied robot learning

| Problem | Group | State |
|---|---|---|
| [Quantize and Dequantize Continuous Robot Actions](problems/rt1-action-codec/) | 3.1 | Runnable |
| [Select Compact Visual Tokens with Learned Attention](problems/rt1-compact-visual-tokens/) | 3.1 | Runnable |
| [Build a Causal Action-Token Mask](problems/rt1-causal-action-token-mask/) | 3.1 | Runnable |
| Sample a Task-Balanced Trajectory Batch | 3.1 | Queued |
| Measure Closed-Loop Latency and Action Dropouts | 3.1 | Queued |
| [Build Sliding Action Chunks with Padding Masks](problems/act-sliding-action-chunks/) | 3.2 | Runnable |
| [Compute a Masked CVAE Reconstruction and KL Loss](problems/act-cvae-loss/) | 3.2 | Runnable |
| [Blend Overlapping Action Chunks with Temporal Ensembling](problems/act-temporal-ensembling/) | 3.2 | Runnable |
| Evaluate Chunk Length Against Compounding Error | 3.2 | Queued |
| Detect Teleoperation Demonstration Quality Failures | 3.2 | Queued |
| [Add Noise to an Action Sequence](problems/diffusion-action-noising/) | 3.3 | Runnable |
| [Compute a Conditional Noise-Prediction Loss](problems/diffusion-conditional-noise-loss/) | 3.3 | Runnable |
| Sample an Action Trajectory with DDPM Steps | 3.3 | Queued |
| [Execute a Receding-Horizon Action Window](problems/diffusion-receding-horizon-window/) | 3.3 | Runnable |
| Budget Denoising Steps Against Control Frequency | 3.3 | Queued |
| [Project Continuous Sensor Features into Language Width](problems/palm-e-project-sensor-features/) | 3.4 | Runnable |
| Interleave Image, State, and Text Tokens | 3.4 | Queued |
| Build a Multimodal Causal Attention Mask | 3.4 | Queued |
| Collate Variable Multimodal Sequences | 3.4 | Queued |
| Validate Missing-Modality and Stale-Sensor Inputs | 3.4 | Queued |
| [Serialize Robot Actions as Discrete Tokens](problems/rt2-serialize-action-tokens/) | 3.5 | Runnable |
| [Parse and Validate an Action-Token Grammar](problems/rt2-parse-action-grammar/) | 3.5 | Runnable |
| Mix Web and Robot Batches at a Target Ratio | 3.5 | Queued |
| [Constrain Autoregressive Decoding to Valid Actions](problems/rt2-constrained-action-decoding/) | 3.5 | Runnable |
| Monitor Invalid Actions and Semantic Generalization Slices | 3.5 | Queued |
| Normalize Heterogeneous Robot Observation Schemas | 3.6 | Queued |
| Normalize and Mask Embodiment-Specific Action Spaces | 3.6 | Queued |
| Sample a Balanced Multi-Dataset Mixture | 3.6 | Queued |
| Compute Per-Embodiment and Transfer Metrics | 3.6 | Queued |
| Version a Cross-Robot Dataset Manifest | 3.6 | Queued |
| Assemble Observation and Task Token Groups | 3.7 | Queued |
| Build Block Masks for Missing Sensors and Goals | 3.7 | Queued |
| Route Tokens into Dataset-Specific Action Heads | 3.7 | Queued |
| Add a Frozen-Backbone Adaptation Module | 3.7 | Queued |
| Verify Trainable Parameters and Fine-Tuning Artifacts | 3.7 | Queued |
| [Fuse Two Visual Feature Streams Safely](planned/vla/openvla-fuse-visual-streams/) | 3.8 | Reviewed draft; evaluator pending |
| Quantize Actions from Training-Set Quantiles | 3.8 | Queued |
| Build a VLA Action-Token Training Batch | 3.8 | Queued |
| [Add Low-Rank Adaptation to a Policy Layer](planned/vla/openvla-lora-policy-layer/) | 3.8 | Reviewed draft; evaluator pending |
| Estimate Memory, Latency, and Quantized Serving Budgets | 3.8 | Queued |
| [Sample Flow-Matching Action Interpolants and Targets](problems/pi0-flow-action-interpolants/) | 3.9 | Runnable |
| Build Block Attention for VLM and Action Expert Tokens | 3.9 | Queued |
| [Integrate an Action Flow with Euler Steps](problems/pi0-euler-action-flow/) | 3.9 | Runnable |
| Evaluate Solver Steps Against Trajectory Error | 3.9 | Queued |
| Monitor Continuous-Action Range and Smoothness Drift | 3.9 | Queued |
| Route Inputs Through a Dual-System Policy Interface | 3.10 | Queued |
| Build a Heterogeneous Real, Video, and Synthetic Batch | 3.10 | Queued |
| Compute a Diffusion-Transformer Action-Chunk Loss | 3.10 | Queued |
| Report Metrics by Source and Embodiment | 3.10 | Queued |
| Gate a Humanoid Policy Release on Safety Slices | 3.10 | Queued |

## 4. Robotics MLOps, deployment, and sim-to-real

| Problem | Group | State |
|---|---|---|
| [Compute Dependency-Graph Blast Radius](problems/dependency-graph-blast-radius/) | 4.1 | Runnable |
| [Detect Feedback Loops in an ML Pipeline](problems/detect-pipeline-feedback-loops/) | 4.1 | Runnable |
| [Score a Robot ML System for Production Readiness](problems/robot-ml-readiness-score/) | 4.1 | Runnable |
| [Gate a Release on Slice and Infrastructure Tests](problems/slice-infrastructure-release-gate/) | 4.1 | Runnable |
| [Triage a Physical-AI Deployment Incident](problems/physical-ai-incident-triage/) | 4.1 | Runnable |
| [Topologically Schedule a Training Pipeline DAG](problems/training-pipeline-topological-order/) | 4.2 | Runnable |
| [Record Dataset, Transform, Model, and Evaluator Lineage](problems/record-artifact-lineage/) | 4.2 | Runnable |
| [Invalidate Cached Artifacts After an Upstream Change](problems/invalidate-downstream-cache/) | 4.2 | Runnable |
| [Detect Training-Serving Transform Skew](problems/training-serving-transform-skew/) | 4.2 | Runnable |
| [Reproduce a Model from an Immutable Run Manifest](problems/verify-immutable-run-manifest/) | 4.2 | Runnable |
| [Infer a Schema from Robot Episodes](problems/infer-robot-episode-schema/) | 4.3 | Runnable |
| [Detect Missing, Range, Domain, and Shape Anomalies](problems/robot-feature-anomalies/) | 4.3 | Runnable |
| [Compare Training and Serving Distributions](problems/compare-training-serving-distributions/) | 4.3 | Runnable |
| [Detect Sensor Timestamp and Calibration Skew](problems/sensor-timestamp-calibration-skew/) | 4.3 | Runnable |
| [Block a Pipeline on Critical Data Anomalies](problems/critical-data-anomaly-gate/) | 4.3 | Runnable |
| [Split Robot Trajectories Without Scene Leakage](problems/scene-safe-trajectory-split/) | 4.4 | Runnable |
| [Batch Variable-Length Episodes with Masks](problems/batch-variable-robot-episodes/) | 4.4 | Runnable |
| [Compare Validation Loss with Rollout Success](problems/validation-loss-rollout-ranking/) | 4.4 | Runnable |
| [Report Performance by Demonstration Quality](problems/demonstration-quality-performance/) | 4.4 | Runnable |
| [Select a Checkpoint with Offline and Rollout Gates](problems/offline-rollout-checkpoint-gate/) | 4.4 | Runnable |
| [Map Robot-Specific Data into a Shared Episode Schema](problems/map-shared-robot-episode/) | 4.5 | Runnable |
| [Balance a Multi-Dataset Training Mixture](problems/balance-multidataset-batch/) | 4.5 | Runnable |
| [Mask Unavailable Action Dimensions](planned/mlops/mask-unavailable-action-dimensions/) | 4.5 | Draft package; review pending |
| [Build a Per-Embodiment Transfer Matrix](planned/mlops/per-embodiment-transfer-matrix/) | 4.5 | Draft package; review pending |
| [Detect Dataset-Version and Schema Drift](planned/mlops/dataset-version-schema-drift/) | 4.5 | Draft package; review pending |
| [Compute p50, p90, and p99 Inference Latency](problems/inference-latency-percentiles/) | 4.6 | Runnable |
| [Simulate Single-Stream and Server Load](planned/mlops/simulate-inference-load/) | 4.6 | Draft package; review pending |
| [Reject Invalid Benchmark Runs](planned/mlops/reject-invalid-benchmark-runs/) | 4.6 | Draft package; review pending |
| [Derive End-to-End Latency from Robotics Trace Events](planned/mlops/robotics-trace-end-to-end-latency/) | 4.6 | Draft package; review pending |
| Measure Throughput and Jitter Across a ROS-Style Graph | 4.6 | Queued |
| Compare Black-Box and Grey-Box Pipeline Measurements | 4.6 | Queued |
| Fuse Compatible Operators in a Compute Graph | 4.7 | Queued |
| Search Tensor Tile Sizes with a Toy Cost Model | 4.7 | Queued |
| Reuse Tensor Buffers with Liveness Analysis | 4.7 | Queued |
| Extract a Depth, Width, and Kernel Subnetwork | 4.7 | Queued |
| Sample a Progressive-Shrinking Curriculum | 4.7 | Queued |
| Select a Pareto Model Under Accuracy and Latency Limits | 4.7 | Queued |
| Package and Verify an Edge Model Artifact | 4.7 | Queued |
| Build a Seeded Visual Randomization Sampler | 4.8 | Queued |
| Stratify Texture, Lighting, Camera, and Distractor Factors | 4.8 | Queued |
| Measure Performance Across Shift Buckets | 4.8 | Queued |
| Estimate Scenario Coverage and Confidence Intervals | 4.8 | Queued |
| Version a Simulation Scenario Distribution | 4.8 | Queued |
| [Sample Mass, Friction, Delay, and Gain Distributions](problems/sample-dynamics-distributions/) | 4.9 | Runnable |
| Aggregate Mean and Worst-Case Policy Returns | 4.9 | Queued |
| Quantify Calibration Sensitivity | 4.9 | Queued |
| Choose Randomization Bounds from Safety Constraints | 4.9 | Queued |
| Gate Sim-to-Real Release with Robustness Evidence | 4.9 | Queued |
