import numpy as np


def euler_action_flow(initial, times, velocity):
    if not isinstance(initial, np.ndarray) or not isinstance(times, np.ndarray) or not callable(velocity):
        raise TypeError("Expected arrays and a callable velocity")
    if initial.dtype != np.float64 or initial.ndim != 3:
        raise ValueError("Invalid action dtype or rank")
    b, h, d = initial.shape
    if not 1 <= b <= 16 or not 1 <= h <= 64 or not 1 <= d <= 32:
        raise ValueError("Invalid action dimensions")
    if not np.isfinite(initial).all() or np.any(np.abs(initial) > 1e6):
        raise ValueError("Invalid initial actions")
    if times.dtype != np.float64 or times.ndim != 1 or not 2 <= times.size <= 129:
        raise ValueError("Invalid flow-time grid")
    if not np.isfinite(times).all() or times[0] != 0 or times[-1] != 1 or np.any(np.diff(times) <= 0):
        raise ValueError("Flow times must increase strictly from zero to one")
    if times.size * initial.size > 1_000_000:
        raise ValueError("Trace element budget exceeded")
    state = initial.copy()
    trace = np.empty((times.size, b, h, d), dtype=np.float64)
    trace[0] = state
    for k in range(times.size - 1):
        field = velocity(state, float(times[k]))
        if not isinstance(field, np.ndarray) or field.dtype != np.float64 or field.shape != initial.shape:
            raise ValueError("Invalid velocity return type, dtype or shape")
        if not np.isfinite(field).all() or np.any(np.abs(field) > 1e6):
            raise ValueError("Invalid velocity values")
        state = state + (times[k + 1] - times[k]) * field
        trace[k + 1] = state
    return state.copy(), trace
