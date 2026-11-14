import numpy as np

def mpc_tracking_cost(states, targets, controls, state_weights, control_weights, terminal_weights):
    """Score a finite-horizon predicted trajectory with stage, control-effort, and terminal penalties."""
    raise NotImplementedError
