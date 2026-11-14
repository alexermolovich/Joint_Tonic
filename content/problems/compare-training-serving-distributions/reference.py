import re

_NAME = re.compile(r"[a-z][a-z0-9_-]{0,63}", re.ASCII)

def categorical_skew(train_counts, serve_counts, threshold):
    if type(threshold) not in (int, float) or not 0 <= threshold <= 1:
        raise ValueError("threshold")
    totals = []
    for counts in (train_counts, serve_counts):
        if not isinstance(counts, dict) or len(counts) > 10000:
            raise ValueError("histogram")
        for name, value in counts.items():
            if not isinstance(name, str) or not _NAME.fullmatch(name):
                raise ValueError("category")
            if type(value) is not int or not 0 <= value <= 10**12:
                raise ValueError("count")
        total = sum(counts.values())
        if total == 0:
            raise ValueError("empty probability distribution")
        totals.append(total)
    deltas = [(name, serve_counts.get(name, 0) / totals[1] - train_counts.get(name, 0) / totals[0])
              for name in sorted(train_counts.keys() | serve_counts.keys())]
    distance = max(abs(delta) for _, delta in deltas)
    return {"deltas": deltas, "distance": distance, "flagged": distance > threshold}

