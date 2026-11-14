# Aggregate Multi-Camera Features with Attention Weights

Implement aggregate_camera_features(features, weights, valid). features and weights are finite NumPy float64, shapes(B,Q,C,S,D) and(B,Q,C,S); valid is NumPy bool same shape as weights. 1<=B,Q,C,S,D<=128; features at most1,000,000 elements; abs feature values<=1e6; weights in[0,1e6]. Set invalid contribution weights to zero, sum remaining weights over camera and sample axes, and return their weighted mean feature per (B,Q). Where total valid weight is zero return an all-zero feature and observed=False; otherwise observed=True. Return new float64 output(B,Q,D) and bool observed(B,Q); preserve inputs and support noncontiguous arrays. Validate all feature/weight entries including invalid slots. TypeError for non-arrays; ValueError for other violations. Features are dimensionless and already sampled at projections of one ego-frame BEV query from synchronized calibrated images; camera index is not a spatial axis. This is an explicitly simplified global weighted reduction, not BEVFormer's full per-camera/head deformable-attention normalization, learned offsets, bilinear sampling, or temporal fusion.

## Worked examples

## Ignore an invalid camera sample

B=Q=1,C=2,S=1,D=2; features=[[[[[2,4]],[[10,20]]]]], weights=[[[[1],[3]]]], valid=[[[[True],[False]]]]. Return output=[[[2,4]]], observed=[[True]]. Invalid weight3 contributes neither numerator nor denominator.

## Fuse two available views

Use the same features/weights but both valid. Return output=[[[8,16]]], observed=[[True]]. (1*[2,4]+3*[10,20])/4=[8,16]. With both weights zero return [[[0,0]]] and [[False]].
