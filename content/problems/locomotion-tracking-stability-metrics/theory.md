# Compute Gait Tracking and Stability Metrics

## Intuition

Command tracking and body stability describe different parts of locomotion. Keep their terms separate so a good tracking reward cannot hide unwanted vertical motion or body tilt.

## Mathematical mechanism

For base-frame linear velocity $v\in\mathbb R^3$ (m/s), angular velocity $\omega\in\mathbb R^3$ (rad/s), and command $c=(c_x,c_y,c_\omega)$, compute $$e_v=(v_x-c_x)^2+(v_y-c_y)^2,\quad e_\omega=(\omega_z-c_\omega)^2,\quad r_v=e^{-e_v/\sigma_v},\quad r_\omega=e^{-e_\omega/\sigma_\omega}.$$ The positive scales have squared velocity and squared angular-rate units respectively, making both rewards dimensionless. With downward unit gravity $g$ expressed in the base frame, the diagnostic penalties are $$p_z=v_z^2,\qquad p_\omega=\omega_x^2+\omega_y^2,\qquad p_g=g_x^2+g_y^2.$$ The first two penalties retain squared physical units. For each environment, average the five terms only across valid time samples; zero masked per-step rows and return NaN means when its count is zero. The gravity-xy surrogate is also zero for an upside-down body and must not be mistaken for an upright-state certificate.

## Visual computation trace

| Signal at v=(.8,.1,.2), command=(1,0,.5), omega=(.1,.2,.3) | Value |
|---|---|
| Horizontal squared error | .05 |
| Yaw squared error | .04 |
| Scales .25 give rewards | exp(-.2), exp(-.16) |
| Vertical / roll-pitch penalties | .04 / .05 |

The table is the static visual and its text alternative; each row describes a transformation or decision.

## Worked calculation

B=T=1, measured v[.8,.1,.2], w[.1,.2,.3], command[1,0,.5], gravity[0,0,-1], validTrue, scales .25,.25 -> terms [exp(-.2),exp(-.16),.04,.05,0], count1 and same means.

## Why this matters on a robot

A velocity expressed in the wrong frame makes a correct gait appear inaccurate. Combining unlike-unit penalties without calibrated weights obscures the physical tradeoff. Tilt alone cannot distinguish upright from inverted configurations.

## Physical contract and limits

Positions and terrain lengths use meters; velocities m/s; angular rates rad/s; contact forces N; durations seconds; normalized action and unit-gravity coordinates are dimensionless. Penalty terms retain the individual units stated in the contract. Each environment is independent. Supplied episode counters and reset flags refer to the same control transition. Terrain update occurs on subsequent resets; no wall-clock scheduling or simulator action is performed. Bounded component associated with Learning to Walk in Minutes. Released reward/termination/curriculum formulas are isolated from full PPO training, physics, command randomization and hardware transfer. Supplied initialization states and recorded draws make replay deterministic.

Source: [primary paper](https://github.com/leggedrobotics/legged_gym/blob/master/legged_gym/envs/base/legged_robot.py). Prerequisite: understand the observation/action schema supplied in the contract; no additional lesson is required.
