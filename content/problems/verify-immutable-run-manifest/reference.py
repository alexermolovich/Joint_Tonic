import hashlib
import re


def verify_run_manifest(manifest, artifacts, environment, seed):
    def identifier(value):
        return isinstance(value, str) and re.fullmatch(r"[a-z][a-z0-9_-]{0,63}", value) is not None
    def seed_ok(value):
        return type(value) is int and 0 <= value <= 2**32 - 1
    def versions(mapping, minimum):
        if not isinstance(mapping, dict) or not minimum <= len(mapping) <= 32:
            raise ValueError("Invalid environment mapping")
        for name, version in mapping.items():
            if not identifier(name) or not isinstance(version, str) or re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._+:-]{0,127}", version) is None:
                raise ValueError("Invalid environment name/version")
    if not isinstance(manifest, dict) or set(manifest) != {"artifact_sha256", "environment", "seed"}:
        raise ValueError("Invalid manifest")
    expected = manifest["artifact_sha256"]
    if not isinstance(expected, dict) or not 1 <= len(expected) <= 128:
        raise ValueError("Invalid expected artifacts")
    for name, digest in expected.items():
        if not identifier(name) or not isinstance(digest, str) or re.fullmatch(r"[0-9a-f]{64}", digest) is None:
            raise ValueError("Invalid artifact name/digest")
    versions(manifest["environment"], 1)
    versions(environment, 0)
    if not seed_ok(manifest["seed"]) or not seed_ok(seed):
        raise ValueError("Invalid seed")
    if not isinstance(artifacts, dict) or len(artifacts) > 128:
        raise ValueError("Invalid observed artifacts")
    total = 0
    for name, payload in artifacts.items():
        if not identifier(name) or type(payload) is not bytes:
            raise ValueError("Expected named bytes")
        total += len(payload)
        if total > 16777216:
            raise ValueError("Artifact byte budget exceeded")
    discrepancies = []
    for name in expected.keys() | artifacts.keys():
        if name not in expected:
            reason = "unexpected"
        elif name not in artifacts:
            reason = "missing"
        elif hashlib.sha256(artifacts[name]).hexdigest() != expected[name]:
            reason = "digest_mismatch"
        else:
            continue
        discrepancies.append(("artifact/" + name, reason))
    declared = manifest["environment"]
    for name in declared.keys() | environment.keys():
        if name not in declared:
            reason = "unexpected"
        elif name not in environment:
            reason = "missing"
        elif environment[name] != declared[name]:
            reason = "version_mismatch"
        else:
            continue
        discrepancies.append(("environment/" + name, reason))
    if seed != manifest["seed"]:
        discrepancies.append(("seed", "mismatch"))
    return sorted(discrepancies)
