import math
import re
import numpy as np

_NAME = re.compile(r"[a-z][a-z0-9_-]{0,63}", re.ASCII)

def _name(value):
    return isinstance(value, str) and _NAME.fullmatch(value) is not None

def feature_anomalies(records, schema):
    if not isinstance(schema, dict) or not 1 <= len(schema) <= 128:
        raise ValueError("schema")
    fields = {"kind", "shape", "required", "minimum", "maximum", "domain"}
    for name, spec in schema.items():
        if not _name(name) or not isinstance(spec, dict) or set(spec) != fields:
            raise ValueError("feature schema")
        kind, shape = spec["kind"], spec["shape"]
        if not isinstance(kind, str) or kind not in ("numeric", "categorical"):
            raise ValueError("kind")
        if not isinstance(shape, tuple) or len(shape) > 4:
            raise ValueError("shape")
        if any(type(d) is not int or not 1 <= d <= 128 for d in shape) or math.prod(shape) > 1024:
            raise ValueError("dimensions")
        if type(spec["required"]) is not bool:
            raise ValueError("required")
        if kind == "numeric":
            low, high = spec["minimum"], spec["maximum"]
            if any(type(v) not in (int, float) or not -1e6 <= v <= 1e6 for v in (low, high)):
                raise ValueError("numeric bounds")
            if low > high or spec["domain"] is not None:
                raise ValueError("numeric schema")
        else:
            domain = spec["domain"]
            if spec["minimum"] is not None or spec["maximum"] is not None:
                raise ValueError("categorical bounds")
            if not isinstance(domain, tuple) or not 1 <= len(domain) <= 128:
                raise ValueError("domain")
            if any(not _name(x) for x in domain) or len(set(domain)) != len(domain):
                raise ValueError("domain labels")
    if not isinstance(records, list) or len(records) > 1000:
        raise ValueError("records")
    total = 0
    for record in records:
        if not isinstance(record, dict) or len(record) > 128 or any(not _name(x) for x in record):
            raise ValueError("record")
        for value in record.values():
            if isinstance(value, np.ndarray):
                total += value.size
                if value.size > 1024 or total > 1000000:
                    raise ValueError("workload")
    issues = []
    for index, record in enumerate(records):
        for name in sorted(record.keys() | schema.keys()):
            if name not in schema:
                code = "unexpected"
            elif name not in record:
                if not schema[name]["required"]:
                    continue
                code = "missing"
            else:
                value, spec = record[name], schema[name]
                if not isinstance(value, np.ndarray):
                    code = "type"
                elif value.shape != spec["shape"]:
                    code = "shape"
                elif (spec["kind"] == "numeric" and value.dtype != np.float64) or (spec["kind"] == "categorical" and value.dtype.kind != "U"):
                    code = "dtype"
                elif spec["kind"] == "numeric":
                    if not np.isfinite(value).all():
                        code = "nonfinite"
                    elif ((value < spec["minimum"]) | (value > spec["maximum"])).any():
                        code = "range"
                    else:
                        continue
                elif not np.isin(value, spec["domain"]).all():
                    code = "domain"
                else:
                    continue
            issues.append((index, name, code))
    return issues

