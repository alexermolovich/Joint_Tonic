import re
import numpy as np

_NAME = re.compile(r"[a-z][a-z0-9_-]{0,63}", re.ASCII)
_UNITS = {"m": ("length", 1.0), "cm": ("length", .01), "mm": ("length", .001),
          "rad": ("angle", 1.0), "deg": ("angle", np.pi/180), "unitless": ("unitless", 1.0)}

def _channels(rows):
    if not isinstance(rows, list) or not 1 <= len(rows) <= 64:
        raise ValueError("channels")
    seen = set()
    for row in rows:
        if not isinstance(row, tuple) or len(row) != 2:
            raise ValueError("channel descriptor")
        name, unit = row
        if not isinstance(name, str) or not _NAME.fullmatch(name) or name in seen:
            raise ValueError("channel name")
        if not isinstance(unit, str) or unit not in _UNITS:
            raise ValueError("channel unit")
        seen.add(name)

def remap_robot_episode(episode, target_channels):
    fields = {"values", "timestamps_ns", "channels", "frame", "control_mode",
              "dataset_id", "dataset_version", "robot_id"}
    if not isinstance(episode, dict) or set(episode) != fields:
        raise ValueError("episode fields")
    for key in ("frame", "dataset_id", "dataset_version", "robot_id"):
        value = episode[key]
        if not isinstance(value, str) or not _NAME.fullmatch(value):
            raise ValueError("metadata")
    mode = episode["control_mode"]
    if not isinstance(mode, str) or mode not in ("position", "delta"):
        raise ValueError("control mode")
    _channels(episode["channels"])
    _channels(target_channels)
    values, stamps = episode["values"], episode["timestamps_ns"]
    if not isinstance(values, np.ndarray) or values.dtype != np.float64 or values.ndim != 2:
        raise ValueError("values dtype or rank")
    length, width = values.shape
    if not 0 <= length <= 10000 or not 1 <= width <= 64 or width != len(episode["channels"]):
        raise ValueError("values dimensions")
    if not np.isfinite(values).all() or (np.abs(values) > 1e6).any():
        raise ValueError("values bounds")
    if not isinstance(stamps, np.ndarray) or stamps.dtype != np.int64 or stamps.shape != (length,):
        raise ValueError("timestamps")
    if (stamps < 0).any() or (stamps[1:] <= stamps[:-1]).any():
        raise ValueError("timestamp ordering")
    source = {name: (index, unit) for index, (name, unit) in enumerate(episode["channels"])}
    indices, scales = [], []
    for name, unit in target_channels:
        if name not in source:
            raise ValueError("unknown target channel")
        index, old_unit = source[name]
        if _UNITS[old_unit][0] != _UNITS[unit][0]:
            raise ValueError("incompatible units")
        indices.append(index)
        scales.append((_UNITS[old_unit][1], _UNITS[unit][1]))
    output = np.empty((length, len(indices)), dtype=np.float64)
    for column, (index, (old_scale, new_scale)) in enumerate(zip(indices, scales)):
        output[:, column] = values[:, index] * old_scale / new_scale
    result = dict(episode)
    result["values"] = output
    result["timestamps_ns"] = stamps.copy()
    result["channels"] = list(target_channels)
    return result

