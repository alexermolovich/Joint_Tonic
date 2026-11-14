## Example 1

initial=[[1]], predicted_noise=[[[0]]], betas=[0.04], step_noise=[[[99]]] gives trace [[[1]],[[1/sqrt(0.96)]]]. Final noise is ignored even though nonzero.

## Example 2

initial=[[0]], predicted_noise=zeros((2,1,1)), betas=[0.04,0.04], step_noise=[[[0]],[[1]]] gives states 0, sqrt(0.04*0.04/0.0784), then that value/sqrt(0.96). Noise enters only at reverse index1.
