# Record Dataset, Transform, Model, and Evaluator Lineage

Implement:

~~~python
def lineage_record(artifacts: dict[str, tuple[str, str]],
                   parents: dict[str, list[str]],
                   target: str) -> list[tuple[str, str, str]]:
    ...
~~~

artifacts maps artifact_id to an exact two-item tuple (kind, sha256). IDs match ASCII [a-z][a-z0-9_-]{0,63}. kind is one of dataset, transform, model, evaluator. sha256 is exactly64 lowercase hexadecimal characters. Different IDs may share a kind or digest.

parents must have exactly the same key set as artifacts. Its values are Python lists of declared artifact IDs consumed by that key. Duplicate parent IDs are ignored semantically. Require 1–10,000 artifacts, at most50,000 supplied parent references, and a declared target ID. Validate the entire graph as acyclic, including disconnected components and self-loops. No fixed ordering of artifact kinds is imposed.

Return the target plus all of its transitive ancestors as (artifact_id, kind, sha256) tuples, sorted by artifact ID. Do not include unrelated artifacts or downstream consumers. Shared ancestors appear once. An artifact with no parents returns its own row. Output order is lexical, not topological. Preserve inputs and return a fresh list.

All malformed types, IDs, digests, missing parent-map keys, unknown references, cycles or exceeded bounds raise ValueError. This function records supplied identities only; it reads no files, computes no artifact bytes and uses no clock or random sampling.

## Worked examples

### Preserve every ingredient of an evaluation

~~~python
artifacts = {"data":("dataset","1"*64), "norm":("transform","2"*64),
             "policy":("model","3"*64), "score":("evaluator","4"*64)}
parents = {"data":[], "norm":["data"], "policy":["data","norm"],
           "score":["policy","data"]}
lineage_record(artifacts,parents,"score")
# [("data","dataset","1"*64),("norm","transform","2"*64),
#  ("policy","model","3"*64),("score","evaluator","4"*64)]
~~~

The data artifact is reachable along several paths but has one row.

### Identical bytes do not merge artifact identities

~~~python
artifacts = {"a":("dataset","a"*64), "b":("dataset","a"*64),
             "model":("model","b"*64), "unused":("transform","c"*64)}
parents = {"a":[], "b":[], "model":["b","a","a"], "unused":[]}
lineage_record(artifacts,parents,"model")
# [("a","dataset","a"*64),("b","dataset","a"*64),("model","model","b"*64)]
~~~

a and b have distinct metadata identities despite matching digests. unused is not an ancestor.

## Source and scope

TFX motivates coordinating versioned pipeline artifacts. The graph schema and returned ancestry record are original teaching choices, not a universal TFX metadata API. Supplied digests are recorded but not verified against bytes in this component. [Primary source](https://research.google/pubs/tfx-a-tensorflow-based-production-scale-machine-learning-platform/).
