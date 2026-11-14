import re
import numpy as np

_NAME = re.compile(r"[a-z][a-z0-9_-]{0,63}", re.ASCII)
_LABEL = re.compile(r"[a-z][a-z0-9_/-]{0,63}", re.ASCII)

def infer_episode_schema(episodes):
    if not isinstance(episodes, list) or len(episodes) > 1000:
        raise ValueError("episodes")
    result, counts, total = {}, {}, 0
    for episode in episodes:
        if not isinstance(episode, dict) or len(episode) > 128:
            raise ValueError("episode")
        for name, signal in episode.items():
            if not isinstance(name, str) or not _NAME.fullmatch(name):
                raise ValueError("name")
            if not isinstance(signal, dict) or set(signal) != {"values", "unit", "frame"}:
                raise ValueError("signal")
            values, unit, frame = signal["values"], signal["unit"], signal["frame"]
            if any(not isinstance(x, str) or not _LABEL.fullmatch(x) for x in (unit, frame)):
                raise ValueError("physical metadata")
            if not isinstance(values, np.ndarray) or values.dtype != np.float64 or values.ndim != 2:
                raise ValueError("values dtype or rank")
            t, width = values.shape
            total += values.size
            if not 1 <= t <= 10000 or not 1 <= width <= 128 or total > 2000000:
                raise ValueError("shape or workload")
            if not np.isfinite(values).all() or (np.abs(values) > 1e6).any():
                raise ValueError("values bounds")
            if name not in result:
                result[name] = {"shape": (width,), "unit": unit, "frame": frame,
                                "minimum": values.min(axis=0), "maximum": values.max(axis=0)}
                counts[name] = 0
            else:
                item = result[name]
                if item["shape"] != (width,) or item["unit"] != unit or item["frame"] != frame:
                    raise ValueError("inconsistent signal")
                item["minimum"] = np.minimum(item["minimum"], values.min(axis=0))
                item["maximum"] = np.maximum(item["maximum"], values.max(axis=0))
            counts[name] += 1
    for name, item in result.items():
        item["required"] = counts[name] == len(episodes)
    return result

