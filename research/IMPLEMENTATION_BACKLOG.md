# Remaining paper implementation backlog

Inventory snapshot: 193 published problems; 457 proposed paper-stage associations collapse to 450 unique normalized titles. Seven exact-title matches were reviewed and reused as explicitly scoped bounded components. The other 443 are proposed contracts, not 443 automatically distinct implementations: semantic overlap and paper-specific requirements must be reviewed before authoring.

No graph association or source-card link establishes full paper reproduction. A paper integration is complete only when its bounded data path, executable entrypoint, evaluation cases, failure analysis and reproducibility note are implemented and reviewed.

## Current batch status

Eleven new PPO/SAC/IQL packages are published and cover twelve proposed titles because the one-step Bellman target is shared. Independent contract and code review, actual isolated Run/Submit and negative controls passed. Seven additional proposed titles reuse reviewed existing bounded components. The remaining 431 unique titles are pending; full paper integrations remain separate.

## Workflow and milestones

1. Review existing-contract matches, preserving source-specific semantics and identifying prerequisites separately.
2. Review atomic blueprints in coherent batches of 8–12; publish only after reference Run/Submit plus starter and mechanism-negative tests.
3. Compose bounded paper integrations from reviewed components, using the same isolated worker and a project manifest agreed with the project-UI owner.
4. Keep missing training, weights, data, closed-loop evaluation and benchmark claims explicitly outside scope.

First batch: PPO surrogate/normalization/targets/diagnostics; SAC target/value/log-probability correction/temperature extension; IQL expectile/critic targets/advantage weights. The SAC temperature extension is labelled later work rather than attributed to the original 2018 paper.

## geometry-calibration-slam

| ID | Proposed exercise | Paper IDs | Status / existing contract |
|---|---|---|---|
| PB-018 | Apply a First-Order Bias Correction | 2015-on-manifold-preintegration | Needs reviewed blueprint |
| PB-025 | Apply Homographic Keypoint Adaptation | 2017-superpoint | Needs reviewed blueprint |
| PB-026 | Apply Paired-Image Self and Cross Attention | 2021-loftr | Needs reviewed blueprint |
| PB-027 | Apply Recurrent Dense Correspondence and Confidence Updates | 2021-droid-slam | Needs reviewed blueprint |
| PB-028 | Apply SE(3) Exponential and Logarithm Maps | 2018-micro-lie-theory | Needs reviewed blueprint |
| PB-031 | Assemble an IMU-Lidar Pose Constraint | 2020-lio-sam | Needs reviewed blueprint |
| PB-033 | Assemble Sensor-Specific Pose Factors | 2019-vins-fusion | Needs reviewed blueprint |
| PB-034 | Assemble Sparse and Dense RGB-D Alignment Residuals | 2016-bundlefusion | Needs reviewed blueprint |
| PB-036 | Associate Map Points with Image Features | 2016-orb-slam-2 | Needs reviewed blueprint |
| PB-037 | Associate Scan Points with Local Map Planes | 2021-fast-lio-2 | Needs reviewed blueprint |
| PB-052 | Build a Dense Reprojection Residual | 2021-droid-slam | Needs reviewed blueprint |
| PB-053 | Build a Feature-Matching Score Matrix | 2019-superglue | Needs reviewed blueprint |
| PB-061 | Build a Visual-Inertial Residual | 2017-vins-mono | Needs reviewed blueprint |
| PB-066 | Build Homography-Supervised Descriptor Correspondence Targets | 2017-superpoint | Needs reviewed blueprint |
| PB-081 | Choose Keyframes by Reconstruction Error | 2021-imap | Needs reviewed blueprint |
| PB-092 | Combine Reprojection and Inertial Residuals in a Local Window | 2020-orb-slam-3 | Needs reviewed blueprint |
| PB-098 | Compare Drift Across Sensor Configurations | 2019-vins-fusion | Needs reviewed blueprint |
| PB-121 | Compute a Point-to-Plane Residual | 2021-fast-lio-2 | Needs reviewed blueprint |
| PB-128 | Compute an Exposure-Corrected Photometric Residual | 2016-direct-sparse-odometry | Needs reviewed blueprint |
| PB-141 | Compute Point-to-Line and Point-to-Plane Scan Residuals | 2020-lio-sam | Needs reviewed blueprint |
| PB-153 | Construct Coarse Correspondence Candidates | 2021-loftr | Needs reviewed blueprint |
| PB-160 | Construct Relative Pose Measurements from Local Odometry | 2019-vins-fusion | Needs reviewed blueprint |
| PB-171 | Decode Occupancy and Color from Hierarchical Scene Features | 2021-nice-slam | Needs reviewed blueprint |
| PB-174 | Deskew a Lidar Scan with Motion Estimates | 2020-lio-sam | Needs reviewed blueprint |
| PB-180 | Detect Unobservable Initialization Motion | 2017-vins-mono | Needs reviewed blueprint |
| PB-199 | Evaluate a Relocalization Candidate | 2016-orb-slam-2 | Needs reviewed blueprint |
| PB-204 | Evaluate Keypoint Repeatability | 2017-superpoint | Needs reviewed blueprint |
| PB-219 | Evaluate Trajectory Error After Alignment | 2020-orb-slam-3 | Needs reviewed blueprint |
| PB-224 | Extract Mutual Matches and Unmatched Labels from Transport Scores | 2019-superglue | Needs reviewed blueprint |
| PB-225 | Filter Geometrically Inconsistent Matches | 2021-loftr | Needs reviewed blueprint |
| PB-230 | Finite-Difference Gradient Check | 2018-micro-lie-theory | [Reused bounded component](/problems/finite-difference-gradient-check) |
| PB-243 | Handle Asynchronous Sensor Timestamps | 2019-vins-fusion | Needs reviewed blueprint |
| PB-251 | Integrate a Depth Frame into a TSDF | 2016-bundlefusion | Needs reviewed blueprint |
| PB-252 | Integrate IMU Rotation Increments on SO3 | 2015-on-manifold-preintegration | Needs reviewed blueprint |
| PB-263 | Marginalize a Visual-Inertial Window with a Schur Complement | 2017-vins-mono | Needs reviewed blueprint |
| PB-277 | Measure Pose and Reconstruction Error | 2021-nice-slam | Needs reviewed blueprint |
| PB-282 | Merge Consistent Map Transforms | 2020-orb-slam-3 | Needs reviewed blueprint |
| PB-291 | Normalize Assignments with Sinkhorn Iterations | 2019-superglue | Needs reviewed blueprint |
| PB-297 | Optimize a Camera Pose Against a Neural Map | 2021-imap | Needs reviewed blueprint |
| PB-302 | Preintegrate a Short IMU Window | 2017-vins-mono | Needs reviewed blueprint |
| PB-303 | Preintegrate Bias-Corrected IMU Velocity and Position | 2015-on-manifold-preintegration | Needs reviewed blueprint |
| PB-311 | Propagate an Error-State IMU Mean and Covariance | 2021-fast-lio-2 | Needs reviewed blueprint |
| PB-312 | Propagate Preintegration Covariance | 2015-on-manifold-preintegration | Needs reviewed blueprint |
| PB-318 | Query Color and Density from a Coordinate MLP | 2021-imap | Needs reviewed blueprint |
| PB-319 | Query Multi-Resolution Scene Features | 2021-nice-slam | Needs reviewed blueprint |
| PB-331 | Refine a Match in a Local Window | 2021-loftr | Needs reviewed blueprint |
| PB-332 | Reintegrate Geometry After a Pose Correction | 2016-bundlefusion | Needs reviewed blueprint |
| PB-333 | Reject Inconsistent Loop Closures | 2020-lio-sam | Needs reviewed blueprint |
| PB-334 | Reject Unmatched Features with Dustbins | 2019-superglue | Needs reviewed blueprint |
| PB-358 | Sample Descriptors at Keypoint Coordinates | 2017-superpoint | Needs reviewed blueprint |
| PB-361 | Sample Informative Mapping Pixels | 2021-imap | Needs reviewed blueprint |
| PB-362 | Sample Rays for Online Mapping | 2021-nice-slam | Needs reviewed blueprint |
| PB-376 | Select Edges for a Frame Graph | 2021-droid-slam | Needs reviewed blueprint |
| PB-377 | Select Geometric Pose Inliers | 2016-orb-slam-2 | Needs reviewed blueprint |
| PB-379 | Select High-Gradient Image Points | 2016-direct-sparse-odometry | Needs reviewed blueprint |
| PB-402 | Update a Global Pose Graph | 2016-bundlefusion | Needs reviewed blueprint |
| PB-406 | Update an Incremental Local Map | 2021-fast-lio-2 | Needs reviewed blueprint |
| PB-407 | Update Poses in a Small Bundle-Adjustment Problem | 2021-droid-slam | Needs reviewed blueprint |
| PB-425 | Validate a Visual-Inertial Initialization | 2020-orb-slam-3 | Needs reviewed blueprint |
| PB-447 | Warp a Point Between Calibrated Frames | 2016-direct-sparse-odometry | Needs reviewed blueprint |

