import re

_NAME = re.compile(r"[a-z][a-z0-9_-]{0,63}", re.ASCII)

def sensor_metadata_skew(expected, observed, max_delta_ns):
    if type(max_delta_ns) is not int or not 0 <= max_delta_ns <= 2**63-1:
        raise ValueError("max_delta_ns")
    for records in (expected, observed):
        if not isinstance(records, dict) or len(records) > 1000:
            raise ValueError("records")
        for sensor, record in records.items():
            if not isinstance(sensor, str) or not _NAME.fullmatch(sensor):
                raise ValueError("sensor")
            if not isinstance(record, tuple) or len(record) != 2:
                raise ValueError("metadata tuple")
            stamp, calibration = record
            if type(stamp) is not int or not 0 <= stamp <= 2**63-1:
                raise ValueError("timestamp")
            if not isinstance(calibration, str) or not _NAME.fullmatch(calibration):
                raise ValueError("calibration")
    result = []
    for sensor in expected.keys() | observed.keys():
        if sensor not in observed:
            result.append((sensor, "missing"))
        elif sensor not in expected:
            result.append((sensor, "unexpected"))
        else:
            if expected[sensor][1] != observed[sensor][1]:
                result.append((sensor, "calibration"))
            if abs(expected[sensor][0] - observed[sensor][0]) > max_delta_ns:
                result.append((sensor, "timing"))
    return sorted(result)

