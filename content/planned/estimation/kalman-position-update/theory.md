# Fuse a Position Measurement with a Kalman Update: theory

## Intuition

A predicted robot position is a belief, not a perfect coordinate. A new sensor reading is also uncertain. The measurement update changes the belief by an amount justified by their relative uncertainty. A high-quality position sensor can correct a weak prediction strongly; a noisy reading should only nudge a confident prediction.

## A position and its uncertainty

Let $\mu$ be the predicted position in meters and $P$ its variance in square meters. A same-time measurement $z$ has independent, zero-mean error variance $R>0$. The identity observation model means the sensor measures that same position axis directly. The innovation is

$$
r=z-\mu,\qquad S=P+R,\qquad K=\frac{P}{S}.
$$

Here $r$ is meters, innovation variance $S$ is square meters, and gain $K$ is dimensionless. Because $P\geq0$ and $R>0$, gain stays between zero and one. The update cannot reverse the innovation direction.

$$
\mu^+=\mu+Kr,\qquad
P^+=(1-K)^2P+K^2R.
$$

The posterior variance is written in Joseph form. The first term retains prediction uncertainty after correction; the second adds the measurement noise that enters through the gain. Under this scalar model it agrees with $(1-K)P$, while making the two noise contributions visible.

## Worked robot example

Suppose wheel odometry predicts $\mu=2$ m with $P=4$ m². A beacon measures $z=5$ m with $R=1$ m². Innovation is 3 m, gain is $4/5$, and the corrected position is 4.4 m. Posterior variance is $0.2^2(4)+0.8^2(1)=0.8$ m². The robot becomes more confident, but not certain.

If the same beacon instead has variance 16 m², its gain falls to 0.2 and the corrected position is only 2.6 m. The sensor value did not change; its credibility did.

## Visual explanation

Show prior and measurement intervals on the same meter axis, then move the measurement-noise control. A linked table lists innovation, gain, posterior position, and variance. Text labels distinguish uncertainty from physical robot width.

## Robot relevance and failure modes

Time mismatch can make an accurate sensor appear inconsistent with odometry. Frame mismatch can produce a smooth but wrong correction. Shared sensor sources violate the independence assumption and can make the estimate overconfident. This lesson isolates one measurement update; a complete estimator also requires prediction, calibration, covariance models, and outlier handling. It prepares the learner to inspect uncertainty propagation before studying visual-inertial estimation papers.

