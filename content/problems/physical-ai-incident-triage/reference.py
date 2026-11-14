import re


def triage_events(events, now_ms, window_ms):
    priority = {"safety_stop": 0, "sensor_stale": 1, "deadline_miss": 1, "model_error": 2}
    def timestamp(value):
        return type(value) is int and 0 <= value <= 2**63 - 1
    if not isinstance(events, list) or len(events) > 100000 or not timestamp(now_ms) or not timestamp(window_ms):
        raise ValueError("Invalid events or clock")
    for event in events:
        if not isinstance(event, tuple) or len(event) != 3:
            raise ValueError("Invalid event record")
        time, component, kind = event
        if not timestamp(time) or time > now_ms:
            raise ValueError("Invalid event timestamp")
        if not isinstance(component, str) or re.fullmatch(r"[a-z][a-z0-9_-]{0,63}", component) is None:
            raise ValueError("Invalid component ID")
        if not isinstance(kind, str) or kind not in priority:
            raise ValueError("Invalid event kind")
    groups = {}
    for time, component, kind in events:
        if time < now_ms - window_ms:
            continue
        rank, count, first = groups.get(component, (2, 0, time))
        groups[component] = (min(rank, priority[kind]), count + 1, min(first, time))
    ordered = sorted(groups, key=lambda name: (groups[name][0], groups[name][2], name))
    return [(name, "P" + str(groups[name][0]), groups[name][1], groups[name][2]) for name in ordered]
