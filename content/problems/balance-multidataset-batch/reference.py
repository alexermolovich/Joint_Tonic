import re

_NAME = re.compile(r"[a-z][a-z0-9_-]{0,63}", re.ASCII)

def allocate_dataset_batch(weights, batch_size):
    if not isinstance(weights, dict) or not 1 <= len(weights) <= 10000:
        raise ValueError("weights")
    if type(batch_size) is not int or not 0 <= batch_size <= 1000000:
        raise ValueError("batch_size")
    for name, weight in weights.items():
        if not isinstance(name, str) or not _NAME.fullmatch(name):
            raise ValueError("dataset ID")
        if type(weight) is not int or not 0 <= weight <= 10**12:
            raise ValueError("weight")
    total = sum(weights.values())
    if total == 0:
        raise ValueError("zero total weight")
    result = {name: batch_size*weights[name]//total for name in sorted(weights)}
    remaining = batch_size - sum(result.values())
    ranked = sorted(weights, key=lambda name: (-(batch_size*weights[name] % total), name))
    for name in ranked[:remaining]:
        result[name] += 1
    return result

