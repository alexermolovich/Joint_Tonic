# Interpolate a Time-Parameterized Joint Trajectory: theory

## Intuition

A list of target poses is incomplete without timing. The same joint displacement over 0.1 seconds and over 10 seconds represents very different motion. A time-parameterized trajectory tells the controller both where a joint should be and how quickly the requested command changes between waypoints.

## The interval contract

Let strictly increasing times $t_0,\ldots,t_{K-1}$ use one monotonic clock in seconds. Each row $q_i\in\mathbb R^D$ stores D joint positions in radians. These coordinates are already unwrapped; crossing the displayed angle boundary does not imply taking the shortest circular path.

For an interior query $t\in[t_i,t_{i+1})$, define

$$
\lambda=\frac{t-t_i}{t_{i+1}-t_i},\qquad
q(t)=(1-\lambda)q_i+\lambda q_{i+1}.
$$

The dimensionless fraction $\lambda$ applies to every joint channel. It is the time fraction, not the waypoint index fraction. The interval velocity is

$$
\dot q(t)=\frac{q_{i+1}-q_i}{t_{i+1}-t_i}.
$$

Its unit is radians per second. Choosing the right interval at an interior knot makes a velocity discontinuity deterministic. Endpoint holding returns the endpoint position and zero velocity, avoiding accidental extrapolation when a controller runs early or late.

## Worked command example

Take times $[0,2,5]$ s and joint vectors $[[0,0],[2,-2],[5,1]]$ rad. At 1 s, the fraction in the first interval is one half, giving position $[1,-1]$ and velocity $[1,-1]$ rad/s. At the interior knot 2 s, the position is $[2,-2]$, but the chosen right-hand interval has velocity $[1,1]$ rad/s. Position is continuous while velocity changes abruptly.

## Visual explanation

Show joint position curves with waypoint markers and the query cursor. A linked velocity plot displays the chosen interval's slope; labels identify endpoint hold regions. A table lists bracketing times, fraction, desired position, and velocity for keyboard access.

## Robot relevance and failure modes

Treating irregular timestamps as equally spaced changes the commanded speed. Mixing a wall clock with elapsed trajectory time can make every query hold the final waypoint. Linear position interpolation alone does not enforce motor limits, collision avoidance, acceleration continuity, or jerk constraints. Those checks belong in later trajectory-generation and control problems. This sampler provides the execution-time vocabulary needed to reason about learned action chunks and receding-horizon policies.

