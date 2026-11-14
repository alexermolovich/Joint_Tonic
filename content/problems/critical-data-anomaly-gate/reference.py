import re

_NAME = re.compile(r"[a-z][a-z0-9_-]{0,63}", re.ASCII)

def _name(value):
    return isinstance(value, str) and _NAME.fullmatch(value) is not None

def data_anomaly_gate(required_sources, checked_sources, anomalies):
    for sources, minimum in ((required_sources, 1), (checked_sources, 0)):
        if not isinstance(sources, list) or not minimum <= len(sources) <= 10000:
            raise ValueError("sources")
        if any(not _name(source) for source in sources):
            raise ValueError("source name")
    if not isinstance(anomalies, list) or len(anomalies) > 50000:
        raise ValueError("anomalies")
    checked, records = set(checked_sources), {}
    for entry in anomalies:
        if not isinstance(entry, tuple) or len(entry) != 3:
            raise ValueError("anomaly tuple")
        source, code, severity = entry
        if not _name(source) or not _name(code) or source not in checked:
            raise ValueError("unchecked source or code")
        if not isinstance(severity, str) or severity not in ("critical", "warning"):
            raise ValueError("severity")
        key = (source, code)
        if key in records and records[key] != severity:
            raise ValueError("conflicting severity")
        records[key] = severity
    blocking = sorted(key for key, severity in records.items() if severity == "critical")
    warnings = sorted(key for key, severity in records.items() if severity == "warning")
    missing = sorted(set(required_sources) - checked)
    return {"blocking": blocking, "warnings": warnings, "missing_sources": missing,
            "blocked": bool(blocking or missing)}

