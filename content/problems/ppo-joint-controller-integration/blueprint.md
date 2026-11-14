---
{
  "schema_version": 1,
  "problem_id": "ppo-joint-controller-integration",
  "content_version": "1.0.0",
  "status": "reviewed",
  "title": "Train and Evaluate a Tiny PPO Joint Controller",
  "summary": "Collect synthetic one-joint rollouts, update a Gaussian policy with PPO and evaluate held-out target positions.",
  "type": "pipeline",
  "difficulty": "hard",
  "estimated_minutes": 60,
  "domains": [
    "robot-learning"
  ],
  "topics": [
    "2017-proximal-policy-optimization",
    "policy-components"
  ],
  "paper_ids": [
    "2017-proximal-policy-optimization"
  ],
  "paper_sections": [
    "Original bounded PPO component. Normalization, boundary handling and diagnostic conventions are explicitly supplied; this does not train a complete locomotion policy."
  ],
  "track_ids": [],
  "prerequisite_problem_ids": [
    "ppo-clipped-policy-surrogate",
    "ppo-normalize-batched-advantages",
    "ppo-policy-update-clip-fractions",
    "ppo-boundary-value-targets"
  ],
  "runtime": {
    "language": "python",
    "python": "3.12.3",
    "image_digest": "pending-local-worker-build",
    "runtime_id": "python-3.12.3-numpy-2.2.4-torch-2.6.0-cpu-bwrap-v2",
    "dependencies": {
      "numpy": "2.2.4"
    },
    "limits": {
      "wall_seconds": 18,
      "cpu_seconds": 10,
      "memory_mb": 4096,
      "output_kb": 64
    }
  },
  "entrypoint": "solution.train_joint_controller",
  "physical_contract": {
    "frames": [
      "one normalized scalar joint coordinate; no real robot or collision model"
    ],
    "units": {
      "q": "normalized joint position",
      "action": "normalized joint position per second",
      "dt": "0.1 seconds",
      "sigma": "0.2 normalized action units"
    },
    "axes": "noise(I,B,T), goals(B), theta(2), evaluation_goals(M)",
    "timestamp_assumptions": "fixed0.1-second integration; each training iteration starts all positions atzero",
    "batching": "B independent episodes with shared policy; I policy iterations; evaluation starts separately"
  },
  "grading": {
    "mode": "numerical",
    "seed": 20261114,
    "rtol": 1e-07,
    "atol": 1e-09,
    "public_case_families": [
      "two-worked-examples"
    ],
    "hidden_case_families": [
      "documented-boundaries",
      "invalid-inputs",
      "independent-invariants"
    ],
    "performance_class": "cpu"
  },
  "fixtures": {
    "source": "original-synthetic",
    "license": "CC0-1.0",
    "version_or_hash": "synthetic-v1-seed-20261113"
  },
  "provenance": {
    "authoring_notes": "Original bounded PPO component. Normalization, boundary handling and diagnostic conventions are explicitly supplied; this does not train a complete locomotion policy.",
    "primary_urls": [
      "https://arxiv.org/abs/1707.06347"
    ],
    "paper_card": "research/papers/robot-learning-rl/2017-proximal-policy-optimization.md",
    "manifest": "research/IMPLEMENTATION_BACKLOG.md"
  },
  "owners": [
    "research_curator"
  ],
  "reviewers": []
}
---

# Train and Evaluate a Tiny PPO Joint Controller

## Exact executable contract

`train_joint_controller(initial_theta, train_goals, noise, eval_goals, epochs, learning_rate, epsilon)` receives theta real(2,) with gain in[0,2] and bias in[-.5,.5]; goals real(B,),1<=B<=32, absolute value<=1; supplied Gaussian-standardized noise real(I,B,T),1<=I<=8,1<=T<=16, absolute value<=3; evaluation goals real(M,),1<=M<=32, absolute value<=1. epochs is a non-bool integer1..4, learning_rate scalar[0,.01], epsilon scalar[.05,.4]. All other numeric arrays finite real CPU, no boolean/complex inputs; malformed input raises ValueError. Arrays are preserved and output arrays independent float64.

Each iteration collects fresh fixed-horizon episodes from q=0 with the current policy. At step t, feature x=[goal-q,1], Gaussian mean mu=x@theta, action a=mu+0.2*noise, q_next=q+0.1*a, reward=-(q_next-goal)^2-0.01*a^2. Record x,a and the behavior log density -0.5*((a-mu)/.2)^2-log(.2*sqrt(2*pi)). This is an unconstrained synthetic scalar integrator, not MuJoCo or real hardware. The finite horizon is a true task terminal.

Compute discounted returns backward with gamma=.95 and terminal bootstrap0. With zero value baseline, advantages are those returns, globally normalized over B*T by sqrt(population variance+1e-8). Hold actions, advantages and behavior likelihoods fixed during each of the specified PPO epochs.

For current theta, recompute Gaussian log densities and ratios exp(log_new-log_old). Maximize mean(min(ratio*A,clip(ratio,1-epsilon,1+epsilon)*A)). Active derivative uses the raw branch except when A>0 and ratio>1+epsilon, or A<0 and ratio<1-epsilon; equality uses the raw branch, A=0 contributes zero. The gradient is mean(active*ratio*A*(a-mu)/.2^2*x). Clip its global L2 norm to at most1, take theta += learning_rate*gradient, then project gain to[0,2] and bias to[-.5,.5]. No extra optimizer, critic, entropy bonus or randomness.

After each iteration, evaluate the new theta with deterministic mean actions (no noise), same T-step dynamics and independent q=0 on eval_goals. Return dict theta_history:float64(I+1,2), training_return:float64(I,) mean UNDISCOUNTED reward sum from that iteration's collected episodes, evaluation_final_error:float64(I,M) absolute final goal error, evaluation_return:float64(I,) mean UNDISCOUNTED evaluation reward sum, clip_fraction:float64(I,epochs) valid fraction of ratios strictly outside clip bounds BEFORE each epoch update.

## Worked checks

1. Initial theta[0,0], goals[1], zero noise(1,1,1), eval[1], epochs1,lr.01,epsilon.2: one advantage normalizes to0; no update. theta_history=[[0,0],[0,0]],training_return[-1],evaluation_final_error[[1]],evaluation_return[-1],clip_fraction[[0]].
2. Initial theta[0,0], train_goals[1,1], noise=[[[1],[-1]]], eval_goals[0], epochs1,lr0,epsilon.2: actions[.2,-.2], rewards[-.9608,-1.0408],mean return-1.0008; no parameter change; held-out goal0 has error0 and return0.

## Original theory and visual

Show the actor -> scalar dynamics -> terminal returns -> normalized advantages -> frozen rollout PPO update -> held-out deterministic evaluation flow. Define score-function derivative, clipped branch, norm clipping and projection. Worked one-step fixture and failed generalization conditions. This integration trains a tiny linear Gaussian controller only; it does not reproduce PPO's neural locomotion experiments or prove hardware safety.

## Verification plan

Independent contract and implementation review; scalar loop oracle; two public fixtures; real nonzero learning and multiple epochs; held-out independence, sign/mask/discounting mutants, dtype/range invalid cases, maximal8x32x16 scale and nonalias checks; actual isolated Run/Submit and starter rejection. Pin existing NumPy worker runtime. Original synthetic CC0 fixtures only.
