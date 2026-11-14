# Train and Evaluate a Tiny PPO Joint Controller

## Intuition

A policy loss is only one part of reinforcement learning. This project closes a small loop: collect actions under one frozen behavior policy, estimate their advantage, update the controller, and measure what changed on independent target positions.

## Mathematical mechanism

The state is normalized joint position q and target g. Feature $x_t=[g-q_t,1]$ has width2; policy parameters $\theta=[k,b]$ are a gain and bias. With supplied standardized noise z and fixed sigma0.2,

$$\mu_t=x_t^T\theta,\quad a_t=\mu_t+\sigma z_t,\quad q_{t+1}=q_t+0.1a_t,\quad r_t=-(q_{t+1}-g)^2-0.01a_t^2.$$

At the T-step terminal use zero bootstrap and discounted returns $R_t=r_t+0.95R_{t+1}$. Normalize these returns over all B*T collected transitions, using population variance plus1e-8, to obtain fixed advantages A. The zero baseline and normalization are explicit teaching choices.

For one PPO epoch, behavior log density stays frozen while the current Gaussian mean changes. Its score derivative is

$$\nabla_\theta\log\pi_\theta(a\mid x)=\frac{a-x^T\theta}{\sigma^2}x.$$

Let $r=\exp(\log\pi_\theta-\log\pi_{old})$. The raw branch contributes $rA\nabla\log\pi$ unless positive A has r above1+epsilon or negative A has r below1-epsilon. Average the active contributions, clip their combined L2 norm to1 and take an ascent step. Project gain to[0,2] and bias to[-0.5,0.5]. These bounds keep this fixture reproducible; they do not certify a physical robot.

$$\theta^+=\Pi\left(\theta+\eta\frac{G}{\max(1,\|G\|_2)}\right).$$

Here G is the mean surrogate gradient, eta the supplied step size and Pi the declared parameter projection. Held-out evaluation uses deterministic mean actions after each training iteration. It reports absolute final error and undiscounted reward sums separately from the training signal.

## Visual computation trace

| Stage | Frozen / changing data | Purpose |
|---|---|---|
| Collect | theta fixed for each rollout | behavior actions and log densities |
| Returns | rewards fixed | normalized update signal |
| PPO epochs | old likelihoods fixed, theta changes | bounded parameter update |
| Held-out goals | new theta, no action noise | independent outcome trace |

The table is the static visual and its text alternative; each row describes a transformation or decision.

## Worked calculation

theta=[0,0], train_goals=[1], noise=zeros((1,1,1)), eval_goals=[1], epochs1, learning_rate.01, epsilon.2: the single return normalizes to zero, so theta_history=[[0,0],[0,0]], training_return=[-1], evaluation_final_error=[[1]], evaluation_return=[-1], clip_fraction=[[0]].

## Why this matters on a robot

Using updated likelihoods as if they were the behavior policy erases the PPO ratio. Mixing held-out goals into the advantage batch leaks evaluation into learning. A shared bias can help positive targets while harming negative ones; report the per-goal errors rather than only one average.

## Physical contract and limits

Normalized joint position q; normalized velocity action units per second; dt=0.1 seconds; Gaussian action standard deviation0.2 normalized velocity units. Fixed-step synthetic episodes reset q=0 each training iteration and held-out evaluation. The T-step horizon is a true terminal. Original executable PPO training loop for a scalar integrator and linear Gaussian controller. It omits neural perception, a critic network, entropy bonus, MuJoCo and real hardware; it is not a VLA or a reproduction of published locomotion scores.

Source: [primary paper](https://arxiv.org/abs/1707.06347). Prerequisite: understand the observation/action schema supplied in the contract; no additional lesson is required.