## humanoid-dexterity-tactile

| ID | Proposed exercise | Paper IDs | Status / existing contract |
|---|---|---|---|
| PB-016 | Align Tactile Frames with Robot Actions | 2020-digit-tactile-sensor | Needs reviewed blueprint |
| PB-017 | Align Terrain Samples to the Robot Frame | 2022-perceptive-locomotion | Needs reviewed blueprint |
| PB-043 | Balance Task and Style Objectives | 2021-adversarial-motion-priors | Needs reviewed blueprint |
| PB-074 | Build Privileged Dynamics-Latent Supervision | 2021-rapid-motor-adaptation | Needs reviewed blueprint |
| PB-091 | Combine Imitation and Task Rewards for Motion Control | 2018-deepmimic | Needs reviewed blueprint |
| PB-114 | Compute a Contact-Based Manipulation Reward | 2022-dexpoint | Needs reviewed blueprint |
| PB-116 | Compute a Hand-Retargeting Geometry Residual | 2021-dexmv | Needs reviewed blueprint |
| PB-123 | Compute an Adversarial Style Reward | 2021-adversarial-motion-priors | Needs reviewed blueprint |
| PB-130 | Compute Belief Reconstruction and Teacher-Action Losses | 2022-perceptive-locomotion | Needs reviewed blueprint |
| PB-133 | Compute Gait Tracking and Stability Metrics | 2021-learning-to-walk-in-minutes | Needs reviewed blueprint |
| PB-139 | Compute Object Rotation Tracking Error | 2018-learning-dexterous-manipulation | Needs reviewed blueprint |
| PB-142 | Compute Pose and Velocity Imitation Rewards | 2018-deepmimic | Needs reviewed blueprint |
| PB-156 | Construct Motion Discriminator Features | 2021-adversarial-motion-priors | Needs reviewed blueprint |
| PB-178 | Detect Phase Misalignment in a Motion Clip | 2018-deepmimic | Needs reviewed blueprint |
| PB-179 | Detect Stale Perception in a Control Window | 2022-perceptive-locomotion | Needs reviewed blueprint |
| PB-191 | Estimate a Latent Dynamics Context | 2021-rapid-motor-adaptation | Needs reviewed blueprint |
| PB-192 | Estimate Contact Patch Statistics | 2020-digit-tactile-sensor | Needs reviewed blueprint |
| PB-201 | Evaluate Foot Clearance Across Terrain Slices | 2022-perceptive-locomotion | Needs reviewed blueprint |
| PB-209 | Evaluate Novel-Object Generalization | 2022-dexpoint | Needs reviewed blueprint |
| PB-212 | Evaluate Policy Recovery After a Parameter Change | 2021-rapid-motor-adaptation | Needs reviewed blueprint |
| PB-214 | Evaluate Retargeted Motion Feasibility | 2021-dexmv | Needs reviewed blueprint |
| PB-215 | Evaluate Robustness to Sensor and Actuator Noise | 2018-learning-dexterous-manipulation | Needs reviewed blueprint |
| PB-253 | Interpolate a Reference Motion Pose | 2018-deepmimic | Needs reviewed blueprint |
| PB-259 | Map Human Demonstration Segments to Robot Time | 2021-dexmv | Needs reviewed blueprint |
| PB-283 | Merge Observed and Imagined Hand Point Clouds | 2022-dexpoint | Needs reviewed blueprint |
| PB-343 | Reset Failed Locomotion Environments | 2021-learning-to-walk-in-minutes | Needs reviewed blueprint |
| PB-359 | Sample Hand Dynamics Randomization | 2018-learning-dexterous-manipulation | Needs reviewed blueprint |
| PB-363 | Sample Terrain Difficulty by Policy Progress | 2021-learning-to-walk-in-minutes | Needs reviewed blueprint |
| PB-368 | Score a Privileged Terrain Teacher Rollout | 2022-perceptive-locomotion | Needs reviewed blueprint |
| PB-372 | Score Predicted Tactile Contact Outcomes | 2020-digit-tactile-sensor | Needs reviewed blueprint |
| PB-387 | Subtract a Tactile Reference Image | 2020-digit-tactile-sensor | Needs reviewed blueprint |
| PB-397 | Track the Age of an Asynchronous Adaptation Latent | 2021-rapid-motor-adaptation | Needs reviewed blueprint |
| PB-412 | Validate a Hand-Object Pose Sequence | 2021-dexmv | Needs reviewed blueprint |
| PB-422 | Validate a Tactile Image Capture Contract | 2020-digit-tactile-sensor | Needs reviewed blueprint |
| PB-426 | Validate Actions Inferred from Retargeted States | 2021-dexmv | Needs reviewed blueprint |
| PB-450 | Window Proprioceptive History | 2021-rapid-motor-adaptation | Needs reviewed blueprint |

## mlops-data-deployment

