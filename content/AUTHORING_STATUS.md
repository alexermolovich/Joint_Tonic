# Curriculum authoring status

Generated from `CURRICULUM.md`, published metadata, and existing draft folders. Refresh with `node scripts/update-authoring-status.mjs`. A complete file package is **not** an independent review or a published evaluator.

Scope: **365 named curriculum problems**, plus the four integration capstone sequences. The corpus has 156 distinct papers; not every collected paper has an approved problem in this roadmap. Additional ideas attached to paper flow nodes remain unreviewed until promoted through a blueprint.

Coverage: 365 named entries map directly to published tasks; 0 have independently reviewed drafts; 0 have draft packages awaiting review; 0 have earlier plans; 0 remain queued. The application has 372 published problems; some are supporting components rather than identical named roadmap entries.

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
| [Broadcast Batched Sensor Features](problems/broadcast-batched-sensor-features/) | 1.1 | Runnable |
| [Stable Softmax for Masked Sequences](problems/stable-masked-softmax/) | 1.1 | Runnable |
| [Finite-Difference Gradient Check](problems/finite-difference-gradient-check/) | 1.1 | Runnable |
| [Seed a Deterministic Evaluation Run](problems/seed-deterministic-evaluation/) | 1.1 | Runnable |
| [Compute Confidence Intervals Across Robot Episodes](problems/robot-episode-confidence-intervals/) | 1.1 | Runnable |
| [Compare Slice Metrics Without Hiding Regressions](problems/slice-metrics-regressions/) | 1.1 | Runnable |
| [Apply an SE(3) Transform to Batched Points](problems/se3-transform-points/) | 1.2 | Runnable |
| [Compose and Invert Coordinate Transforms](problems/compose-frame-transforms/) | 1.2 | Runnable |
| [Normalize and Multiply Quaternions](problems/normalize-multiply-quaternions/) | 1.2 | Runnable |
| [Interpolate a Pose with SLERP](problems/interpolate-pose-slerp/) | 1.2 | Runnable |
| [Project Camera Points into Pixels](problems/project-camera-points/) | 1.2 | Runnable |
| [Unproject a Depth Map into a Point Cloud](problems/unproject-depth-map/) | 1.2 | Runnable |
| [Apply Radial and Tangential Lens Distortion](problems/radial-tangential-lens-distortion/) | 1.2 | Runnable |
| [Validate a Camera Calibration Matrix](problems/validate-camera-calibration-matrix/) | 1.2 | Runnable |
| [Solve a Small Hand-Eye Calibration Residual](problems/hand-eye-translation-residual/) | 1.2 | Runnable |
| [Trace Frames Through a Robot Perception Graph](problems/trace-perception-frame-graph/) | 1.2 | Runnable |
| [Interpolate Franka FR3 Joint Waypoints](problems/fr3-joint-interpolation/) | 1.3 | Runnable |
| [Compute Forward Kinematics for a Serial Chain](problems/serial-chain-forward-kinematics/) | 1.3 | Runnable |
| [Solve Closed-Form IK for a Planar Two-Link Arm](problems/planar-two-link-ik/) | 1.3 | Runnable |
| [Compute a Geometric Jacobian from Joint Axes](problems/geometric-jacobian-joint-axes/) | 1.3 | Runnable |
| [Solve IK with a Jacobian Pseudoinverse](problems/planar-ik-jacobian-pseudoinverse/) | 1.3 | Runnable |
| [Stabilize Singular IK with Damped Least Squares](problems/damped-least-squares-ik-step/) | 1.3 | Runnable |
| [Enforce Joint Limits and Collision Constraints in IK](problems/joint-limit-collision-ik-candidates/) | 1.3 | Runnable |
| [Interpolate Joint State at Camera Time](problems/interpolate-joint-state/) | 1.4 | Runnable |
| [Match Approximate Sensor Timestamps](problems/match-approximate-sensor-timestamps/) | 1.4 | Runnable |
| [Detect Dropped and Duplicated Sensor Frames](problems/detect-dropped-duplicated-sensor-frames/) | 1.4 | Runnable |
| [Estimate Clock Offset from Paired Events](problems/estimate-clock-offset-paired-events/) | 1.4 | Runnable |
| [Window an Episode Without Crossing Boundaries](problems/window-episode-without-crossing-boundaries/) | 1.4 | Runnable |
| [Build Padding and Validity Masks for Robot Sequences](problems/build-robot-sequence-validity-masks/) | 1.4 | Runnable |
| [One Kalman Filter Predict Step](problems/kalman-filter-predict-step/) | 1.5 | Runnable |
| [One Kalman Filter Measurement Update](problems/kalman-filter-measurement-update/) | 1.5 | Runnable |
| [Gate Measurements with Mahalanobis Distance](problems/mahalanobis-measurement-gate/) | 1.5 | Runnable |
| [Normalize and Resample Particle Weights](problems/normalize-resample-particle-weights/) | 1.5 | Runnable |
| [Update Occupancy Grid Log Odds](problems/occupancy-grid-log-odds-update/) | 1.5 | Runnable |
| [Fuse Asynchronous Position and Velocity Sensors](problems/fuse-asynchronous-position-velocity/) | 1.5 | Runnable |
| [PID with Integral Anti-Windup](problems/pid-anti-windup/) | 1.6 | Runnable |
| [Interpolate a Time-Parameterized Trajectory](problems/time-parameterized-trajectory/) | 1.6 | Runnable |
| [Check a Segment Against Occupancy Cells](problems/segment-occupancy-cell-check/) | 1.6 | Runnable |
| [Compute a Differential-Drive Rollout](problems/differential-drive-rollout/) | 1.6 | Runnable |
| [Evaluate an MPC Tracking Cost](problems/mpc-tracking-cost/) | 1.6 | Runnable |
| [Enforce Velocity and Acceleration Limits](problems/velocity-acceleration-command-limits/) | 1.6 | Runnable |

