from fractions import Fraction
import re

_NAME = re.compile(r"[a-z][a-z0-9_-]{0,63}", re.ASCII)

def compare_checkpoint_metrics(records):
    if not isinstance(records, list) or not 1 <= len(records) <= 10000:
        raise ValueError("records")
    seen = set()
    for record in records:
        if not isinstance(record, tuple) or len(record) != 4:
            raise ValueError("record")
        name, loss, successes, trials = record
        if not isinstance(name, str) or not _NAME.fullmatch(name) or name in seen:
            raise ValueError("checkpoint ID")
        seen.add(name)
        if type(loss) not in (int, float) or not 0 <= loss <= 1e6:
            raise ValueError("loss")
        if type(successes) is not int or type(trials) is not int or not 1 <= trials <= 1000000 or not 0 <= successes <= trials:
            raise ValueError("counts")
    offline = [row[0] for row in sorted(records, key=lambda row: (row[1], row[0]))]
    rollout = [row[0] for row in sorted(records, key=lambda row: (-Fraction(row[2], row[3]), row[0]))]
    return {"offline_order": offline, "rollout_order": rollout, "disagree": offline[0] != rollout[0]}