| ID | Proposed exercise | Paper IDs | Status / existing contract |
|---|---|---|---|
| PB-003 | Aggregate Evaluation by Activity Slice | 2021-ego4d, 2023-ego-exo4d | Needs reviewed blueprint |
| PB-004 | Aggregate Generalization Across Scene Families | 2024-robocasa | Needs reviewed blueprint |
| PB-005 | Aggregate Metrics by Operational Slice | 2018-model-cards | Needs reviewed blueprint |
| PB-009 | Aggregate Weighted Learner Gradients | 2017-rllib | Needs reviewed blueprint |
| PB-010 | Align Actions and Images in a Video Window | 2019-robonet | Needs reviewed blueprint |
| PB-012 | Align Egocentric Video Annotations | 2021-ego4d | Needs reviewed blueprint |
| PB-020 | Apply a Weight-Pruning Mask | 2015-deep-compression | Needs reviewed blueprint |
| PB-021 | Apply an Equivalent Channel Rescaling | 2022-smoothquant | Needs reviewed blueprint |
| PB-039 | Audit Data and Calibration Lineage | 2024-droid | Needs reviewed blueprint |
| PB-044 | Batch Actor Samples into Learner Updates | 2017-rllib | Needs reviewed blueprint |
| PB-047 | Bootstrap a Stratified Performance Profile | 2021-rliable-statistical-precipice | Needs reviewed blueprint |
| PB-051 | Build a Continual-Learning Task Sequence | 2023-libero | Needs reviewed blueprint |
| PB-070 | Build Leakage-Safe Temporal Splits | 2021-ego4d | Needs reviewed blueprint |
| PB-095 | Compare Activation-Weighted Quantization Error | 2023-awq | Needs reviewed blueprint |
| PB-106 | Compare Slice Metrics Without Hiding Regressions | 2021-rliable-statistical-precipice | [Reused bounded component](/problems/slice-metrics-regressions) |
| PB-111 | Compute a Compressed Model Storage Budget | 2015-deep-compression | Needs reviewed blueprint |
| PB-115 | Compute a Forward and Backward Transfer Matrix | 2023-libero | Needs reviewed blueprint |
| PB-119 | Compute a Masked Video-Prediction Loss | 2019-robonet | Needs reviewed blueprint |
| PB-129 | Compute an Interquartile Mean Benchmark Score | 2021-rliable-statistical-precipice | Needs reviewed blueprint |
| PB-131 | Compute Collector and Task Coverage | 2018-datasheets-for-datasets, 2018-roboturk | Needs reviewed blueprint |
| PB-132 | Compute Confidence Intervals Across Robot Episodes | 2021-rliable-statistical-precipice | [Reused bounded component](/problems/robot-episode-confidence-intervals) |
| PB-134 | Compute Group-Wise Quantization Parameters | 2023-awq | Needs reviewed blueprint |
| PB-176 | Detect Missing Provenance Fields | 2018-datasheets-for-datasets | Needs reviewed blueprint |
| PB-177 | Detect Paused or Corrupted Action Segments | 2018-roboturk | Needs reviewed blueprint |
| PB-194 | Estimate Quantized VLA Backbone Memory | 2023-awq | Needs reviewed blueprint |
| PB-220 | Evaluate Transfer by Environment Slice | 2023-bridgedata-v2 | Needs reviewed blueprint |
| PB-240 | Generate a Data-Use Risk Report | 2018-datasheets-for-datasets | Needs reviewed blueprint |
| PB-260 | Map Operator Motion into a Robot Control Frame | 2018-roboturk | Needs reviewed blueprint |
| PB-271 | Measure Cross-Robot Prediction Error | 2019-robonet | Needs reviewed blueprint |
| PB-276 | Measure Per-Channel Activation and Weight Ranges | 2022-smoothquant | Needs reviewed blueprint |
| PB-279 | Measure Sampling and Learning Throughput | 2017-rllib | Needs reviewed blueprint |
| PB-295 | Normalize Multi-Environment Robot Records | 2023-bridgedata-v2 | Needs reviewed blueprint |
| PB-305 | Project a Tracked Point Across Views | 2023-ego-exo4d, 2020-sapien | Needs reviewed blueprint |
| PB-316 | Quantize Shared Weight Centroids | 2015-deep-compression | Needs reviewed blueprint |
| PB-317 | Quantize Weights and Activations to Int8 | 2022-smoothquant | Needs reviewed blueprint |
| PB-327 | Record a Continual-Learning Evaluation Matrix | 2023-libero | Needs reviewed blueprint |
| PB-330 | Recover Failed Worker Tasks Idempotently | 2017-ray | Needs reviewed blueprint |
| PB-370 | Score Chained Task Success | 2021-calvin, 2021-habitat-2 | Needs reviewed blueprint |
| PB-374 | Segment a Long-Horizon Robot Rollout | 2021-calvin | Needs reviewed blueprint |
| PB-381 | Separate Task Semantics from Scene Variation | 2023-libero | Needs reviewed blueprint |
| PB-383 | Split Demonstrations by Scene and Collector | 2024-droid | Needs reviewed blueprint |
| PB-386 | Stratify Tasks by Scene Factors | 2024-robocasa | Needs reviewed blueprint |
| PB-388 | Synchronize Ego and Exo Camera Events | 2023-ego-exo4d | Needs reviewed blueprint |
| PB-394 | Track Immutable Artifact References | 2017-ray | Needs reviewed blueprint |
| PB-396 | Track Policy Version Staleness | 2017-rllib | Needs reviewed blueprint |
| PB-410 | Validate a Distributed Robot Episode | 2024-droid | Needs reviewed blueprint |
| PB-413 | Validate a Kitchen Scenario Configuration | 2024-robocasa | Needs reviewed blueprint |
| PB-414 | Validate a Model Card Schema | 2018-model-cards | Needs reviewed blueprint |
| PB-418 | Validate a Robot Dataset Datasheet | 2018-datasheets-for-datasets | Needs reviewed blueprint |
| PB-423 | Validate a Teleoperation Demonstration | 2018-roboturk, 2024-robocasa | Needs reviewed blueprint |
| PB-431 | Validate Language-to-Episode Annotations | 2021-calvin | Needs reviewed blueprint |
| PB-432 | Validate Layer Output Error After Smoothing | 2022-smoothquant | Needs reviewed blueprint |
| PB-434 | Validate Multi-View Calibration Metadata | 2023-ego-exo4d | Needs reviewed blueprint |
| PB-445 | Version a Cross-Robot Dataset Manifest | 2021-rlds | [Reused bounded component](/problems/oxe-version-dataset-manifest) |
| PB-449 | Window an Episode Without Crossing Boundaries | 2021-rlds | [Reused bounded component](/problems/window-episode-without-crossing-boundaries) |

## mlops-sim2real

| ID | Proposed exercise | Paper IDs | Status / existing contract |
|---|---|---|---|
| PB-041 | Average Per-Scenario Perception Losses | 2017-domain-randomization | Needs reviewed blueprint |
| PB-105 | Compare Schedules with Reproducible Latency Measurement | 2018-tvm | Needs reviewed blueprint |
| PB-117 | Compute a Masked Behavior-Cloning Log-Likelihood | 2021-robomimic | Needs reviewed blueprint |
| PB-135 | Compute Inference Throughput from Query Traces | 2019-mlperf-inference | Needs reviewed blueprint |
| PB-165 | Declare Reproducible Robotics Benchmark Boundaries | 2023-robotperf | Needs reviewed blueprint |

## perception-3d