## 2. Vision, VLM, and 3D perception

| Problem | Group | State |
|---|---|---|
| [Decode YOLO Grid Predictions into Image Boxes](problems/decode-yolo-grid/) | 2.1 | Runnable |
| [Assign Ground-Truth Objects to Responsible Cells](problems/yolo-responsible-cell-targets/) | 2.1 | Runnable |
| [Compute YOLO Coordinate, Objectness, and Class Losses](problems/yolo-coordinate-objectness-class-loss/) | 2.1 | Runnable |
| [Run Class-Aware Non-Maximum Suppression](problems/class-aware-nms/) | 2.1 | Runnable |
| [Evaluate Detection with IoU, Precision-Recall, and mAP](problems/detection-precision-recall-map/) | 2.1 | Runnable |
| [Benchmark Detector Accuracy Against Edge Latency](problems/detector-accuracy-latency-frontier/) | 2.1 | Runnable |
| [Build a Detection Bipartite-Matching Cost Matrix](problems/detr-matching-cost/) | 2.2 | Runnable |
| [Match Object Queries with the Hungarian Algorithm](problems/detr-hungarian-assignment/) | 2.2 | Runnable |
| [Compute DETR Classification, L1, and GIoU Losses](problems/detr-matched-training-losses/) | 2.2 | Runnable |
| [Handle the No-Object Class and Padding Masks](problems/detr-no-object-targets/) | 2.2 | Runnable |
| [Diagnose Query Collapse and Missed Small Objects](problems/detr-query-small-object-diagnostics/) | 2.2 | Runnable |
| [Patchify and Reconstruct an Image Tensor](problems/vit-patchify-reconstruct/) | 2.3 | Runnable |
| [Build Learned Patch and Class Tokens](problems/vit-patch-class-tokens/) | 2.3 | Runnable |
| [Interpolate 2D Positional Embeddings](problems/vit-position-interpolation/) | 2.3 | Runnable |
| [Assemble a Pre-Norm Vision Transformer Block](problems/vit-pre-norm-block/) | 2.3 | Runnable |
| [Profile Token Count, Memory, and Latency by Resolution](problems/vit-resolution-profile/) | 2.3 | Runnable |
| [Normalize Image and Text Embeddings](problems/clip-normalize-embeddings/) | 2.4 | Runnable |
| [Compute Symmetric Contrastive Loss](problems/clip-symmetric-loss/) | 2.4 | Runnable |
| [Build a Prompt-Ensembled Zero-Shot Classifier](problems/clip-prompt-ensemble/) | 2.4 | Runnable |
| [Evaluate Cross-Modal Retrieval Recall at K](problems/clip-retrieval-recall/) | 2.4 | Runnable |
| [Detect Prompt and Class Distribution Drift](problems/clip-prompt-class-drift/) | 2.4 | Runnable |
| [Encode Positive and Negative Point Prompts](problems/sam-point-prompt-encoding/) | 2.5 | Runnable |
| [Encode a Box Prompt with Positional Features](problems/sam-box-prompt-encoding/) | 2.5 | Runnable |
| [Rank Candidate Masks with Predicted IoU](problems/sam-mask-ranking/) | 2.5 | Runnable |
| [Filter Automatic Masks by Stability and Overlap](problems/sam-stability-overlap-filter/) | 2.5 | Runnable |
| [Map Text Tokens to Grounded Phrases](problems/grounding-token-phrase-map/) | 2.5 | Runnable |
| [Select Language-Guided Object Queries](problems/grounding-language-query-selection/) | 2.5 | Runnable |
| [Decode Phrase-Labeled Boxes](problems/grounding-phrase-box-decoding/) | 2.5 | Runnable |
| [Build a Grounded Segmentation Pipeline and Trace Failures](problems/grounded-segmentation-failure-trace/) | 2.5 | Runnable |
| [Update a Teacher Encoder with Exponential Moving Average](problems/dinov2-teacher-ema/) | 2.6 | Runnable |
| [Center and Sharpen Teacher Probabilities](problems/dinov2-center-sharpen/) | 2.6 | Runnable |
| [Combine Class-Token and Masked-Patch Objectives](problems/dinov2-class-patch-objectives/) | 2.6 | Runnable |
| [Evaluate Frozen Features with k-NN](problems/dinov2-knn-evaluation/) | 2.6 | Runnable |
| [Monitor Frozen-Feature Drift Across Camera Domains](problems/dinov2-camera-feature-drift/) | 2.6 | Runnable |
| [Prove Permutation Invariance with Symmetric Pooling](problems/pointnet-symmetric-pooling/) | 2.7 | Runnable |
| [Build a Shared Point MLP and Global Feature](problems/pointnet-shared-mlp/) | 2.7 | Runnable |
| [Concatenate Local and Global Features for Segmentation](problems/pointnet-local-global-features/) | 2.7 | Runnable |
| [Regularize a Learned Feature Transform](problems/pointnet-transform-regularizer/) | 2.7 | Runnable |
| [Validate Point-Cloud Density and Coordinate Conventions](problems/pointcloud-density-conventions/) | 2.7 | Runnable |
| [Generate Calibrated Camera Rays](problems/nerf-calibrated-camera-rays/) | 2.8 | Runnable |
| [Stratify Samples Along Near and Far Bounds](problems/nerf-stratified-samples/) | 2.8 | Runnable |
| [Encode 3D Positions with Fourier Features](problems/nerf-fourier-features/) | 2.8 | Runnable |
| [Compute Transmittance and Alpha Compositing Weights](problems/nerf-alpha-compositing/) | 2.8 | Runnable |
| [Render Color and Expected Depth Along a Ray](problems/nerf-render-color-depth/) | 2.8 | Runnable |
| [Detect Bad Poses with Reprojection and Render Residuals](problems/nerf-pose-residual-diagnostics/) | 2.8 | Runnable |
| [Project BEV Reference Points into Calibrated Cameras](problems/bev-project-reference-points/) | 2.9 | Runnable |
| [Mask Out-of-View and Behind-Camera Samples](problems/bev-visibility-mask/) | 2.9 | Runnable |
| [Aggregate Multi-Camera Features with Attention Weights](problems/bev-weighted-camera-features/) | 2.9 | Runnable |
| [Warp a Previous BEV with Ego Motion](problems/bev-ego-motion-warp/) | 2.9 | Runnable |
| [Fuse Temporal BEV State](problems/bev-temporal-fusion/) | 2.9 | Runnable |
| [Diagnose Camera Dropout and Calibration Drift in BEV](problems/bev-camera-health-diagnostics/) | 2.9 | Runnable |

