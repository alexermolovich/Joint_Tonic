# Build a Pre-Grasp Pose Along the Tool Axis: theory

## Intuition

A robot usually should not teleport its gripper directly to a grasp pose. It first moves to a nearby pre-grasp pose, then follows a controlled approach direction. That direction belongs to the gripper frame. A top-down grasp and a side grasp therefore need different world-space offsets even if their approach distances are identical.

## Read the target transform

Let $T_{wg}$ map grasp-frame coordinates into world coordinates. Its rotation $R_{wg}$ has the grasp basis vectors as columns, expressed in world coordinates. Its translation $t_{wg}$ is the target grasp origin in meters.

The unit grasp z-axis expressed in world coordinates is

$$
z_w=R_{wg}\begin{bmatrix}0\\0\\1\end{bmatrix}.
$$

By contract, the final approach moves along positive grasp z. The pre-grasp origin must therefore lie behind the target along that direction. For nonnegative distance $d$ meters,

$$
t_{w,\mathrm{pre}}=t_{wg}-d\,z_w,\qquad
R_{w,\mathrm{pre}}=R_{wg}.
$$

The distance affects translation only. The three rotation columns remain orthonormal and right-handed; a translation offset cannot fix an invalid orientation.

## Worked grasp example

For an identity orientation and target origin $(0.4,0.2,0.3)$ m, grasp z points along world z. With $d=0.1$ m, the pre-grasp origin is $(0.4,0.2,0.2)$ m. Moving 0.1 m along the tool's positive z then reaches the target.

Rotate the grasp by 90 degrees about world y. Its local z now points along world x. A target at $(1,0,0.5)$ m with $d=0.2$ m has pre-grasp origin $(0.8,0,0.5)$ m. Subtracting world z instead would produce a plausible but wrong approach.

## Visual explanation

Draw target and pre-grasp frames with matching orientations, connected by an approach arrow. A distance control shifts only the pre-grasp origin. A table lists the rotation's third column, offset vector, and resulting origin; axis labels convey direction without color.

## Robot relevance and failure modes

A grasp frame is not necessarily the robot wrist frame. Missing the fixed tool calibration shifts contact geometry. A correct geometric pre-grasp can still be unreachable, collide with an obstacle, exceed joint limits, or approach through the object. Learned grasp-quality work supplies useful applications, but this lesson isolates frame-correct pose construction. Reachability and swept-path validation must remain explicit later checks.