| ID | Proposed exercise | Paper IDs | Status / existing contract |
|---|---|---|---|
| PB-015 | Align relative inverse-depth predictions | 2024-depth-anything-v2 | Needs reviewed blueprint |
| PB-030 | Apply valid/ignored anchor masks and reductions | 2017-focal-loss-retinanet | Needs reviewed blueprint |
| PB-035 | Assign regions to pyramid levels | 2016-feature-pyramid-networks | Needs reviewed blueprint |
| PB-063 | Build an all-pairs correlation tensor | 2020-raft | Needs reviewed blueprint |
| PB-065 | Build Gaussian Covariances from Rotation and Scale | 2023-3d-gaussian-splatting | Needs reviewed blueprint |
| PB-088 | Collect Intermediate Transformer Tokens with Patch-Grid Metadata | 2021-dense-prediction-transformers | Needs reviewed blueprint |
| PB-096 | Compare aligned and metric depth errors | 2021-dense-prediction-transformers | Needs reviewed blueprint |
| PB-099 | Compare gradient weights across confidence levels | 2017-focal-loss-retinanet | Needs reviewed blueprint |
| PB-100 | Compare instance-mask IoU and box IoU | 2017-mask-r-cnn | Needs reviewed blueprint |
| PB-108 | Composite depth-ordered Gaussian contributions | 2023-3d-gaussian-splatting | Needs reviewed blueprint |
| PB-118 | Compute a Masked Patch Reconstruction Loss | 2021-masked-autoencoders | Needs reviewed blueprint |
| PB-152 | Construct class-specific mask targets | 2017-mask-r-cnn | Needs reviewed blueprint |
| PB-157 | Construct objectness and independent class targets | 2018-yolov3 | Needs reviewed blueprint |
| PB-161 | Convert Dense Class Logits to Independent Sigmoid Probabilities | 2017-focal-loss-retinanet | Needs reviewed blueprint |
| PB-164 | Create Teacher Depth Targets with Validity and Preprocessing Metadata | 2024-depth-anything-v2 | Needs reviewed blueprint |
| PB-169 | Decode multi-scale anchor predictions | 2018-yolov3 | Needs reviewed blueprint |
| PB-184 | Encode and decode proposal regression targets | 2015-faster-r-cnn | Needs reviewed blueprint |
| PB-206 | Evaluate mask drift, absence, and correction recovery | 2024-sam-2 | Needs reviewed blueprint |
| PB-207 | Evaluate metric error by distance and surface type | 2024-depth-anything-v2 | Needs reviewed blueprint |
| PB-227 | Filter proposals and test region-feature alignment | 2015-faster-r-cnn | Needs reviewed blueprint |
| PB-233 | Fuse lateral and top-down maps | 2016-feature-pyramid-networks | Needs reviewed blueprint |
| PB-235 | Fuse multi-resolution dense features | 2021-dense-prediction-transformers | Needs reviewed blueprint |
| PB-239 | Gather Visible Patch Tokens with Position Indices | 2021-masked-autoencoders | Needs reviewed blueprint |
| PB-241 | Generate default boxes at multiple scales | 2015-ssd | Needs reviewed blueprint |
| PB-242 | Generate dense anchors | 2015-faster-r-cnn | Needs reviewed blueprint |
| PB-246 | Implement bilinear ROI sampling | 2017-mask-r-cnn | Needs reviewed blueprint |
| PB-247 | Implement farthest-point sampling | 2017-pointnet-plus-plus | Needs reviewed blueprint |
| PB-249 | Implement stable sigmoid focal loss | 2017-focal-loss-retinanet | Needs reviewed blueprint |
| PB-255 | Interpolate coarse features onto fine points | 2017-pointnet-plus-plus | Needs reviewed blueprint |
| PB-258 | Maintain object-specific video memory | 2024-sam-2 | Needs reviewed blueprint |
| PB-261 | Map Proposal Boxes to Feature-Map Coordinates | 2017-mask-r-cnn | Needs reviewed blueprint |
| PB-265 | Mask invalid depth boundaries | 2024-depth-anything-v2 | Needs reviewed blueprint |
| PB-268 | Match defaults with deterministic tie handling | 2015-ssd | Needs reviewed blueprint |
| PB-278 | Measure primitive contribution for density control | 2023-3d-gaussian-splatting | Needs reviewed blueprint |
| PB-299 | Perform bounded-radius neighborhood grouping | 2017-pointnet-plus-plus | Needs reviewed blueprint |
| PB-300 | Pool Proposal Regions and Apply Class-Specific Box Deltas | 2015-faster-r-cnn | Needs reviewed blueprint |
| PB-306 | Project anisotropic covariance into an image | 2023-3d-gaussian-splatting | Needs reviewed blueprint |
| PB-308 | Project Multi-Scale Backbone Maps to a Shared Channel Width | 2016-feature-pyramid-networks | Needs reviewed blueprint |
| PB-326 | Reassemble tokens into feature maps | 2021-dense-prediction-transformers | Needs reviewed blueprint |
| PB-354 | Sample a correlation pyramid around flow estimates | 2020-raft | Needs reviewed blueprint |
| PB-356 | Sample and Restore Masked Image Patches | 2021-masked-autoencoders | Needs reviewed blueprint |
| PB-378 | Select hard negative classification examples | 2015-ssd | Needs reviewed blueprint |
| PB-380 | Select memory frames under a fixed budget | 2024-sam-2 | Needs reviewed blueprint |
| PB-399 | Transform Current-Frame Prompts into Encoded Image Coordinates | 2024-sam-2 | Needs reviewed blueprint |
| PB-443 | Verify odd-resolution shape alignment | 2016-feature-pyramid-networks | Needs reviewed blueprint |
| PB-444 | Verify tensor flattening and scale transforms | 2018-yolov3 | Needs reviewed blueprint |
| PB-448 | Warp images and evaluate endpoint error | 2020-raft | Needs reviewed blueprint |

## planning-control-ik

