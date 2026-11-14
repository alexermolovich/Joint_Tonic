import re

_NAME = re.compile(r"[a-z][a-z0-9_-]{0,63}", re.ASCII)

def quality_performance(records):
    if not isinstance(records, list) or len(records) > 100000:
        raise ValueError("records")
    counts = {}
    for row in records:
        if not isinstance(row, tuple) or len(row) != 3:
            raise ValueError("trial")
        quality, task, success = row
        if any(not isinstance(label, str) or not _NAME.fullmatch(label) for label in (quality, task)):
            raise ValueError("labels")
        if type(success) is not bool:
            raise ValueError("success")
        key = (quality, task)
        if key not in counts:
            counts[key] = [0, 0]
            if len(counts) > 10000:
                raise ValueError("slice budget")
        counts[key][0] += 1
        counts[key][1] += int(success)
    by_slice, groups = [], {}
    for (quality, task), (trials, successes) in sorted(counts.items()):
        rate = successes / trials
        by_slice.append((quality, task, trials, successes, rate))
        if quality not in groups:
            groups[quality] = [0, 0, []]
        groups[quality][0] += trials
        groups[quality][1] += successes
        groups[quality][2].append(rate)
    by_quality = [(quality, n, s, s/n, sum(rates)/len(rates))
                  for quality, (n, s, rates) in sorted(groups.items())]
    return {"by_slice": by_slice, "by_quality": by_quality}

