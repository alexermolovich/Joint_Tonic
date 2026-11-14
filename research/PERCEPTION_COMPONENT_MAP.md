# Perception and geometry paper component mapping

Scope: 50 existing paper cards across vision-vlm-3d, perception-3d, vlm-grounding, and geometry-calibration-slam. Newly collected curator cards are mapped by their author and audited separately.

The mapping covers 150 execution stages, 41 runnable component links, and 182 planned-component placements. Sixteen existing links were moved out of stage completion into explicit prerequisite prose because they were supporting skills rather than that stage’s implementation. The ten main perception-paper cards use exact curriculum titles where available. Other titles retain their original idea names; a gap pass added 30 precise unreviewed ideas so every explained stage has an implementation association. All ideas without reviewed blueprints remain explicitly unreviewed.

## Verification

- Each runnable slug resolves to an existing published problem and appears in its corresponding explanation section.
- Each planned title appears at its mapped stage and in the paper’s planned component list; no runnable URL was invented for an idea.
- All 468 inline/display math expressions across these 50 cards passed strict KaTeX parsing.
- Manual mechanism placement distinguishes paired alignment from grounding, pinhole geometry from complete SLAM, and reusable compositing from a trained neural map.
- This audit validates linkage and syntax, not a claim that all planned problems are implemented or every paper has been fully reproduced.

| Paper card | Stages | Runnable component links | Planned placements |
|---|---:|---:|---:|
| [2016-yolo-v1](papers/vision-vlm-3d/2016-yolo-v1.md) | 3 | 3 | 4 |
| [2017-pointnet](papers/vision-vlm-3d/2017-pointnet.md) | 3 | 3 | 2 |
| [2020-detr](papers/vision-vlm-3d/2020-detr.md) | 3 | 3 | 4 |
| [2020-nerf](papers/vision-vlm-3d/2020-nerf.md) | 3 | 4 | 4 |
| [2021-clip](papers/vision-vlm-3d/2021-clip.md) | 3 | 4 | 1 |
| [2021-vision-transformer](papers/vision-vlm-3d/2021-vision-transformer.md) | 3 | 3 | 3 |
| [2022-bevformer](papers/vision-vlm-3d/2022-bevformer.md) | 3 | 4 | 5 |
| [2023-dinov2](papers/vision-vlm-3d/2023-dinov2.md) | 3 | 4 | 2 |
| [2023-grounding-dino](papers/vision-vlm-3d/2023-grounding-dino.md) | 3 | 0 | 6 |
| [2023-segment-anything](papers/vision-vlm-3d/2023-segment-anything.md) | 3 | 2 | 5 |
| [2015-faster-r-cnn](papers/perception-3d/2015-faster-r-cnn.md) | 3 | 2 | 4 |
| [2015-ssd](papers/perception-3d/2015-ssd.md) | 3 | 2 | 3 |
| [2016-feature-pyramid-networks](papers/perception-3d/2016-feature-pyramid-networks.md) | 3 | 0 | 4 |
| [2017-focal-loss-retinanet](papers/perception-3d/2017-focal-loss-retinanet.md) | 3 | 0 | 4 |
| [2017-mask-r-cnn](papers/perception-3d/2017-mask-r-cnn.md) | 3 | 0 | 4 |
| [2017-pointnet-plus-plus](papers/perception-3d/2017-pointnet-plus-plus.md) | 3 | 0 | 3 |
| [2018-yolov3](papers/perception-3d/2018-yolov3.md) | 3 | 2 | 3 |
| [2020-raft](papers/perception-3d/2020-raft.md) | 3 | 0 | 3 |
| [2021-dense-prediction-transformers](papers/perception-3d/2021-dense-prediction-transformers.md) | 3 | 0 | 4 |
| [2023-3d-gaussian-splatting](papers/perception-3d/2023-3d-gaussian-splatting.md) | 3 | 0 | 4 |
| [2024-depth-anything-v2](papers/perception-3d/2024-depth-anything-v2.md) | 3 | 0 | 4 |
| [2024-sam-2](papers/perception-3d/2024-sam-2.md) | 3 | 0 | 4 |
| [2021-align](papers/vlm-grounding/2021-align.md) | 3 | 3 | 3 |
| [2021-glip](papers/vlm-grounding/2021-glip.md) | 3 | 0 | 4 |
| [2022-blip](papers/vlm-grounding/2022-blip.md) | 3 | 1 | 3 |
| [2022-flamingo](papers/vlm-grounding/2022-flamingo.md) | 3 | 0 | 3 |
| [2022-owl-vit](papers/vlm-grounding/2022-owl-vit.md) | 3 | 0 | 4 |
| [2022-pali](papers/vlm-grounding/2022-pali.md) | 3 | 0 | 3 |
| [2023-blip-2](papers/vlm-grounding/2023-blip-2.md) | 3 | 0 | 3 |
| [2023-florence-2](papers/vlm-grounding/2023-florence-2.md) | 3 | 0 | 3 |
| [2023-kosmos-2](papers/vlm-grounding/2023-kosmos-2.md) | 3 | 0 | 3 |
| [2023-llava](papers/vlm-grounding/2023-llava.md) | 3 | 0 | 4 |
| [2023-pali-3](papers/vlm-grounding/2023-pali-3.md) | 3 | 0 | 4 |
| [2023-siglip](papers/vlm-grounding/2023-siglip.md) | 3 | 0 | 3 |
| [2024-paligemma](papers/vlm-grounding/2024-paligemma.md) | 3 | 0 | 4 |
| [2015-on-manifold-preintegration](papers/geometry-calibration-slam/2015-on-manifold-preintegration.md) | 3 | 0 | 4 |
| [2016-bundlefusion](papers/geometry-calibration-slam/2016-bundlefusion.md) | 3 | 0 | 4 |
| [2016-direct-sparse-odometry](papers/geometry-calibration-slam/2016-direct-sparse-odometry.md) | 3 | 0 | 3 |
| [2016-orb-slam-2](papers/geometry-calibration-slam/2016-orb-slam-2.md) | 3 | 0 | 3 |
| [2017-superpoint](papers/geometry-calibration-slam/2017-superpoint.md) | 3 | 0 | 4 |
| [2017-vins-mono](papers/geometry-calibration-slam/2017-vins-mono.md) | 3 | 0 | 4 |
| [2019-superglue](papers/geometry-calibration-slam/2019-superglue.md) | 3 | 0 | 4 |
| [2019-vins-fusion](papers/geometry-calibration-slam/2019-vins-fusion.md) | 3 | 0 | 4 |
| [2020-lio-sam](papers/geometry-calibration-slam/2020-lio-sam.md) | 3 | 0 | 4 |
| [2020-orb-slam-3](papers/geometry-calibration-slam/2020-orb-slam-3.md) | 3 | 0 | 4 |
| [2021-droid-slam](papers/geometry-calibration-slam/2021-droid-slam.md) | 3 | 0 | 4 |
| [2021-fast-lio-2](papers/geometry-calibration-slam/2021-fast-lio-2.md) | 3 | 0 | 4 |
| [2021-imap](papers/geometry-calibration-slam/2021-imap.md) | 3 | 1 | 4 |
| [2021-loftr](papers/geometry-calibration-slam/2021-loftr.md) | 3 | 0 | 4 |
| [2021-nice-slam](papers/geometry-calibration-slam/2021-nice-slam.md) | 3 | 0 | 4 |