| ID | Proposed exercise | Paper IDs | Status / existing contract |
|---|---|---|---|
| PB-001 | Add Noise to a Joint-Space Path | 2023-motion-planning-diffusion | Needs reviewed blueprint |
| PB-023 | Apply Collision-Cost Guidance During Denoising | 2023-motion-planning-diffusion | Needs reviewed blueprint |
| PB-032 | Assemble Obstacle and Prior Residuals | 2017-gaussian-process-motion-planning | Needs reviewed blueprint |
| PB-045 | Batch Forward-Kinematics Queries | 2023-curobo | Needs reviewed blueprint |
| PB-048 | Bound a Sequential Convex Trust-Region Step | 2014-trajopt | Needs reviewed blueprint |
| PB-054 | Build a Gaussian-Process Smoothness Factor | 2017-gaussian-process-motion-planning | Needs reviewed blueprint |
| PB-055 | Build a Joint-Space Smoothness Cost | 2014-trajopt | Needs reviewed blueprint |
| PB-078 | Check Endpoint and Smoothness Constraints | 2023-motion-planning-diffusion | Needs reviewed blueprint |
| PB-080 | Choose a Collision-Free Minimum-Cost Tree Parent | 2010-rrt-star | Needs reviewed blueprint |
| PB-082 | Clamp Goal Conditions During Denoising | 2022-diffuser | Needs reviewed blueprint |
| PB-083 | Cluster Diverse IK Solutions | 2021-ikflow | Needs reviewed blueprint |
| PB-090 | Combine Competing Task-Space Accelerations | 2018-rmpflow | Needs reviewed blueprint |
| PB-102 | Compare Path Cost Across Sampling Budgets | 2010-rrt-star | Needs reviewed blueprint |
| PB-112 | Compute a Conditional Flow Log-Likelihood | 2021-ikflow | Needs reviewed blueprint |
| PB-122 | Compute a Signed-Distance Collision Cost | 2023-curobo | Needs reviewed blueprint |
| PB-151 | Construct a State-Action Trajectory Tensor | 2022-diffuser | Needs reviewed blueprint |
| PB-183 | Encode a Target Pose for Conditional IK | 2021-ikflow | Needs reviewed blueprint |
| PB-186 | Encode Obstacles into a Fixed Feature | 2018-motion-planning-networks | Needs reviewed blueprint |
| PB-190 | Enumerate Valid Joint-Angle Branches | 2022-ik-geo | Needs reviewed blueprint |
| PB-195 | Evaluate a Batch of Trajectories with a Black-Box Cost | 2024-diffusion-es | Needs reviewed blueprint |
| PB-198 | Evaluate a Generated Plan Under Dynamics | 2022-diffuser | Needs reviewed blueprint |
| PB-222 | Express Revolute Joint-Axis Geometry | 2022-ik-geo | Needs reviewed blueprint |
| PB-228 | Filter Sampled IK Configurations by Joint Limits | 2021-ikflow | Needs reviewed blueprint |
| PB-229 | Find Nearby Planning Tree Vertices | 2010-rrt-star | Needs reviewed blueprint |
| PB-250 | Integrate a Constant-Jerk Motion Segment | 2021-ruckig | Needs reviewed blueprint |
| PB-254 | Interpolate a Trajectory Between Support States | 2017-gaussian-process-motion-planning | Needs reviewed blueprint |
| PB-257 | Linearize a Signed-Distance Collision Penalty | 2014-trajopt | Needs reviewed blueprint |
| PB-273 | Measure End-Effector Pose Error | 2021-ikflow | Needs reviewed blueprint |
| PB-287 | Mutate a Trajectory with Partial Denoising | 2024-diffusion-es | Needs reviewed blueprint |
| PB-293 | Normalize Exponential Trajectory Cost Weights | 2015-path-integral-mpc | Needs reviewed blueprint |
| PB-301 | Predict and Validate an Intermediate Waypoint | 2018-motion-planning-networks | Needs reviewed blueprint |
| PB-304 | Preserve Feasible Start and Goal Conditions | 2024-diffusion-es | Needs reviewed blueprint |
| PB-313 | Pull Back a Local Motion Metric | 2018-rmpflow | Needs reviewed blueprint |
| PB-314 | Push Robot State into a Task Space | 2018-rmpflow | Needs reviewed blueprint |
| PB-320 | Rank Candidates with a Black-Box Cost | 2024-diffusion-es | Needs reviewed blueprint |
| PB-323 | Rank Multi-Seed Motion Trajectories | 2023-curobo | Needs reviewed blueprint |
| PB-335 | Repair an Infeasible Planned Segment | 2018-motion-planning-networks | Needs reviewed blueprint |
| PB-346 | Rewire a Tree Without Creating Cycles | 2010-rrt-star | Needs reviewed blueprint |
| PB-349 | Roll Out Perturbed Control Sequences | 2015-path-integral-mpc | Needs reviewed blueprint |
| PB-382 | Solve a Circle-Plane Rotation Subproblem | 2022-ik-geo | Needs reviewed blueprint |
| PB-390 | Synchronize Multi-Joint Motion Durations | 2021-ruckig | Needs reviewed blueprint |
| PB-403 | Update a Receding-Horizon Control Sequence | 2015-path-integral-mpc | Needs reviewed blueprint |
| PB-424 | Validate a Trajectory Against Derivative Limits | 2021-ruckig | Needs reviewed blueprint |
| PB-442 | Verify IK Solutions with Forward Kinematics | 2022-ik-geo | Needs reviewed blueprint |

## robot-learning-rl

