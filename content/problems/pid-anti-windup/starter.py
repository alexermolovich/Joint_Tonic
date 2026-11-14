def pid_step(error, previous_error, integral, dt, gains, output_limits) -> tuple[float, float, float]:
    """Return (bounded command, next integral, derivative) for one joint.

    Errors are radians, integral radian-seconds, and dt seconds.
    Integrate unless the candidate command and error push outward together.
    """
    # Calculate a candidate, select the integral, then recompute and clip.
    pass
