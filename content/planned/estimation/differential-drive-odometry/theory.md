# Two wheel distances imply an arc

## Intuition

When both wheels travel equally, the base moves straight. When the right wheel travels farther, the robot turns left. The midpoint of the axle follows an arc whose length depends on average wheel travel, while heading change depends on the difference.

Let $d_l,d_r$ be signed left/right travel in meters over one synchronized interval. Let $b>0$ be track width in meters. The world pose is $(x,y,\theta)$, where heading is counterclockwise from world +x. Robot forward is local +x and left is local +y.

## Motion implied by wheel travel

The axle midpoint's signed arc length d and rotation $\phi$ are:

$$
d=\frac{d_r+d_l}{2},\qquad
\phi=\frac{d_r-d_l}{b}.
$$

For nonzero rotation, radius is $\rho=d/\phi$. Integrating constant curvature yields:

$$
\Delta x=\rho[\sin(\theta+\phi)-\sin\theta],\qquad
\Delta y=\rho[\cos\theta-\cos(\theta+\phi)].
$$

These displacements are expressed in the world frame. They are not simply d along the robot's starting forward axis unless the turn is zero.

Near zero rotation, direct division can lose accuracy. An equivalent midpoint form is:

$$
(\Delta x,\Delta y)=d\,\operatorname{sinc}(\phi/2)
(\cos(\theta+\phi/2),\sin(\theta+\phi/2)),
$$

where $\operatorname{sinc}(a)=\sin(a)/a$ with value 1 at zero. This is the unnormalized sinc convention, not a library definition using $\sin(\pi a)/(\pi a)$.

## Worked mobile-base example

Starting at the origin with heading zero, take $b=1$, $d_l=0$, and $d_r=\pi/2$. Then $\phi=\pi/2$, $d=\pi/4$, and radius is 0.5 meters. The axle midpoint ends at $(0.5,0.5)$ with heading $\pi/2$. Approximating the path as a straight translation would miss that endpoint.

## Visual and practical limits

The planned viewport shows wheel paths, instantaneous turn center, and the axle midpoint's arc. A table reports wheel distances, curvature, world displacement, and normalized heading. Pure rotation has zero midpoint translation even though both wheels move.

Wheel slip, unequal effective radii, flexible tires, and track-width calibration produce systematic drift. Integration alone cannot detect those errors. Keep wheel calibration, encoder signs, timestamps, and robot geometry with an odometry trace. This lesson produces ideal relative motion that later estimators can compare with camera or inertial evidence; it does not recover an absolute world pose.