| ID | Proposed exercise | Paper IDs | Status / existing contract |
|---|---|---|---|
| PB-002 | Aggregate Analytic Grasp Quality Under Pose Perturbations | 2017-dex-net-2 | Needs reviewed blueprint |
| PB-006 | Aggregate Reward-Component Diagnostics | 2023-eureka | Needs reviewed blueprint |
| PB-011 | Align Camera and Gripper Timestamps | 2024-umi | Needs reviewed blueprint |
| PB-013 | Align Instruction Embeddings with Manipulation Observations | 2021-cliport | Needs reviewed blueprint |
| PB-019 | Apply a Seeded Random-Shift Augmentation | 2020-data-regularized-q | Needs reviewed blueprint |
| PB-024 | Apply Groupwise SimNorm to Latent States | 2023-td-mpc2 | Needs reviewed blueprint |
| PB-029 | Apply Tanh Action Log-Probability Correction | 2018-soft-actor-critic | [Published bounded component](/problems/sac-tanh-logprob-correction) |
| PB-040 | Average Augmented Bellman Targets | 2020-data-regularized-q | Needs reviewed blueprint |
| PB-056 | Build a Pick Heatmap | 2020-transporter-networks | Needs reviewed blueprint |
| PB-062 | Build Advantage-Weighted Action Weights | 2021-implicit-q-learning | [Published bounded component](/problems/iql-advantage-action-weights) |
| PB-064 | Build Distributional Reward and Ensemble-Value Targets | 2023-td-mpc2 | Needs reviewed blueprint |
| PB-068 | Build IQL Critic Targets with Terminal Masks | 2021-implicit-q-learning | [Published bounded component](/problems/soft-value-bellman-target) |
| PB-069 | Build Lambda-Return Targets | 2023-dreamerv3 | Needs reviewed blueprint |
| PB-094 | Combine Temporal and Language Alignment Losses | 2022-r3m | Needs reviewed blueprint |
| PB-101 | Compare Logged and Sampled Action Values | 2020-conservative-q-learning | Needs reviewed blueprint |
| PB-104 | Compare Robustness Across Randomization Settings | 2024-dr-eureka | Needs reviewed blueprint |
| PB-109 | Compute a Balanced Latent-Model Loss | 2023-dreamerv3 | Needs reviewed blueprint |
| PB-110 | Compute a Binary Grasp-Quality Loss | 2017-dex-net-2 | Needs reviewed blueprint |
| PB-113 | Compute a Conservative Q Penalty | 2020-conservative-q-learning | Needs reviewed blueprint |
| PB-120 | Compute a Multi-View Critic Regression Loss | 2020-data-regularized-q | Needs reviewed blueprint |
| PB-125 | Compute an Entropy-Regularized Bellman Target | 2018-soft-actor-critic | [Published bounded component](/problems/soft-value-bellman-target) |
| PB-126 | Compute an Entropy-Regularized State Value | 2018-soft-actor-critic | [Published bounded component](/problems/sac-soft-state-value) |
| PB-127 | Compute an Expectile Regression Loss | 2021-implicit-q-learning | [Published bounded component](/problems/iql-expectile-regression) |
| PB-138 | Compute Language-Conditioned Pick-and-Place Cross-Entropy | 2021-cliport | Needs reviewed blueprint |
| PB-145 | Compute the Clipped Policy Surrogate | 2017-proximal-policy-optimization | [Published bounded component](/problems/ppo-clipped-policy-surrogate) |
| PB-146 | Compute Value Targets Across Episode Boundaries | 2017-proximal-policy-optimization | [Published bounded component](/problems/ppo-boundary-value-targets) |
| PB-147 | Condition a Place Map on a Language Goal | 2021-cliport | Needs reviewed blueprint |
| PB-148 | Condition an Action Denoiser on a Point Feature | 2024-3d-diffusion-policy | Needs reviewed blueprint |
| PB-158 | Construct Offline Bellman Targets with Termination Masks | 2020-conservative-q-learning | Needs reviewed blueprint |
| PB-162 | Correlate a Pick Feature Crop with a Place Map | 2020-transporter-networks | Needs reviewed blueprint |
| PB-166 | Decode a Spatial Action Distribution | 2020-transporter-networks | Needs reviewed blueprint |
| PB-167 | Decode a Voxel Action Heatmap | 2022-peract | Needs reviewed blueprint |
| PB-182 | Encode a Discrete Six-DoF Action Target | 2022-peract | Needs reviewed blueprint |
| PB-188 | Encode Symlog Two-Hot Reward Targets | 2023-dreamerv3 | Needs reviewed blueprint |
| PB-200 | Evaluate Compositional Manipulation Slices | 2021-cliport | Needs reviewed blueprint |
| PB-202 | Evaluate Frozen Features in a Small Policy | 2022-r3m | Needs reviewed blueprint |
| PB-203 | Evaluate Grasp Precision Under a Safety Threshold | 2017-dex-net-2 | Needs reviewed blueprint |
| PB-210 | Evaluate Offline Policy Support | 2020-conservative-q-learning | Needs reviewed blueprint |
| PB-213 | Evaluate Policy Robustness to Visual Shifts | 2020-data-regularized-q | Needs reviewed blueprint |
| PB-221 | Evaluate Viewpoint and Geometry Shift | 2024-3d-diffusion-policy | Needs reviewed blueprint |
| PB-223 | Extract a Grasp-Aligned Depth Patch | 2017-dex-net-2 | Needs reviewed blueprint |
| PB-236 | Fuse Semantic and Spatial Feature Streams | 2021-cliport | Needs reviewed blueprint |
| PB-238 | Gate an Online Policy Update | 2024-hil-serl | Needs reviewed blueprint |
| PB-256 | Label Human Intervention Segments | 2024-hil-serl | Needs reviewed blueprint |
| PB-269 | Measure Closed-Loop Latency and Action Dropouts | 2024-mobile-aloha | [Reused bounded component](/problems/rt1-control-latency-dropouts) |
| PB-284 | Merge Online and Demonstration Replay | 2024-serl | Needs reviewed blueprint |
| PB-285 | Mix Intervention and Autonomous Replay | 2024-hil-serl | Needs reviewed blueprint |
| PB-286 | Mix Static and Mobile Demonstration Batches | 2024-mobile-aloha | Needs reviewed blueprint |
| PB-292 | Normalize Batched Advantages | 2017-proximal-policy-optimization | [Published bounded component](/problems/ppo-normalize-batched-advantages) |
| PB-294 | Normalize Heterogeneous Robot Observation Schemas | 2024-mobile-aloha | [Reused bounded component](/problems/oxe-normalize-observation-schema) |
| PB-321 | Rank Grasp Candidates by Predicted Quality | 2017-dex-net-2 | Needs reviewed blueprint |
| PB-324 | Rank Reward Candidates by Rollout Evidence | 2023-eureka | Needs reviewed blueprint |
| PB-329 | Record Intervention and Reset Statistics | 2024-serl | Needs reviewed blueprint |
| PB-340 | Report Policy Update Clip Fractions | 2017-proximal-policy-optimization | [Published bounded component](/problems/ppo-policy-update-clip-fractions) |
| PB-347 | Roll Out a Latent Dynamics Sequence | 2023-td-mpc2 | Needs reviewed blueprint |
| PB-348 | Roll Out Imagined Latent Trajectories | 2023-dreamerv3 | Needs reviewed blueprint |
| PB-353 | Sample a Bounded Dynamics Randomization Config | 2024-dr-eureka | Needs reviewed blueprint |
| PB-355 | Sample and Normalize Scene Points | 2024-3d-diffusion-policy | Needs reviewed blueprint |
| PB-364 | Sample Time-Contrastive Video Triplets | 2022-r3m | Needs reviewed blueprint |
| PB-365 | Schedule Actor-Learner Updates | 2024-serl | Needs reviewed blueprint |
| PB-369 | Score Candidate Action Trajectories | 2023-td-mpc2 | Needs reviewed blueprint |
| PB-400 | Transform Demonstrations into a Shared Tool Frame | 2024-umi | Needs reviewed blueprint |
| PB-404 | Update a Sampling-Based Planner | 2023-td-mpc2 | Needs reviewed blueprint |
| PB-405 | Update a Temperature Objective (later SAC extension) | 2018-soft-actor-critic | [Published bounded component](/problems/sac-temperature-objective-update) |
| PB-409 | Validate a Demonstration Replay Bundle | 2024-umi | Needs reviewed blueprint |
| PB-411 | Validate a Generated Reward Program | 2024-dr-eureka | Needs reviewed blueprint |
| PB-417 | Validate a Reward Function Contract | 2023-eureka | Needs reviewed blueprint |
| PB-428 | Validate an Offline Dataset Split | 2021-implicit-q-learning | [Published bounded component](/problems/iql-offline-dataset-split) |
| PB-437 | Validate Success-Classifier Rewards on Robot Failures | 2024-serl | Needs reviewed blueprint |
| PB-446 | Voxelize a Calibrated RGB-D Scene | 2022-peract | Needs reviewed blueprint |

## simulation-sim2real

