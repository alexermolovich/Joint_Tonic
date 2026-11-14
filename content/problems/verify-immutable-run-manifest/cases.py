from copy import deepcopy
import hashlib


EMPTY="e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"


def manifest():
    return {"artifact_sha256":{"weights":EMPTY},"environment":{"python":"3.12.3"},"seed":7}


def invalid(call):
    try: call()
    except ValueError: return
    raise AssertionError("Expected ValueError")


def matching(m):
    assert m.verify_run_manifest(manifest(),{"weights":b""},{"python":"3.12.3"},7)==[]


def mismatched(m):
    assert m.verify_run_manifest(manifest(),{"weights":b"x","extra":b""},{"python":"3.11.0"},8)==[("artifact/extra","unexpected"),("artifact/weights","digest_mismatch"),("environment/python","version_mismatch"),("seed","mismatch")]


def missing(m):
    assert m.verify_run_manifest(manifest(),{}, {},7)==[("artifact/weights","missing"),("environment/python","missing")]


def exact_bytes_and_versions(m):
    payload=b"\x00\r\n\xff";doc={"artifact_sha256":{"data":hashlib.sha256(payload).hexdigest()},"environment":{"runtime":"3.12.3+cpu","seed_impl":"v1"},"seed":2**32-1}
    assert m.verify_run_manifest(doc,{"data":payload},{"runtime":"3.12.3+cpu","seed_impl":"v1"},2**32-1)==[]
    assert m.verify_run_manifest(doc,{"data":payload},{"runtime":"3.12.3","seed_impl":"v1","extra":"x"},2**32-1)==[("environment/extra","unexpected"),("environment/runtime","version_mismatch")]


def malformed(m):
    base=manifest()
    for doc,art,env,seed in [(None,{}, {},7),({**base,"extra":1},{},{},7),({**base,"artifact_sha256":{}},{},{},7),({**base,"artifact_sha256":{"a":"A"*64}},{},{},7),({**base,"environment":{}},{},{},7),({**base,"seed":True},{},{},7),(base,{"weights":bytearray()}, {},7),(base,{"bad/name":b""},{},7),(base,{},{"python":"3.*"},7),(base,{},{"python":False},7),(base,{}, {},False),(base,{}, {},10**1000)]:
        invalid(lambda: m.verify_run_manifest(doc,art,env,seed))
    invalid(lambda: m.verify_run_manifest(base,{"a"+str(i):b"" for i in range(129)},{},7))
    invalid(lambda: m.verify_run_manifest(base,{},{"a"+str(i):"1" for i in range(33)},7))


def byte_budget(m):
    payload=b"x"*16777216;doc=manifest();doc["artifact_sha256"]["weights"]=hashlib.sha256(payload).hexdigest()
    assert m.verify_run_manifest(doc,{"weights":payload},{"python":"3.12.3"},7)==[]
    invalid(lambda: m.verify_run_manifest(doc,{"weights":payload,"other":b"x"},{"python":"3.12.3"},7))


def storage(m):
    args=(manifest(),{"weights":b"x"},{"python":"3.12.3"},7);saved=deepcopy(args);out=m.verify_run_manifest(*args)
    assert out==[("artifact/weights","digest_mismatch")] and args==saved and type(out) is list and type(out[0]) is tuple


TESTS=[("Matching run preflight","public",matching),("Concrete mismatch reasons","public",mismatched),("Missing inputs","public",missing),
       ("Raw bytes and exact versions","hidden",exact_bytes_and_versions),("Malformed contracts","hidden",malformed),
       ("Declared total-byte limit","hidden",byte_budget),("Immutable inputs and exact output","hidden",storage)]
