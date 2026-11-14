# A target can have several joint explanations

## Intuition

Forward kinematics asks where the tool goes for given joint angles. Inverse kinematics asks which angles could explain a desired tool position. Even a simple two-link arm usually has two answers: the elbow can bend to either side. A useful solver declares its branch instead of relying on whichever angle function happens to be used.

Let $L_1,L_2>0$ be link lengths in meters, and $(x,y)$ the target in the fixed base frame. The shoulder angle $q_1$ and relative elbow angle $q_2$ are radians about +z.

## Reachability before angles

The tool's distance from the shoulder is $r=\sqrt{x^2+y^2}$. A two-link chain can reach an annulus:

$$
|L_1-L_2|\le r\le L_1+L_2.
$$

A target beyond the outer boundary requires stretched links; one inside the inner boundary would require the longer link to shrink. Neither is a numerical failure. Return a clear unreachable status.

The triangle geometry gives:

$$
c_2=\frac{x^2+y^2-L_1^2-L_2^2}{2L_1L_2},\qquad
q_2=\arccos(c_2).
$$

Choosing arccos selects the declared positive-elbow branch $q_2\in[0,\pi]$. The shoulder must point toward the target minus the bend introduced by the second link:

$$
q_1=\operatorname{atan2}(y,x)-
\operatorname{atan2}(L_2\sin q_2,L_1+L_2\cos q_2).
$$

The cosine may exceed one by tiny floating error at a reachable boundary. Clip only after the physical reachability test, so a genuinely impossible target is not silently projected into the workspace.

## Worked robot example

With unit links and target $(1,1)$, the elbow cosine is zero, giving $q_2=\pi/2$. The target bearing and internal offset are both $\pi/4$, so $q_1=0$. Forward kinematics then reaches $(1,1)$ exactly.

## Visual and failure interpretation

The planned sidecar draws the reachable annulus, target, chosen elbow branch, and tool residual. A text table reports target distance, branch, angles, and forward-check error. Full extension and complete folding are singular: an infinitesimal target displacement may require a large angle change or a different branch.

This exercise provides a geometric position solution, not a collision-free motion or safety guarantee. Real deployments also enforce joint limits, choose continuity across successive targets, and consider tool orientation. The equal-length origin case has infinitely many shoulder choices; its explicit convention keeps tests deterministic.
