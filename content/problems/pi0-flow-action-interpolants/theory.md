# Sample Flow-Matching Action Interpolants and Targets: theory

## Intuition

Flow matching creates a simple path between a random starting action chunk and a demonstrated chunk. A network learns the direction of travel along that path, conditioned on the robot observation. This component creates the path point and its known direction; it does not yet learn or integrate the network.

## Define the time and tensor axes

Let clean normalized actions be $A\in\mathbb R^{B\times H\times D}$ and supplied noise be $E$ with the same shape. $H$ indexes future controller ticks, while $\tau_b\in[0,1]$ is dimensionless **flow time** for batch item $b$. It is broadcast as $(B,1,1)$, not interpreted as one timestamp per action step.

The path and its derivative are

$$
X_{bhd}(\tau_b)=(1-\tau_b)E_{bhd}+\tau_bA_{bhd},
$$

$$
U_{bhd}=\frac{\partial X_{bhd}}{\partial\tau_b}=A_{bhd}-E_{bhd}.
$$

$X(0)=E$ and $X(1)=A$. The velocity target is constant along this particular sampled straight path. It remains nonzero at an endpoint unless the supplied action and noise coincide.

## Mask the training pair

For boolean validity $M\in\{0,1\}^{B\times H}$, return

$$
\widetilde X_{bhd}=M_{bh}X_{bhd},\qquad\widetilde U_{bhd}=M_{bh}U_{bhd}.
$$

Both outputs must be masked. An all-padding input can produce a valid empty-information pair here because there is no division. A later regression loss needs its own policy for a zero valid count.

For one valid scalar, derivatives of the interpolant are $\partial X/\partial A=\tau$, $\partial X/\partial E=1-\tau$, and $\partial X/\partial\tau=A-E$. The target derivatives are1 with respect to A and-1 with respect to E. These identities make useful focused gradient checks.

## Contrast with diffusion noising

The published noising exercise uses square-root coefficients $\sqrt{\bar\alpha}A+\sqrt{1-\bar\alpha}E$ and supplies noise $E$ as its prediction target. This exercise instead uses linear coefficients and target $A-E$. Mixing a flow target with a noise-prediction sampler changes the model’s meaning. Under standard Gaussian E, the conditional variance of the linear interpolant is $(1-\tau)^2I$, as follows directly from scaling the noise; it should not be confused with its standard deviation.

## Worked calculation

For $A=6,E=2,\tau=1/4$, the interpolant is $X=3$ and target $U=4$. Increasing flow time by0.1 changes this straight-path point by0.4. That is a generative-coordinate derivative, not a physical joint velocity of0.4radians per second.

## Original flow diagram

| Flow time | Interpolant for noise 2, action 6 | Velocity target |
|---|---:|---:|
| 0 | 2 | 4 |
| 0.25 | 3 | 4 |
| 0.5 | 4 | 4 |
| 1 | 6 | 4 |

Read downward as motion along a straight path in normalized action space, not elapsed robot-control time.

Text alternative: start at the supplied noise, move a tau fraction toward the clean action, and label the point with the constant difference action-minus-noise. Apply the same horizon validity mask to the point and target.

## Why this matters on a robot

Flow time, physical control time, and action units are separate quantities. Confusing them can invert a sampler or misinterpret a velocity target as an actuator velocity. A model trained with one normalization artifact or time direction must be sampled with the same convention before generated actions are converted back into physical commands.

## Check your understanding

1. What are the interpolant and velocity target at tau0 and tau1?
2. Why must tau(B,) be reshaped before applying it to(B,H,D)?
3. If the path is reparameterized to run from data at0 to noise at1, what changes in its velocity target?

## Sources and prerequisites

[Primary paper, arXiv2410.24164v4 SectionIV page5](https://arxiv.org/pdf/2410.24164v4). This corrected revision gives actions-minus-noise as the velocity target, matching the derivative of the noise-to-action path. Earlier v1 printed the opposite target sign. Noise and flow times are supplied to make the exercise deterministic; it does not draw the paper’s timestep distribution, train a vector field, integrate an ODE, or reconstruct a full VLA. Padding masks are an explicit educational batching extension.

- [diffusion-action-noising](/problems/diffusion-action-noising)