| ID | Proposed exercise | Paper IDs | Status / existing contract |
|---|---|---|---|
| PB-007 | Aggregate Seeded Benchmark Returns | 2018-deepmind-control-suite | Needs reviewed blueprint |
| PB-046 | Batch Independent Simulator States | 2021-isaac-gym | Needs reviewed blueprint |
| PB-057 | Build a Reproducible Interaction Scenario | 2020-sapien | Needs reviewed blueprint |
| PB-059 | Build a Task-Variation Sampler | 2019-rlbench | Needs reviewed blueprint |
| PB-060 | Build a Vectorized Manipulation Batch | 2023-maniskill-2 | Needs reviewed blueprint |
| PB-079 | Check Gradient Consistency for a Small Dynamics Model | 2021-brax | Needs reviewed blueprint |
| PB-136 | Compute Joint PD Control Effort | 2020-robosuite | Needs reviewed blueprint |
| PB-137 | Compute Joint-Conditioned Object State | 2020-sapien | Needs reviewed blueprint |
| PB-144 | Compute Success and SPL | 2019-habitat | Needs reviewed blueprint |
| PB-150 | Construct a Rearrangement Goal Graph | 2021-habitat-2 | Needs reviewed blueprint |
| PB-175 | Detect an Invalid Interaction Transition | 2017-ai2thor | Needs reviewed blueprint |
| PB-196 | Evaluate a Bounded Continuous-Control Reward | 2018-deepmind-control-suite | Needs reviewed blueprint |
| PB-197 | Evaluate a Cooperative Interaction Episode | 2023-habitat-3 | Needs reviewed blueprint |
| PB-217 | Evaluate Skill Success Across Object Instances | 2021-maniskill | Needs reviewed blueprint |
| PB-244 | Implement a Functional Physics Step Contract | 2021-brax | Needs reviewed blueprint |
| PB-245 | Implement Action Repeat Correctly | 2018-deepmind-control-suite | Needs reviewed blueprint |
| PB-272 | Measure Domain Shift Between Simulated Scenes | 2020-igibson | Needs reviewed blueprint |
| PB-275 | Measure Human-Robot Proximity Events | 2023-habitat-3 | Needs reviewed blueprint |
| PB-280 | Measure Simulation and Learning Throughput | 2021-isaac-gym | Needs reviewed blueprint |
| PB-289 | Normalize a Simulation Observation Dictionary | 2020-robosuite | Needs reviewed blueprint |
| PB-290 | Normalize Action Bounds Across Tasks | 2021-maniskill | Needs reviewed blueprint |
| PB-328 | Record a Deterministic Rollout Manifest | 2020-robosuite | Needs reviewed blueprint |
| PB-336 | Replay a Seeded Navigation Trajectory | 2019-habitat | Needs reviewed blueprint |
| PB-337 | Replay Sensor Streams from a Fixed Seed | 2020-igibson | Needs reviewed blueprint |
| PB-339 | Report Generalization by Object Split | 2023-maniskill-2 | Needs reviewed blueprint |
| PB-342 | Reset Completed Environments Selectively | 2021-isaac-gym | Needs reviewed blueprint |
| PB-371 | Score Multi-Stage Task Completion | 2019-rlbench | Needs reviewed blueprint |
| PB-385 | Stratify Manipulation Object Instances | 2021-maniskill | Needs reviewed blueprint |
| PB-389 | Synchronize Human and Robot Agent States | 2023-habitat-3 | Needs reviewed blueprint |
| PB-395 | Track Object-State Preconditions | 2017-ai2thor | Needs reviewed blueprint |
| PB-408 | Validate a Continuous-Control Time Step | 2018-deepmind-control-suite | Needs reviewed blueprint |
| PB-415 | Validate a Navigation Episode | 2019-habitat | Needs reviewed blueprint |
| PB-419 | Validate a Robot-Controller-Task Configuration | 2020-robosuite, 2023-maniskill-2 | Needs reviewed blueprint |
| PB-420 | Validate a Scene Interaction Graph | 2020-igibson | Needs reviewed blueprint |
| PB-421 | Validate a Simulator Action Grammar | 2017-ai2thor | Needs reviewed blueprint |
| PB-427 | Validate an Articulated Object Schema | 2020-sapien | Needs reviewed blueprint |
| PB-429 | Validate Demonstration Waypoints | 2019-rlbench | Needs reviewed blueprint |
| PB-433 | Validate Manipulation Task Observations | 2021-maniskill | Needs reviewed blueprint |
| PB-435 | Validate Object Reset States | 2021-habitat-2 | Needs reviewed blueprint |
| PB-436 | Validate Skill Preconditions in a Rearrangement Plan | 2021-habitat-2 | Needs reviewed blueprint |
| PB-439 | Validate Task-Specific Success Predicates | 2023-maniskill-2 | Needs reviewed blueprint |
| PB-441 | Vectorize Environment Resets | 2021-brax | Needs reviewed blueprint |

## vision-vlm-3d

| ID | Proposed exercise | Paper IDs | Status / existing contract |
|---|---|---|---|
| PB-170 | Decode Normalized Boxes and Classes from Object Queries | 2020-detr | Needs reviewed blueprint |
| PB-181 | Differentiate Rendered Color on a Small Synthetic Field | 2020-nerf | Needs reviewed blueprint |
| PB-205 | Evaluate Localization and Phrase Grounding Separately | 2023-grounding-dino | Needs reviewed blueprint |
| PB-231 | Flatten Spatial Features with Position and Padding Metadata | 2020-detr | Needs reviewed blueprint |
| PB-234 | Fuse Masked Image and Text Tokens with Bidirectional Cross-Attention | 2023-grounding-dino | Needs reviewed blueprint |
| PB-248 | Implement Nearest-Neighbor Feature-Spreading Regularization | 2023-dinov2 | Needs reviewed blueprint |
| PB-325 | Read a Normalized Class Token with a Linear Head | 2021-vision-transformer | Needs reviewed blueprint |
| PB-345 | Reuse Image Embeddings Without Stale-Cache Errors | 2023-segment-anything | Needs reviewed blueprint |
| PB-357 | Sample Calibrated Multi-Camera Feature Maps | 2022-bevformer | Needs reviewed blueprint |
| PB-360 | Sample Hierarchical Depth Intervals | 2020-nerf | Needs reviewed blueprint |
| PB-401 | Transform Prompt Coordinates Through Image Preprocessing | 2023-segment-anything | Needs reviewed blueprint |

## vla-embodied

| ID | Proposed exercise | Paper IDs | Status / existing contract |
|---|---|---|---|
| PB-050 | Build a Conditional Action Denoiser | 2023-diffusion-policy | Needs reviewed blueprint |
| PB-189 | Encode Synchronized Observations for an Action Denoiser | 2023-diffusion-policy | Needs reviewed blueprint |

## vla-generalist

