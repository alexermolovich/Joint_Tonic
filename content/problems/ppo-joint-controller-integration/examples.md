## Example 1

theta=[0,0], train_goals=[1], noise=zeros((1,1,1)), eval_goals=[1], epochs1, learning_rate.01, epsilon.2: the single return normalizes to zero, so theta_history=[[0,0],[0,0]], training_return=[-1], evaluation_final_error=[[1]], evaluation_return=[-1], clip_fraction=[[0]].

## Example 2

theta=[0,0], train_goals=[1,1], noise=[[[1],[-1]]], eval_goals=[0], epochs1, learning_rate0, epsilon.2: actions[.2,-.2] give rewards[-.9608,-1.0408], training_return[-1.0008]. No update occurs; held-out goal0 has final error0 and return0.
