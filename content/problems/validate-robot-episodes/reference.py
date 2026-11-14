"""Original schema checker for synthetic robot episodes."""
import numbers
import numpy as np


def _number(value):
    return isinstance(value, numbers.Real) and not isinstance(value, (bool, np.bool_)) and np.isfinite(value)


def _validated_schema(schema):
    if not isinstance(schema, dict) or not isinstance(schema.get("signals"), dict):
        raise ValueError("schema.signals must be a dictionary")
    if type(schema.get("allow_extra_signals", True)) is not bool:
        raise ValueError("allow_extra_signals must be bool")
    for name, spec in schema["signals"].items():
        if not isinstance(name, str) or not name or not isinstance(spec, dict):
            raise ValueError("invalid signal schema")
        shape = spec.get("shape")
        if not isinstance(shape, list) or any(type(n) is not int or n < 1 for n in shape):
            raise ValueError("shape must be a list of positive dimensions")
        if spec.get("dtype") not in ("float", "int", "bool") or type(spec.get("required", True)) is not bool:
            raise ValueError("invalid dtype or required flag")
        for key in ("unit", "frame"):
            if key in spec and not isinstance(spec[key], str):
                raise ValueError("unit/frame must be strings")
        for key in ("min", "max"):
            if key in spec and not _number(spec[key]):
                raise ValueError("bounds must be finite numbers")
        if "min" in spec and "max" in spec and spec["min"] > spec["max"]:
            raise ValueError("min exceeds max")
        missing = spec.get("max_missing_fraction", 0)
        if not _number(missing) or not 0 <= missing <= 1:
            raise ValueError("missing fraction must be in [0,1]")


def validate_episodes(episodes, schema):
    if not isinstance(episodes, list):
        raise ValueError("episodes must be a list")
    _validated_schema(schema)
    issues = []

    def emit(index, path, code):
        issues.append({"episode": index, "path": path, "code": code})

    for index, episode in enumerate(episodes):
        if not isinstance(episode, dict):
            emit(index, "", "type")
            continue
        times = episode.get("timestamps")
        if not isinstance(times, list):
            emit(index, "timestamps", "type")
            continue
        count = len(times)
        if count == 0:
            emit(index, "timestamps", "empty")
        for t, value in enumerate(times):
            if not _number(value):
                emit(index, f"timestamps[{t}]", "nonfinite")
            elif t > 0 and _number(times[t - 1]) and value <= times[t - 1]:
                emit(index, f"timestamps[{t}]", "nonmonotonic")
        signals = episode.get("signals")
        if not isinstance(signals, dict):
            emit(index, "signals", "type")
            continue
        if not schema.get("allow_extra_signals", True):
            for name in signals:
                if name not in schema["signals"]:
                    emit(index, f"signals.{name}", "unexpected")
        for name, spec in schema["signals"].items():
            path = f"signals.{name}"
            if name not in signals:
                if spec.get("required", True):
                    emit(index, path, "missing")
                continue
            signal = signals[name]
            if not isinstance(signal, dict):
                emit(index, path, "type")
                continue
            for key in ("unit", "frame"):
                if key in spec and signal.get(key) != spec[key]:
                    emit(index, f"{path}.{key}", "metadata")
            values = signal.get("values")
            if not isinstance(values, list):
                emit(index, f"{path}.values", "type")
                continue
            if len(values) != count:
                emit(index, f"{path}.values", "length")
                continue
            missing = sum(row is None for row in values)
            if count and missing / count > spec.get("max_missing_fraction", 0):
                emit(index, f"{path}.values", "missing_fraction")
            for t, row in enumerate(values):
                if row is None:
                    continue
                row_path = f"{path}.values[{t}]"
                try:
                    array = np.asarray(row)
                except (ValueError, TypeError):
                    emit(index, row_path, "shape")
                    continue
                if array.shape != tuple(spec["shape"]):
                    emit(index, row_path, "shape")
                    continue
                kinds = {"float": "fiu", "int": "iu", "bool": "b"}[spec["dtype"]]
                if array.dtype.kind not in kinds:
                    emit(index, row_path, "dtype")
                    continue
                if not np.isfinite(array).all():
                    emit(index, row_path, "nonfinite")
                elif ("min" in spec and np.any(array < spec["min"])) or ("max" in spec and np.any(array > spec["max"])):
                    emit(index, row_path, "range")
    return sorted(issues, key=lambda x: (x["episode"], x["path"], x["code"]))
