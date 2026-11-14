# Stop integral state fighting an actuator limit

## Intuition

A joint controller may request more effort than a motor can deliver. Clipping the command restricts output but does not stop integral state accumulating. That state can keep commanding excessive effort after the target error shrinks.

## One discrete update

Let $e_k,e_{k-1}$ be consecutive angular errors in radians, $\Delta t>0$ the period in seconds, and $I_{k-1}$ the previous integral in radian-seconds. The candidate update is

$$
d_k=\frac{e_k-e_{k-1}}{\Delta t},\qquad
I_c=I_{k-1}+e_k\Delta t,\qquad
u_c=K_p e_k+K_i I_c+K_d d_k.
$$

The derivative $d_k$ has rad/s units. Gains $K_p,K_i,K_d$ have command/rad, command/(rad·s), and command·s/rad units respectively, so all three effort terms can be added.

For lower and upper limits $\ell<h$, conditional integration selects

$$
I_k=\begin{cases}
I_{k-1},&(u_c>h\land e_k>0)\lor(u_c<\ell\land e_k<0),\\
I_c,&\text{otherwise}.
\end{cases}
$$

Recompute $u=K_p e_k+K_i I_k+K_d d_k$ and return $\min(h,\max(\ell,u))$. A rejected integral must not influence this step's command.

## Visual: the decision path

| Candidate effort | Error | Integral decision | Reason |
|---|---|---|---|
| Above upper limit | Positive | Keep old state | Prevent positive windup |
| Below lower limit | Negative | Keep old state | Prevent negative windup |
| Above upper limit | Negative | Accept candidate | Allow unwinding |
| Within or exactly on limits | Either | Accept candidate | No outward saturation |

Read the table as a decision diagram: effort and error jointly choose stored state; clipping happens afterward. It is a static text alternative.

With $e_k=0.2$ rad, $I_{k-1}=0$, $\Delta t=0.1$ s and gains (2,1,0), candidate integral is 0.02 rad·s and command $0.4+0.02=0.42$. Limits ±1 permit integration.

## Why this matters on a robot

An arm pressing against a stop can build a large integral, then overshoot when contact ends. Conditional integration addresses this state buildup; it does not guarantee stability, enforce joint limits, or protect hardware.

A common error freezes integration whenever effort saturates, preventing useful unwinding. Another uses a nominal period despite timestamp jitter, distorting both derivative and integral.

## Check your understanding

- Do we integrate exactly on the limit? Yes; rejection uses strict inequalities.
- Can output still saturate after rejecting integration? Yes; proportional or derivative effort can exceed the limit alone.

## Source and scope

Åström and Murray's [Feedback Systems](https://www.cds.caltech.edu/~murray/books/AM05/pdf/fbs-pid_01Jan19.pdf) gives the control context. This task defines a particular conditional-integration discretization; alternative anti-windup designs are outside its contract.
