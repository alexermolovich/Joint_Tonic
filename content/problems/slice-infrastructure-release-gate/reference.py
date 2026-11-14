import re


def release_rejections(required, evidence, candidate, now_ms, max_age_ms):
    def check_id(value):
        return isinstance(value, str) and re.fullmatch(r"(slice|infra)/[a-z][a-z0-9_-]{0,63}", value) is not None
    def version(value):
        return isinstance(value, str) and re.fullmatch(r"[a-z][a-z0-9_-]{0,63}", value) is not None
    def timestamp(value):
        return type(value) is int and 0 <= value <= 2**63 - 1
    if not isinstance(required, list) or not 1 <= len(required) <= 10000 or any(not check_id(v) for v in required):
        raise ValueError("Invalid required checks")
    if not isinstance(evidence, dict) or len(evidence) > 10000 or not version(candidate):
        raise ValueError("Invalid evidence or candidate")
    if not timestamp(now_ms) or not timestamp(max_age_ms):
        raise ValueError("Invalid time")
    for name, record in evidence.items():
        if not check_id(name) or not isinstance(record, tuple) or len(record) != 3:
            raise ValueError("Invalid evidence record")
        tested, completed, status = record
        if not version(tested) or not timestamp(completed) or not isinstance(status, str) or status not in ("pass", "fail"):
            raise ValueError("Invalid evidence fields")
    rejected = []
    for name in sorted(set(required)):
        if name not in evidence:
            reason = "missing"
        else:
            tested, completed, status = evidence[name]
            if tested != candidate:
                reason = "wrong_version"
            elif completed > now_ms:
                reason = "future"
            elif now_ms - completed > max_age_ms:
                reason = "stale"
            elif status == "fail":
                reason = "failed"
            else:
                continue
        rejected.append((name, reason))
    return rejected
