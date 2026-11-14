def readiness_score(checks):
    categories = ("data", "model", "infrastructure", "monitoring")
    credits = {"none": 0.0, "manual": 0.5, "automated": 1.0}
    if not isinstance(checks, dict) or set(checks) != set(categories):
        raise ValueError("Expected exactly four readiness categories")
    totals = {}
    for category in categories:
        statuses = checks[category]
        if not isinstance(statuses, list) or len(statuses) > 7:
            raise ValueError("Expected at most seven checks per category")
        if any(not isinstance(status, str) or status not in credits for status in statuses):
            raise ValueError("Invalid evidence status")
        totals[category] = sum((credits[status] for status in statuses), 0.0)
    return {"categories": totals, "score": min(totals.values())}
