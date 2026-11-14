import numpy as np


def match_queries(cost):
    if not isinstance(cost, np.ndarray):
        raise TypeError("cost must be a NumPy array")
    if cost.dtype != np.float64 or cost.ndim != 2:
        raise ValueError("cost must be float64 (Q,M)")
    queries, targets = cost.shape
    if not 1 <= queries <= 128 or not 0 <= targets <= queries:
        raise ValueError("assignment dimensions")
    if not np.isfinite(cost).all() or (np.abs(cost) > 1e6).any():
        raise ValueError("finite bounded costs")
    if targets == 0:
        return np.empty(0, dtype=np.int64)
    # Target rows, query columns; index zero is the augmenting-path sentinel.
    rows = cost.T
    u = np.zeros(targets + 1)
    v = np.zeros(queries + 1)
    owner = np.zeros(queries + 1, dtype=np.int64)
    predecessor = np.zeros(queries + 1, dtype=np.int64)
    for target in range(1, targets + 1):
        owner[0] = target
        column = 0
        used = np.zeros(queries + 1, dtype=bool)
        slack = np.full(queries + 1, np.inf)
        while True:
            used[column] = True
            row = owner[column]
            reduced = rows[row - 1] - u[row] - v[1:]
            available = ~used[1:]
            improves = available & (reduced < slack[1:])
            slack[1:][improves] = reduced[improves]
            predecessor[1:][improves] = column
            candidate_slack = np.where(available, slack[1:], np.inf)
            next_column = int(np.argmin(candidate_slack)) + 1
            delta = slack[next_column]
            u[owner[used]] += delta
            v[used] -= delta
            slack[~used] -= delta
            column = next_column
            if owner[column] == 0:
                break
        while column:
            previous_column = predecessor[column]
            owner[column] = owner[previous_column]
            column = previous_column
    result = np.empty(targets, dtype=np.int64)
    for column in range(1, queries + 1):
        if owner[column]:
            result[owner[column] - 1] = column - 1
    return result

