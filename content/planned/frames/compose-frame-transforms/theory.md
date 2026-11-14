# A calibration chain is a route between frames

## Intuition

A point observed by a wrist camera passes through two coordinate descriptions before the planner can use it: camera to robot base, then base to world. The matrices describe these changes of coordinates. Multiplication follows the route; it does not mean “apply the matrix nearest the world name first.”

Write $T_{ab}$ for **a-from-b**, containing rotation $R_{ab}$ and translation $t_{ab}$. The columns of $R_{ab}$ are b's axes expressed in a, while $t_{ab}$ is b's origin expressed in a. Translation is measured in meters; rotations are dimensionless. All calibrations here refer to one synchronized instant.

## Composition with physical meaning

For a camera point $p_c$, first express it in b and then in a:

$$
p_b=R_{bc}p_c+t_{bc},\qquad
p_a=R_{ab}p_b+t_{ab}.
$$

Substitution gives the composed rotation and translation:

$$
R_{ac}=R_{ab}R_{bc},\qquad
t_{ac}=R_{ab}t_{bc}+t_{ab}.
$$

The second translation cannot simply be added unchanged: it was measured along b's axes. The first rotation turns it into a's coordinates. Homogeneous multiplication packages exactly these operations as $T_{ac}=T_{ab}T_{bc}$.

For the inverse, orthogonality gives:

$$
R_{ca}=R_{ac}^{\mathsf T},\qquad
t_{ca}=-R_{ac}^{\mathsf T}t_{ac}.
$$

Negating translation without rotating it leaves the answer in the wrong frame.

## A robot example

Let the base be translated one meter along world x and rotated 90 degrees about world z. A camera one meter along base x is then at world position $(1,1,0)$, not $(2,0,0)$. Its mounting offset turns with the base. The inverse translation becomes $(-1,1,0)$ in the camera frame.

## Visual and numerical checks

The planned visual shows world, base, and camera axes with arrows labeled by direction. Selecting a point follows the two transformations; a table lists the intermediate coordinates. Compare this with a single composed transformation. An inverse round trip should restore the original point within tolerance.

## Why it matters and what can fail

Frame-order bugs often produce plausible numbers and no runtime error. Their effect becomes obvious only when the robot rotates, because a mounting offset incorrectly stays aligned with the world. Carry frame IDs, timestamp, units, and calibration version with the matrix. This problem validates rigid transforms and known chains; it does not solve calibration, account for flexibility, or synchronize moving frames.

[Modern Robotics](https://modernrobotics.northwestern.edu/nu-gm-book-resource/3-3-1-homogeneous-transformation-matrices/) provides the frame convention; the explanation and fixtures here are original.
