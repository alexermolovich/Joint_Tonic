# Train and Evaluate a Tiny PPO Joint Controller

A policy loss is only one part of reinforcement learning. This project closes a small loop: collect actions under one frozen behavior policy, estimate their advantage, update the controller, and measure what changed on independent target positions.

## Contract

`train_joint_controller(initial_theta, train_goals, noise, eval_goals, epochs, learning_rate, epsilon)` receives theta real(2,) with gain in[0,2] and bias in[-.5,.5]; goals real(B,),1<=B<=32, absolute value<=1; supplied Gaussian-standardized noise real(I,B,T),1<=I<=8,1<=T<=16, absolute value<=3; evaluation goals real(M,),1<=M<=32, absolute value<=1. epochs is a non-bool integer1..4, learning_rate scalar[0,.01], epsilon scalar[.05,.4]. All other numeric arrays finite real CPU, no boolean/complex inputs; malformed input raises ValueError. Arrays are preserved and output arrays independent float64.

Each iteration collects fresh fixed-horizon episodes from q=0 with the current policy. At step t, feature x=[goal-q,1], Gaussian mean mu=x@theta, action a=mu+0.2*noise, q_next=q+0.1*a, reward=-(q_next-goal)^2-0.01*a^2. Record x,a and the behavior log density -0.5*((a-mu)/.2)^2-log(.2*sqrt(2*pi)). This is an unconstrained synthetic scalar integrator, not MuJoCo or real hardware. The finite horizon is a true task terminal.

Compute discounted returns backward with gamma=.95 and terminal bootstrap0. With zero value baseline, advantages are those returns, globally normalized over B*T by sqrt(population variance+1e-8). Hold actions, advantages and behavior likelihoods fixed during each of the specified PPO epochs.

For current theta, recompute Gaussian log densities and ratios exp(log_new-log_old). Maximize mean(min(ratio*A,clip(ratio,1-epsilon,1+epsilon)*A)). Active derivative uses the raw branch except when A>0 and ratio>1+epsilon, or A<0 and ratio<1-epsilon; equality uses the raw branch, A=0 contributes zero. The gradient is mean(active*ratio*A*(a-mu)/.2^2*x). Clip its global L2 norm to at most1, take theta += learning_rate*gradient, then project gain to[0,2] and bias to[-.5,.5]. No extra optimizer, critic, entropy bonus or randomness.

After each iteration, evaluate the new theta with deterministic mean actions (no noise), same T-step dynamics and independent q=0 on eval_goals. Return dict theta_history:float64(I+1,2), training_return:float64(I,) mean UNDISCOUNTED reward sum from that iteration's collected episodes, evaluation_final_error:float64(I,M) absolute final goal error, evaluation_return:float64(I,) mean UNDISCOUNTED evaluation reward sum, clip_fraction:float64(I,epochs) valid fraction of ratios strictly outside clip bounds BEFORE each epoch update.



Unless a tighter bound is stated below, numeric array-like inputs must have real integer/floating dtype after `np.asarray`, be finite with absolute values <=1e6 and at most1,000,000 entries. Boolean, complex, string and object numeric arrays are invalid; Boolean masks must have Boolean dtype. Integer arrays/scalars exclude booleans. All invalid inputs raise ValueError. Return new arrays, preserve inputs, and compute floating outputs in float64 on CPU. No automatic differentiation is required.

## Physical context and scope

Normalized joint position q; normalized velocity action units per second; dt=0.1 seconds; Gaussian action standard deviation0.2 normalized velocity units. Fixed-step synthetic episodes reset q=0 each training iteration and held-out evaluation. The T-step horizon is a true terminal. Original executable PPO training loop for a scalar integrator and linear Gaussian controller. It omits neural perception, a critic network, entropy bonus, MuJoCo and real hardware; it is not a VLA or a reproduction of published locomotion scores.


## Example 1

theta=[0,0], train_goals=[1], noise=zeros((1,1,1)), eval_goals=[1], epochs1, learning_rate.01, epsilon.2: the single return normalizes to zero, so theta_history=[[0,0],[0,0]], training_return=[-1], evaluation_final_error=[[1]], evaluation_return=[-1], clip_fraction=[[0]].

## Example 2

theta=[0,0], train_goals=[1,1], noise=[[[1],[-1]]], eval_goals=[0], epochs1, learning_rate0, epsilon.2: actions[.2,-.2] give rewards[-.9608,-1.0408], training_return[-1.0008]. No update occurs; held-out goal0 has final error0 and return0.
