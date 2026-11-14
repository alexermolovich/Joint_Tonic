from fractions import Fraction
import re

_NAME = re.compile(r"[a-z][a-z0-9_-]{0,63}", re.ASCII)

def select_checkpoint(candidates, max_loss, min_success, min_trials):
    if type(max_loss) not in (int, float) or not 0 <= max_loss <= 1e6:
        raise ValueError("max_loss")
    if type(min_trials) is not int or not 1 <= min_trials <= 1000000:
        raise ValueError("min_trials")
    if not isinstance(min_success, tuple) or len(min_success) != 2:
        raise ValueError("min_success")
    p, q = min_success
    if type(p) is not int or type(q) is not int or not 1 <= q <= 1000000 or not 0 <= p <= q:
        raise ValueError("success threshold")
    if not isinstance(candidates, list) or len(candidates) > 10000:
        raise ValueError("candidates")
    seen, eligible = set(), []
    for row in candidates:
        if not isinstance(row, tuple) or len(row) != 4:
            raise ValueError("candidate")
        name, loss, successes, trials = row
        if not isinstance(name, str) or not _NAME.fullmatch(name) or name in seen:
            raise ValueError("checkpoint ID")
        seen.add(name)
        if type(loss) not in (int, float) or not 0 <= loss <= 1e6:
            raise ValueError("loss")
        if type(successes) is not int or type(trials) is not int or not 0 <= trials <= 1000000 or not 0 <= successes <= trials:
            raise ValueError("counts")
        if loss <= max_loss and trials >= min_trials and successes*q >= p*trials:
            eligible.append(row)
    if not eligible:
        return None
    return min(eligible, key=lambda row: (-Fraction(row[2], row[3]), row[1], row[0]))[0]

