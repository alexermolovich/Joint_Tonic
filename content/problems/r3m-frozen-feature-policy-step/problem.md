# Evaluate Frozen Features in a Small Policy

A frozen encoder can still support learning a new robot controller. Update only a small policy head, then evaluate it on rows that did not contribute gradients.

## Contract

Features real(N,D), robot_state real(N,P), actions real(N,A), 1<=N<=4096,1<=D<=64,0<=P<=32,1<=A<=16; all finite abs<=10, actions normalized in[-1,1]. Train/evaluate bool(N,), disjoint, at least one train row; evaluation may be empty. Weight real(D+P,A), bias real(A,), abs<=10; learning_rate scalar[0,1]. All input features/state are already normalized dimensionless coordinates; action channels use the supplied normalized controller convention. Concatenate X=[features,state]. Initial predictions XW+b. Training loss mean squared error over train rows AND action channels. Gradient dW=2 Xtrain.T residual/(ntrain*A), db=2 sum(residual)/(ntrain*A). Compute simultaneous one-step SGD W'=W-lr*dW,b'=b-lr*db. Frozen features and all input arrays remain untouched. Return dict weight,bias,predictions (all N rows after update), train_loss_before,train_loss_after,evaluation_loss (same mean squared error on evaluation rows, NaN if none). Evaluation actions never affect the update. This is a single affine policy step on supplied frozen embeddings; the paper uses a BatchNorm-plus-MLP behavior-cloning policy and online success evaluation, neither reproduced here. No claim that action MSE equals task success.

Unless a tighter bound is stated below, numeric array-like inputs must have real integer/floating dtype after `np.asarray`, be finite with absolute values <=1e6 and at most 1,000,000 entries. Boolean, complex, string and object numeric arrays are invalid; Boolean masks must have Boolean dtype. Integer arrays/scalars exclude booleans. All invalid inputs raise ValueError. Return new arrays, preserve inputs, and compute floating outputs in float64 on CPU. No automatic differentiation is required.

## Physical context and scope

Embedding coordinates, supplied logits, normalized robot state and normalized actions are dimensionless. Frame indices are ordinal positions, not timestamps in seconds. Triplets stay in one video and the negative comes from another. Policy rows are supplied observations with explicit training/evaluation membership; no temporal transitions are inferred. Original bounded R3M component. The sampler is an explicit sequential recorded-draw recipe, the loss pins valid-row mean reduction and anchor regularization, and the policy uses an affine head rather than the paper's BatchNorm/MLP. No pretrained model or benchmark reproduction claim.

## Example 1

features [[1],[2]], state empty(2,0), actions [[1],[0]], train [True,False], evaluate [False,True], weight [[0]], bias [0], lr0.1 -> weight[[0.2]], bias[0.2], predictions[[0.4],[0.6]], losses before1, train-after0.36, evaluation0.36.

## Example 2

same data with lr0 and evaluate allFalse -> unchanged parameters, all predictions0, train losses1, evaluationNaN.
