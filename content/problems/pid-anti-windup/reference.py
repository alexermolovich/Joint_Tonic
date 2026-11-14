import math
from numbers import Real


def _scalar(value):
    if not isinstance(value, Real) or isinstance(value, bool):
        raise ValueError("Expected a real scalar, excluding booleans")
    try:
        result = float(value)
    except OverflowError as exc:
        raise ValueError("Scalar is outside the supported range") from exc
    if not math.isfinite(result) or abs(result) > 1e6:
        raise ValueError("Values must be finite and bounded by 1e6")
    return result


def pid_step(error, previous_error, integral, dt, gains, output_limits):
    error, previous_error, integral, dt = map(_scalar, (error, previous_error, integral, dt))
    try:
        kp, ki, kd = map(_scalar, gains)
        lower, upper = map(_scalar, output_limits)
    except (TypeError, OverflowError) as exc:
        raise ValueError("Gains and limits must be real sequences of length3 and2") from exc
    if dt <= 0 or min(kp, ki, kd) < 0 or lower >= upper:
        raise ValueError("Require dt>0, nonnegative gains, increasing limits")
    derivative = (error - previous_error) / dt
    candidate = integral + error * dt
    effort = kp * error + ki * candidate + kd * derivative
    if not all(math.isfinite(v) for v in (derivative, candidate, effort)):
        raise ValueError("Nonfinite intermediate calculation")
    outward = (effort > upper and error > 0) or (effort < lower and error < 0)
    next_integral = integral if outward else candidate
    command = kp * error + ki * next_integral + kd * derivative
    if not math.isfinite(command):
        raise ValueError("Nonfinite command")
    return float(min(upper, max(lower, command))), float(next_integral), float(derivative)