| ID | Proposed exercise | Paper IDs | Status / existing contract |
|---|---|---|---|
| PB-014 | Align Language Corrections with Action Windows | 2024-rt-h | Needs reviewed blueprint |
| PB-042 | Balance Robot-Task Training Mixtures | 2023-robocat | Needs reviewed blueprint |
| PB-058 | Build a Small Action Decoder | 2024-tinyvla | Needs reviewed blueprint |
| PB-071 | Build Object-Centric Prompt Tokens | 2022-vima | Needs reviewed blueprint |
| PB-076 | Build Task-Aware Sequence Masks | 2022-gato | Needs reviewed blueprint |
| PB-084 | Collate Heterogeneous Embodied Training Examples | 2025-pi0-5 | Needs reviewed blueprint |
| PB-085 | Collate Interleaved Multimodal Prompts | 2022-vima | Needs reviewed blueprint |
| PB-093 | Combine Skill Likelihood and Feasibility Scores | 2022-saycan | Needs reviewed blueprint |
| PB-103 | Compare Policy Latency Under Serving Settings | 2025-openvla-oft | Needs reviewed blueprint |
| PB-149 | Construct a Compact Policy Flow-Matching Target | 2025-smolvla | Needs reviewed blueprint |
| PB-155 | Construct Goal-Conditioned Policy Batches | 2023-robocat | Needs reviewed blueprint |
| PB-159 | Construct Parallel Action-Chunk Targets | 2025-openvla-oft | Needs reviewed blueprint |
| PB-168 | Decode Actions from a Shared Token Space | 2022-gato | Needs reviewed blueprint |
| PB-172 | Decode Structured Manipulation Actions | 2022-vima | Needs reviewed blueprint |
| PB-193 | Estimate End-to-End Policy Memory | 2024-tinyvla | Needs reviewed blueprint |
| PB-218 | Evaluate Subtask and Action Errors Separately | 2024-rt-h | Needs reviewed blueprint |
| PB-270 | Measure Codec Rate-Distortion Tradeoffs | 2025-fast-action-tokenization | Needs reviewed blueprint |
| PB-274 | Measure Fine-Tuning Throughput | 2025-openvla-oft | Needs reviewed blueprint |
| PB-281 | Measure Stale-Action Latency | 2025-smolvla | Needs reviewed blueprint |
| PB-288 | Normalize a Compact VLA Observation Batch | 2025-smolvla | Needs reviewed blueprint |
| PB-307 | Project Compact Visual-Language Features | 2024-tinyvla | Needs reviewed blueprint |
| PB-315 | Quantize Compressed Action Coefficients | 2025-fast-action-tokenization | Needs reviewed blueprint |
| PB-322 | Rank Grounded Skill Candidates | 2022-saycan | Needs reviewed blueprint |
| PB-338 | Report Generalization Across Novel Environments | 2025-pi0-5 | Needs reviewed blueprint |
| PB-344 | Resolve Perception Results into Control Calls | 2022-code-as-policies | Needs reviewed blueprint |
| PB-350 | Route High-Level and Low-Level Supervision | 2025-pi0-5 | Needs reviewed blueprint |
| PB-351 | Route High-Level Tasks into Language Subtasks | 2024-rt-h | Needs reviewed blueprint |
| PB-366 | Schedule Asynchronous Policy Chunks | 2025-smolvla | Needs reviewed blueprint |
| PB-373 | Score Task Relevance for Available Robot Skills | 2022-saycan | Needs reviewed blueprint |
| PB-384 | Stop a Skill Sequence at Completion | 2022-saycan | Needs reviewed blueprint |
| PB-391 | Tokenize Mixed Observation Modalities | 2022-gato | Needs reviewed blueprint |
| PB-392 | Trace a Composed Robot Policy | 2022-code-as-policies | Needs reviewed blueprint |
| PB-393 | Track Adaptation Data Lineage | 2023-robocat | Needs reviewed blueprint |
| PB-398 | Transform an Action Chunk into Frequency Coefficients | 2025-fast-action-tokenization | Needs reviewed blueprint |
| PB-416 | Validate a Restricted Robot Program AST | 2022-code-as-policies | Needs reviewed blueprint |

## vlm-grounding

| ID | Proposed exercise | Paper IDs | Status / existing contract |
|---|---|---|---|
| PB-008 | Aggregate Token Scores into Region Scores | 2021-glip | Needs reviewed blueprint |
| PB-022 | Apply Bidirectional Region-Token Feature Fusion | 2021-glip | Needs reviewed blueprint |
| PB-038 | Attach Text-Scoring and Box Heads to Spatial Vision Tokens | 2022-owl-vit | Needs reviewed blueprint |
| PB-049 | Build a Bidirectional-Prefix Causal-Suffix Attention Mask | 2024-paligemma | Needs reviewed blueprint |
| PB-067 | Build Image-Text Matching Pairs | 2022-blip | Needs reviewed blueprint |
| PB-072 | Build Phrase-to-Token Positive Maps | 2021-glip | Needs reviewed blueprint |
| PB-073 | Build Positive-Negative Pair Masks | 2023-siglip | Needs reviewed blueprint |
| PB-075 | Build Query-to-Image Attention Masks | 2023-blip-2 | Needs reviewed blueprint |
| PB-077 | Build Text-Conditioned Detection Scores | 2022-owl-vit | Needs reviewed blueprint |
| PB-086 | Collate Multilingual Image-Text Batches | 2022-pali | Needs reviewed blueprint |
| PB-087 | Collate Variable Image-Text Conversations | 2023-llava | Needs reviewed blueprint |
| PB-089 | Combine Alignment and Caption Losses | 2022-blip | Needs reviewed blueprint |
| PB-097 | Compare Batch-Size Sensitivity | 2023-siglip | Needs reviewed blueprint |
| PB-107 | Compare Transfer Metrics Across Tasks | 2023-pali-3 | Needs reviewed blueprint |
| PB-124 | Compute an Assistant-Only Visual-Instruction Loss | 2023-llava | Needs reviewed blueprint |
| PB-140 | Compute Pairwise Sigmoid Alignment Loss | 2023-pali-3, 2023-siglip | Needs reviewed blueprint |
| PB-143 | Compute Retrieval Recall by Slice | 2021-align | Needs reviewed blueprint |
| PB-154 | Construct Contrastive Pair Labels | 2021-align | Needs reviewed blueprint |
| PB-163 | Count Trainable and Frozen Parameters | 2023-blip-2 | Needs reviewed blueprint |
| PB-173 | Deduplicate Image-Text Training Pairs | 2021-align | Needs reviewed blueprint |
| PB-185 | Encode Grounding Locations as Tokens | 2023-kosmos-2 | Needs reviewed blueprint |
| PB-187 | Encode Spatial Locations as Tokens | 2024-paligemma | Needs reviewed blueprint |
| PB-208 | Evaluate Metrics by Language and Task | 2022-pali | Needs reviewed blueprint |
| PB-211 | Evaluate Phrase Grounding Recall | 2021-glip | Needs reviewed blueprint |
| PB-216 | Evaluate Seen and Unseen Class Slices | 2022-owl-vit | Needs reviewed blueprint |
| PB-226 | Filter Noisy Captions by Agreement | 2022-blip | Needs reviewed blueprint |
| PB-232 | Format Image-Prefix Language Sequences | 2024-paligemma | Needs reviewed blueprint |
| PB-237 | Gate a Multimodal Residual Update | 2022-flamingo | Needs reviewed blueprint |
| PB-262 | Map Text Spans to Image Boxes | 2023-kosmos-2 | Needs reviewed blueprint |
| PB-264 | Mask Cross-Attention by Image Position | 2022-flamingo | Needs reviewed blueprint |
| PB-266 | Mask Task-Specific Output Tokens | 2022-pali | Needs reviewed blueprint |
| PB-267 | Mask Visual-Instruction Training Labels | 2023-llava | Needs reviewed blueprint |
| PB-296 | Normalize Spatial Coordinates into Tokens | 2023-florence-2 | Needs reviewed blueprint |
| PB-298 | Parse Structured Detection Tokens | 2023-florence-2 | Needs reviewed blueprint |
| PB-309 | Project Query Features into Language Tokens | 2023-blip-2 | Needs reviewed blueprint |
| PB-310 | Project Visual Tokens into Language Width | 2023-llava | Needs reviewed blueprint |
| PB-341 | Resample Variable Visual Features | 2022-flamingo | Needs reviewed blueprint |
| PB-352 | Route Task Prompts to Output Schemas | 2023-florence-2 | Needs reviewed blueprint |
| PB-367 | Schedule Multi-Task Data Mixtures | 2023-pali-3 | Needs reviewed blueprint |
| PB-375 | Select Boxes for a Query Phrase | 2022-owl-vit | Needs reviewed blueprint |
| PB-430 | Validate Grounded Sequence Syntax | 2023-kosmos-2 | Needs reviewed blueprint |
| PB-438 | Validate Task-Specific Output Grammars | 2024-paligemma | Needs reviewed blueprint |
| PB-440 | Validate Vision-Language Feature Shapes | 2023-pali-3 | Needs reviewed blueprint |