## 3. VLA and embodied robot learning

| Problem | Group | State |
|---|---|---|
| [Quantize and Dequantize Continuous Robot Actions](problems/rt1-action-codec/) | 3.1 | Runnable |
| [Select Compact Visual Tokens with Learned Attention](problems/rt1-compact-visual-tokens/) | 3.1 | Runnable |
| [Build a Causal Action-Token Mask](problems/rt1-causal-action-token-mask/) | 3.1 | Runnable |
| [Sample a Task-Balanced Trajectory Batch](problems/rt1-task-balanced-trajectories/) | 3.1 | Runnable |
| [Measure Closed-Loop Latency and Action Dropouts](problems/rt1-control-latency-dropouts/) | 3.1 | Runnable |
| [Build Sliding Action Chunks with Padding Masks](problems/act-sliding-action-chunks/) | 3.2 | Runnable |
| [Compute a Masked CVAE Reconstruction and KL Loss](problems/act-cvae-loss/) | 3.2 | Runnable |
| [Blend Overlapping Action Chunks with Temporal Ensembling](problems/act-temporal-ensembling/) | 3.2 | Runnable |
| [Evaluate Chunk Length Against Compounding Error](problems/act-chunk-compounding-error/) | 3.2 | Runnable |
| [Detect Teleoperation Demonstration Quality Failures](problems/act-teleoperation-quality/) | 3.2 | Runnable |
| [Add Noise to an Action Sequence](problems/diffusion-action-noising/) | 3.3 | Runnable |
| [Compute a Conditional Noise-Prediction Loss](problems/diffusion-conditional-noise-loss/) | 3.3 | Runnable |
| [Sample an Action Trajectory with DDPM Steps](problems/diffusion-ddpm-action-sampler/) | 3.3 | Runnable |
| [Execute a Receding-Horizon Action Window](problems/diffusion-receding-horizon-window/) | 3.3 | Runnable |
| [Budget Denoising Steps Against Control Frequency](problems/diffusion-denoising-budget/) | 3.3 | Runnable |
| [Project Continuous Sensor Features into Language Width](problems/palm-e-project-sensor-features/) | 3.4 | Runnable |
| [Interleave Image, State, and Text Tokens](problems/palm-e-interleave-modal-tokens/) | 3.4 | Runnable |
| [Build a Multimodal Causal Attention Mask](problems/palm-e-multimodal-causal-mask/) | 3.4 | Runnable |
| [Collate Variable Multimodal Sequences](problems/palm-e-collate-multimodal-sequences/) | 3.4 | Runnable |
| [Validate Missing-Modality and Stale-Sensor Inputs](problems/palm-e-sensor-readiness/) | 3.4 | Runnable |
| [Serialize Robot Actions as Discrete Tokens](problems/rt2-serialize-action-tokens/) | 3.5 | Runnable |
| [Parse and Validate an Action-Token Grammar](problems/rt2-parse-action-grammar/) | 3.5 | Runnable |
| [Mix Web and Robot Batches at a Target Ratio](problems/rt2-mix-web-robot-batches/) | 3.5 | Runnable |
| [Constrain Autoregressive Decoding to Valid Actions](problems/rt2-constrained-action-decoding/) | 3.5 | Runnable |
| [Monitor Invalid Actions and Semantic Generalization Slices](problems/rt2-action-generalization-slices/) | 3.5 | Runnable |
| [Normalize Heterogeneous Robot Observation Schemas](problems/oxe-normalize-observation-schema/) | 3.6 | Runnable |
| [Normalize and Mask Embodiment-Specific Action Spaces](problems/oxe-normalize-action-spaces/) | 3.6 | Runnable |
| [Sample a Balanced Multi-Dataset Mixture](problems/oxe-balanced-dataset-sampling/) | 3.6 | Runnable |
| [Compute Per-Embodiment and Transfer Metrics](problems/oxe-embodiment-transfer-metrics/) | 3.6 | Runnable |
| [Version a Cross-Robot Dataset Manifest](problems/oxe-version-dataset-manifest/) | 3.6 | Runnable |
| [Assemble Observation and Task Token Groups](problems/octo-assemble-token-groups/) | 3.7 | Runnable |
| [Build Block Masks for Missing Sensors and Goals](problems/octo-missing-modality-block-mask/) | 3.7 | Runnable |
| [Route Tokens into Dataset-Specific Action Heads](problems/octo-dataset-specific-action-heads/) | 3.7 | Runnable |
| [Add a Frozen-Backbone Adaptation Module](problems/octo-frozen-backbone-adaptation/) | 3.7 | Runnable |
| [Verify Trainable Parameters and Fine-Tuning Artifacts](problems/octo-verify-finetuning-artifacts/) | 3.7 | Runnable |
| [Fuse Two Visual Feature Streams Safely](problems/openvla-fuse-visual-streams/) | 3.8 | Runnable |
| [Quantize Actions from Training-Set Quantiles](problems/openvla-training-quantile-action-bins/) | 3.8 | Runnable |
| [Build a VLA Action-Token Training Batch](problems/openvla-action-token-training-batch/) | 3.8 | Runnable |
| [Add Low-Rank Adaptation to a Policy Layer](problems/openvla-lora-policy-layer/) | 3.8 | Runnable |
| [Estimate Memory, Latency, and Quantized Serving Budgets](problems/openvla-quantized-serving-budget/) | 3.8 | Runnable |
| [Sample Flow-Matching Action Interpolants and Targets](problems/pi0-flow-action-interpolants/) | 3.9 | Runnable |
| [Build Block Attention for VLM and Action Expert Tokens](problems/pi0-vlm-action-block-attention/) | 3.9 | Runnable |
| [Integrate an Action Flow with Euler Steps](problems/pi0-euler-action-flow/) | 3.9 | Runnable |
| [Evaluate Solver Steps Against Trajectory Error](problems/pi0-solver-trajectory-error/) | 3.9 | Runnable |
| [Monitor Continuous-Action Range and Smoothness Drift](problems/pi0-action-range-smoothness-drift/) | 3.9 | Runnable |
| [Route Inputs Through a Dual-System Policy Interface](problems/gr00t-dual-system-routing/) | 3.10 | Runnable |
| [Build a Heterogeneous Real, Video, and Synthetic Batch](problems/gr00t-heterogeneous-training-batch/) | 3.10 | Runnable |
| [Compute a Masked Action Flow-Matching Loss](problems/gr00t-masked-action-flow-loss/) | 3.10 | Runnable |
| [Report Metrics by Source and Embodiment](problems/gr00t-source-embodiment-metrics/) | 3.10 | Runnable |
| [Gate a Humanoid Policy Release on Safety Slices](problems/gr00t-humanoid-safety-slice-gate/) | 3.10 | Runnable |

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
| [Mask Unavailable Action Dimensions](problems/mask-unavailable-action-dimensions/) | 4.5 | Runnable |
| [Build a Per-Embodiment Transfer Matrix](problems/per-embodiment-transfer-matrix/) | 4.5 | Runnable |
| [Detect Dataset-Version and Schema Drift](problems/dataset-version-schema-drift/) | 4.5 | Runnable |
| [Compute p50, p90, and p99 Inference Latency](problems/inference-latency-percentiles/) | 4.6 | Runnable |
| [Simulate Single-Stream and Server Load](problems/simulate-inference-load/) | 4.6 | Runnable |
| [Reject Invalid Benchmark Runs](problems/reject-invalid-benchmark-runs/) | 4.6 | Runnable |
| [Derive End-to-End Latency from Robotics Trace Events](problems/robotics-trace-end-to-end-latency/) | 4.6 | Runnable |
| [Measure Throughput and Jitter Across a ROS-Style Graph](problems/graph-throughput-jitter/) | 4.6 | Runnable |
| [Compare Black-Box and Grey-Box Pipeline Measurements](problems/compare-pipeline-measurements/) | 4.6 | Runnable |
| [Fuse Compatible Operators in a Compute Graph](problems/fuse-compatible-operators/) | 4.7 | Runnable |
| [Search Tensor Tile Sizes with a Toy Cost Model](problems/search-tensor-tiles/) | 4.7 | Runnable |
| [Reuse Tensor Buffers with Liveness Analysis](problems/reuse-tensor-buffers/) | 4.7 | Runnable |
| [Extract a Depth, Width, and Kernel Subnetwork](problems/extract-elastic-subnetwork/) | 4.7 | Runnable |
| [Sample a Progressive-Shrinking Curriculum](problems/progressive-shrinking-curriculum/) | 4.7 | Runnable |
| [Select a Pareto Model Under Accuracy and Latency Limits](problems/pareto-edge-model-selection/) | 4.7 | Runnable |
| [Package and Verify an Edge Model Artifact](problems/package-edge-model-artifact/) | 4.7 | Runnable |
| [Build a Seeded Visual Randomization Sampler](problems/seeded-visual-randomization/) | 4.8 | Runnable |
| [Stratify Texture, Lighting, Camera, and Distractor Factors](problems/stratify-visual-factors/) | 4.8 | Runnable |
| [Measure Performance Across Shift Buckets](problems/shift-bucket-performance/) | 4.8 | Runnable |
| [Estimate Scenario Coverage and Confidence Intervals](problems/scenario-coverage-confidence/) | 4.8 | Runnable |
| [Version a Simulation Scenario Distribution](problems/version-simulation-distribution/) | 4.8 | Runnable |
| [Sample Mass, Friction, Delay, and Gain Distributions](problems/sample-dynamics-distributions/) | 4.9 | Runnable |
| [Aggregate Mean and Worst-Case Policy Returns](problems/aggregate-policy-returns/) | 4.9 | Runnable |
| [Quantify Calibration Sensitivity](problems/calibration-sensitivity/) | 4.9 | Runnable |
| [Choose Randomization Bounds from Safety Constraints](problems/randomization-safety-bounds/) | 4.9 | Runnable |
| [Gate Sim-to-Real Release with Robustness Evidence](problems/sim-to-real-robustness-gate/) | 4.9 | Runnable |

