## Example 1

Both categorical logits [0,0], one group, prediction_loss 2, valid True -> K=0, loss=3.1, both logit gradients 0,prediction_gradient 1.

## Example 2

Same inputs with valid False -> loss 0, kl NaN,all gradients 0. With two valid identical rows predictions [2,4],loss 4.1 and prediction_gradient [.5,.5].