## 7. Reviewed paper-library expansion

| Problem | Group | State |
|---|---|---|
| [Compute the Clipped Policy Surrogate](problems/ppo-clipped-policy-surrogate/) | 7.1 | Runnable |
| [Normalize Batched Advantages](problems/ppo-normalize-batched-advantages/) | 7.1 | Runnable |
| [Report Policy Update Clip Fractions](problems/ppo-policy-update-clip-fractions/) | 7.1 | Runnable |
| [Compute Value Targets Across Episode Boundaries](problems/ppo-boundary-value-targets/) | 7.1 | Runnable |
| [Compute an Entropy-Regularized State Value](problems/sac-soft-state-value/) | 7.1 | Runnable |
| [Compute an Entropy-Regularized Bellman Target](problems/soft-value-bellman-target/) | 7.1 | Runnable |
| [Apply Tanh Action Log-Probability Correction](problems/sac-tanh-logprob-correction/) | 7.1 | Runnable |
| [Update a Temperature Objective (later SAC extension)](problems/sac-temperature-objective-update/) | 7.1 | Runnable |
| [Compute an Expectile Regression Loss](problems/iql-expectile-regression/) | 7.1 | Runnable |
| [Build Advantage-Weighted Action Weights](problems/iql-advantage-action-weights/) | 7.1 | Runnable |
| [Validate an Offline Dataset Split](problems/iql-offline-dataset-split/) | 7.1 | Runnable |
| [Train and Evaluate a Tiny PPO Joint Controller](problems/ppo-joint-controller-integration/) | 7.1 | Runnable |
| [Compute a Conservative Q Penalty](problems/cql-discrete-conservative-penalty/) | 7.1 | Runnable |
| [Compare Logged and Sampled Action Values](problems/cql-logged-sampled-value-gap/) | 7.1 | Runnable |
| [Evaluate Offline Policy Support](problems/cql-offline-policy-support/) | 7.1 | Runnable |
| [Apply a Seeded Random-Shift Augmentation](problems/drq-seeded-random-shift/) | 7.1 | Runnable |
| [Average Augmented Bellman Targets](problems/drq-augmented-bellman-targets/) | 7.1 | Runnable |
| [Compute a Multi-View Critic Regression Loss](problems/drq-multiview-critic-loss/) | 7.1 | Runnable |
| [Interpolate a Reference Motion Pose](problems/deepmimic-reference-pose/) | 7.1 | Runnable |
| [Detect Phase Misalignment in a Motion Clip](problems/deepmimic-phase-alignment/) | 7.1 | Runnable |
| [Compute Pose and Velocity Imitation Rewards](problems/deepmimic-pose-velocity-rewards/) | 7.1 | Runnable |
| [Combine Motion and Task Rewards](problems/motion-task-reward-blend/) | 7.1 | Runnable |
| [Construct Motion Discriminator Features](problems/amp-motion-discriminator-features/) | 7.1 | Runnable |
| [Compute an Adversarial Style Reward](problems/amp-adversarial-style-reward/) | 7.1 | Runnable |
| [Build Privileged Dynamics-Latent Supervision](problems/rma-privileged-latent-supervision/) | 7.1 | Runnable |
| [Window Proprioceptive History](problems/rma-proprioceptive-history-window/) | 7.1 | Runnable |
| [Estimate a Latent Dynamics Context](problems/rma-latent-context-estimator/) | 7.1 | Runnable |
| [Track the Age of an Asynchronous Adaptation Latent](problems/rma-asynchronous-latent-age/) | 7.1 | Runnable |
| [Evaluate Policy Recovery After a Parameter Change](problems/rma-parameter-change-recovery/) | 7.1 | Runnable |
| [Validate a Reward Function Contract](problems/eureka-reward-output-contract/) | 7.1 | Runnable |
| [Aggregate Reward-Component Diagnostics](problems/eureka-reward-component-diagnostics/) | 7.1 | Runnable |
| [Rank Reward Candidates by Rollout Evidence](problems/eureka-rank-rollout-candidates/) | 7.1 | Runnable |
| [Validate a Generated Reward Program](problems/dreureka-reward-expression-program/) | 7.1 | Runnable |
| [Compare Robustness Across Randomization Settings](problems/dreureka-randomization-robustness/) | 7.1 | Runnable |
| [Compute a Balanced Latent-Model Loss](problems/dreamer-balanced-latent-loss/) | 7.1 | Runnable |
| [Encode Symlog Two-Hot Reward Targets](problems/dreamer-symlog-twohot-targets/) | 7.1 | Runnable |
| [Build Lambda-Return Targets](problems/dreamer-continuation-lambda-returns/) | 7.1 | Runnable |
| [Roll Out Imagined Latent Trajectories](problems/dreamer-imagined-latent-rollout/) | 7.1 | Runnable |
| [Apply Groupwise SimNorm to Latent States](problems/tdmpc2-groupwise-simnorm/) | 7.1 | Runnable |
| [Roll Out a Latent Dynamics Sequence](problems/tdmpc2-latent-dynamics-sequence/) | 7.1 | Runnable |
| [Build Distributional Reward and Ensemble-Value Targets](problems/tdmpc2-distributional-ensemble-targets/) | 7.1 | Runnable |
| [Score Candidate Action Trajectories](problems/tdmpc2-candidate-trajectory-scores/) | 7.1 | Runnable |
| [Update a Sampling-Based Planner](problems/tdmpc2-weighted-elite-planner/) | 7.1 | Runnable |
| [Validate Success-Classifier Rewards on Robot Failures](problems/serl-success-reward-failure-audit/) | 7.1 | Runnable |
| [Merge Online and Demonstration Replay](problems/serl-merge-replay-sources/) | 7.1 | Runnable |
| [Schedule Actor-Learner Updates](problems/serl-actor-learner-schedule/) | 7.1 | Runnable |
| [Label Human Intervention Segments](problems/hilserl-intervention-segments/) | 7.1 | Runnable |
| [Mix Intervention and Autonomous Replay](problems/hilserl-mix-corrective-replay/) | 7.1 | Runnable |
| [Gate an Online Policy Update](problems/hilserl-autonomous-update-gate/) | 7.1 | Runnable |
| [Record Intervention and Reset Statistics](problems/serl-intervention-reset-statistics/) | 7.1 | Runnable |
| [Sample Time-Contrastive Video Triplets](problems/r3m-time-contrastive-video-triplets/) | 7.1 | Runnable |
| [Combine Temporal and Language Alignment Losses](problems/r3m-temporal-language-objective/) | 7.1 | Runnable |
| [Evaluate Frozen Features in a Small Policy](problems/r3m-frozen-feature-policy-step/) | 7.1 | Runnable |
| [Compute Gait Tracking and Stability Metrics](problems/locomotion-tracking-stability-metrics/) | 7.1 | Runnable |
| [Reset Failed Locomotion Environments](problems/locomotion-failure-reset-batch/) | 7.1 | Runnable |
| [Sample Terrain Difficulty by Policy Progress](problems/locomotion-terrain-progress-curriculum/) | 7.1 | Runnable |
| [Compute Belief Reconstruction and Teacher-Action Losses](problems/perceptive-teacher-belief-loss/) | 7.1 | Runnable |
| [Evaluate Foot Clearance Across Terrain Slices](problems/perceptive-terrain-foot-clearance/) | 7.1 | Runnable |
| [Validate a Tactile Image Capture Contract](problems/digit-capture-contract/) | 7.2 | Runnable |
| [Subtract a Tactile Reference Image](problems/digit-reference-subtraction/) | 7.2 | Runnable |
| [Estimate Contact Patch Statistics](problems/digit-contact-patch-statistics/) | 7.2 | Runnable |
| [Align Tactile Frames with Robot Actions](problems/digit-align-actions/) | 7.2 | Runnable |
| [Score Predicted Tactile Contact Outcomes](problems/digit-predicted-contact-cost/) | 7.2 | Runnable |
| [Integrate a Constant-Jerk Motion Segment](problems/constant-jerk-segment/) | 7.3 | Runnable |
| [Validate a Trajectory Against Derivative Limits](problems/trajectory-derivative-audit/) | 7.3 | Runnable |
| [Build a Joint-Space Smoothness Cost](problems/joint-space-smoothness-cost/) | 7.3 | Runnable |
| [Compute a Signed-Distance Collision Cost](problems/sphere-signed-distance-cost/) | 7.3 | Runnable |
| [Linearize a Signed-Distance Collision Penalty](problems/linearized-collision-penalty/) | 7.3 | Runnable |
| [Bound a Sequential Convex Trust-Region Step](problems/bound-convex-trust-step/) | 7.3 | Runnable |
| [Normalize Exponential Trajectory Cost Weights](problems/exponential-trajectory-weights/) | 7.3 | Runnable |
| [Update a Receding-Horizon Control Sequence](problems/receding-horizon-control-update/) | 7.3 | Runnable |
| [Find Nearby Planning Tree Vertices](problems/nearby-planning-tree-vertices/) | 7.3 | Runnable |
| [Choose a Collision-Free Minimum-Cost Tree Parent](problems/minimum-cost-tree-parent/) | 7.3 | Runnable |
| [Roll Out Perturbed Control Sequences](problems/perturbed-linear-rollouts/) | 7.3 | Runnable |
| [Rewire a Tree Without Creating Cycles](problems/rewire-planning-tree/) | 7.3 | Runnable |
| [Compare Path Cost Across Sampling Budgets](problems/planning-budget-comparison/) | 7.3 | Runnable |
| [Build a Gaussian-Process Smoothness Factor](problems/gp-constant-velocity-factor/) | 7.3 | Runnable |
| [Assemble Obstacle and Prior Residuals](problems/assemble-motion-residuals/) | 7.3 | Runnable |
| [Interpolate a Trajectory Between Support States](problems/gp-support-interpolation/) | 7.3 | Runnable |
| [Push Robot State into a Task Space](problems/push-task-state/) | 7.3 | Runnable |
| [Pull Back a Local Motion Metric](problems/pullback-motion-metric/) | 7.3 | Runnable |
| [Combine Competing Task-Space Accelerations](problems/combine-motion-policies/) | 7.3 | Runnable |
| [Rank Multi-Seed Motion Trajectories](problems/rank-motion-candidates/) | 7.3 | Runnable |
| [Select High-Gradient Image Points](problems/select-gradient-image-points/) | 7.4 | Runnable |
| [Warp a Point Between Calibrated Frames](problems/warp-calibrated-pixels/) | 7.4 | Runnable |
| [Compute an Exposure-Corrected Photometric Residual](problems/exposure-photometric-residual/) | 7.4 | Runnable |
| [Compute Point-to-Line and Point-to-Plane Scan Residuals](problems/lidar-feature-residuals/) | 7.4 | Runnable |
| [Associate Scan Points with Local Map Planes](problems/associate-local-map-planes/) | 7.4 | Runnable |
| [Deskew a Lidar Scan with Motion Estimates](problems/deskew-lidar-points/) | 7.4 | Runnable |
| [Apply SE(3) Exponential and Logarithm Maps](problems/se3-exponential-logarithm/) | 7.4 | Runnable |
| [Integrate IMU Rotation Increments on SO3](problems/integrate-imu-rotation/) | 7.4 | Runnable |
| [Preintegrate Bias-Corrected IMU Velocity and Position](problems/preintegrate-imu-translation/) | 7.4 | Runnable |
| [Apply a First-Order Bias Correction](problems/first-order-imu-bias-correction/) | 7.4 | Runnable |
| [Apply Homographic Keypoint Adaptation](problems/homographic-keypoint-adaptation/) | 7.4 | Runnable |
| [Evaluate Keypoint Repeatability](problems/keypoint-repeatability/) | 7.4 | Runnable |
| [Build Homography-Supervised Descriptor Correspondence Targets](problems/homography-descriptor-targets/) | 7.4 | Runnable |
| [Sample Descriptors at Keypoint Coordinates](problems/sample-keypoint-descriptors/) | 7.4 | Runnable |
| [Build a Feature-Matching Score Matrix](problems/feature-matching-score-matrix/) | 7.4 | Runnable |
| [Normalize Assignments with Sinkhorn Iterations](problems/log-sinkhorn-assignments/) | 7.4 | Runnable |
| [Reject Unmatched Features with Dustbins](problems/dustbin-partial-assignment/) | 7.4 | Runnable |
| [Extract Mutual Matches and Unmatched Labels from Transport Scores](problems/extract-mutual-feature-matches/) | 7.4 | Runnable |
| [Apply Paired-Image Self and Cross Attention](problems/paired-linear-image-attention/) | 7.4 | Runnable |
| [Construct Coarse Correspondence Candidates](problems/dual-softmax-coarse-matches/) | 7.4 | Runnable |
| [Refine a Match in a Local Window](problems/local-window-match-expectation/) | 7.4 | Runnable |
| [Filter Geometrically Inconsistent Matches](problems/sampson-epipolar-match-gate/) | 7.4 | Runnable |
| [Detect Unobservable Initialization Motion](problems/initialization-observability-rank/) | 7.4 | Runnable |
| [Preintegrate a Short IMU Window](problems/short-window-imu-preintegration/) | 7.4 | Runnable |
| [Build a Visual-Inertial Residual](problems/visual-inertial-keyframe-residual/) | 7.4 | Runnable |
| [Marginalize a Visual-Inertial Window with a Schur Complement](problems/schur-window-marginalization/) | 7.4 | Runnable |
| [Associate Map Points with Image Features](problems/pose-guided-binary-feature-association/) | 7.4 | Runnable |
| [Select Geometric Pose Inliers](problems/reprojection-pose-hypothesis-inliers/) | 7.4 | Runnable |
| [Evaluate a Relocalization Candidate](problems/relocalization-landmark-coverage/) | 7.4 | Runnable |
| [Evaluate Trajectory Error After Alignment](problems/aligned-trajectory-position-error/) | 7.4 | Runnable |
| [Construct Relative Pose Measurements from Local Odometry](problems/relative-odometry-edges/) | 7.4 | Runnable |
| [Assemble Sensor-Specific Pose Factors](problems/global-sensor-pose-factors/) | 7.4 | Runnable |
| [Compare Drift Across Sensor Configurations](problems/sensor-configuration-drift/) | 7.4 | Runnable |
| [Propagate Preintegration Covariance](problems/imu-preintegration-covariance/) | 7.4 | Runnable |
| [Assemble an IMU-Lidar Pose Constraint](problems/imu-lidar-extrinsic-pose-residual/) | 7.4 | Runnable |
| [Reject Inconsistent Loop Closures](problems/loop-closure-consistency-gate/) | 7.4 | Runnable |
| [Update an Incremental Local Map](problems/incremental-voxel-local-map/) | 7.4 | Runnable |
| [Validate a Visual-Inertial Initialization](problems/visual-inertial-initialization-gate/) | 7.4 | Runnable |
| [Measure Per-Channel Activation and Weight Ranges](problems/smoothquant-channel-ranges/) | 7.5 | Runnable |
| [Apply an Equivalent Channel Rescaling](problems/smoothquant-equivalent-rescaling/) | 7.5 | Runnable |
| [Quantize Weights and Activations to Int8](problems/smoothquant-int8-linear-layer/) | 7.5 | Runnable |
| [Validate Layer Output Error After Smoothing](problems/smoothquant-layer-error-report/) | 7.5 | Runnable |
| [Apply a Weight-Pruning Mask](problems/deep-compression-pruning-mask/) | 7.5 | Runnable |
| [Quantize Shared Weight Centroids](problems/deep-compression-centroid-assignment/) | 7.5 | Runnable |
| [Compute a Compressed Model Storage Budget](problems/deep-compression-storage-budget/) | 7.5 | Runnable |
| [Compare Activation-Weighted Quantization Error](problems/awq-activation-weighted-error/) | 7.5 | Runnable |
| [Compute Group-Wise Quantization Parameters](problems/awq-groupwise-quantization/) | 7.5 | Runnable |
| [Calibrate and Evaluate a Smoothed Int8 Layer](problems/smoothquant-calibrated-layer-integration/) | 7.5 | Runnable |
| [Recover Failed Worker Tasks Idempotently](problems/ray-recovery-reconciliation/) | 7.5 | Runnable |
| [Track Immutable Artifact References](problems/ray-immutable-object-locations/) | 7.5 | Runnable |
| [Track Policy Version Staleness](problems/rllib-policy-version-staleness/) | 7.5 | Runnable |
| [Aggregate Weighted Learner Gradients](problems/rllib-weighted-learner-gradients/) | 7.5 | Runnable |
| [Split Demonstrations by Scene and Collector](problems/droid-scene-collector-split/) | 7.5 | Runnable |
| [Audit Data and Calibration Lineage](problems/droid-calibration-lineage-audit/) | 7.5 | Runnable |
| [Validate a Robot Dataset Datasheet](problems/robot-dataset-datasheet-schema/) | 7.5 | Runnable |
| [Generate a Data-Use Risk Report](problems/robot-data-use-risk-report/) | 7.5 | Runnable |
| [Validate a Model Card Schema](problems/robot-model-card-schema/) | 7.5 | Runnable |
| [Detect Paused or Corrupted Action Segments](problems/roboturk-action-segments/) | 7.5 | Runnable |
| [Compute an Interquartile Mean Benchmark Score](problems/rliable-interquartile-mean/) | 7.5 | Runnable |
| [Bootstrap a Stratified Performance Profile](problems/rliable-stratified-performance-profile/) | 7.5 | Runnable |
| [Validate a Continuous-Control Time Step](problems/dm-control-timestep-validation/) | 7.5 | Runnable |
| [Implement Action Repeat Correctly](problems/dm-control-action-repeat/) | 7.5 | Runnable |
| [Evaluate a Bounded Continuous-Control Reward](problems/dm-control-tolerance-reward/) | 7.5 | Runnable |
| [Aggregate Seeded Benchmark Returns](problems/dm-control-seeded-return-summary/) | 7.5 | Runnable |
| [Batch Independent Simulator States](problems/isaac-gym-batch-joint-state/) | 7.5 | Runnable |
| [Reset Completed Environments Selectively](problems/simulator-selective-environment-reset/) | 7.5 | Runnable |
| [Measure Simulation and Learning Throughput](problems/isaac-gym-steady-state-throughput/) | 7.5 | Runnable |
| [Implement a Functional Physics Step Contract](problems/brax-functional-damped-step/) | 7.5 | Runnable |
| [Build a Continual-Learning Task Sequence](problems/libero-continual-task-schedule/) | 7.5 | Runnable |
| [Separate Task Semantics from Scene Variation](problems/libero-semantic-scene-factors/) | 7.5 | Runnable |
| [Record a Continual-Learning Evaluation Matrix](problems/libero-evaluation-history-matrix/) | 7.5 | Runnable |
| [Compute a Forward and Backward Transfer Matrix](problems/libero-forward-backward-transfer/) | 7.5 | Runnable |
| [Align Actions and Images in a Video Window](problems/robonet-transition-frame-windows/) | 7.5 | Runnable |
| [Compute a Masked Video-Prediction Loss](problems/robonet-masked-video-prediction-loss/) | 7.5 | Runnable |
| [Measure Cross-Robot Prediction Error](problems/robonet-cross-robot-prediction-error/) | 7.5 | Runnable |
| [Align Egocentric Video Annotations](problems/ego4d-annotation-frame-ranges/) | 7.5 | Runnable |
| [Build Leakage-Safe Temporal Splits](problems/ego4d-temporal-leakage-groups/) | 7.5 | Runnable |
| [Aggregate Evaluation by Activity Slice](problems/egocentric-activity-confusion-report/) | 7.5 | Runnable |
| [Decode Normalized Boxes and Classes from Object Queries](problems/detr-decode-object-queries/) | 7.6 | Runnable |
| [Flatten Spatial Features with Position and Padding Metadata](problems/detr-flatten-spatial-metadata/) | 7.6 | Runnable |
| [Read a Normalized Class Token with a Linear Head](problems/vit-class-token-linear-head/) | 7.6 | Runnable |
| [Transform Prompt Coordinates Through Image Preprocessing](problems/sam-transform-prompt-coordinates/) | 7.6 | Runnable |
| [Reuse Image Embeddings Without Stale-Cache Errors](problems/sam-image-embedding-cache-key/) | 7.6 | Runnable |
| [Sample Calibrated Multi-Camera Feature Maps](problems/bev-bilinear-camera-sampling/) | 7.6 | Runnable |
| [Sample Hierarchical Depth Intervals](problems/nerf-hierarchical-depth-sampling/) | 7.6 | Runnable |
| [Differentiate Rendered Color on a Small Synthetic Field](problems/nerf-rendered-color-gradients/) | 7.6 | Runnable |
| [Implement Nearest-Neighbor Feature-Spreading Regularization](problems/dinov2-neighbor-feature-spreading/) | 7.6 | Runnable |
| [Fit a Tiny Coordinate-Feature Radiance Field](problems/nerf-tiny-field-training/) | 7.6 | Runnable |
| [Fuse Masked Image and Text Tokens with Bidirectional Cross-Attention](problems/grounding-bidirectional-cross-attention/) | 7.7 | Runnable |
| [Evaluate Localization and Phrase Grounding Separately](problems/grounding-localization-phrase-metrics/) | 7.7 | Runnable |
| [Encode Synchronized Observations for an Action Denoiser](problems/diffusion-observation-window-encoder/) | 7.7 | Runnable |
| [Build a Conditional Action Denoiser](problems/diffusion-conditional-temporal-denoiser/) | 7.7 | Runnable |
