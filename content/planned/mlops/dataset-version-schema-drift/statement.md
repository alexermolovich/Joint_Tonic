# Detect Dataset-Version and Schema Drift

Implement dataset_contract_drift(expected: dict, observed: dict) -> list[tuple[str,str,str]].

Each snapshot is a dictionary of0–128 dataset IDs. IDs, versions and feature names are strings matching ASCII [a-z][a-z0-9_-]{0,63}. Each dataset maps to exactly {"version":version_id,"features":feature_dict}; features contains1–128 names.

A feature descriptor is a tuple(dtype,shape,unit,frame):
- dtype is exactly one string float32,float64,int64,bool.
- shape is a Python tuple of0–4 built-in non-bool positive int dimensions, each<=10000; () is scalar. It describes one sample, not a batch or episode length.
- unit and frame are strings matching ASCII [a-z][a-z0-9_/-]{0,63}; these are declared labels, not converted or inferred.
All fields of both snapshots are validated before reporting, including an unexpected dataset.

Return sorted tuples(dataset_id,feature_name,reason):
- Dataset present only in expected: ("dataset","", "missing_dataset"), using its actual ID. Present only in observed: unexpected_dataset. Do not also emit all its feature changes.
- Shared dataset with different version string: feature_name="" and reason version.
- Shared dataset, feature only in expected: reason missing_feature; only in observed: unexpected_feature.
- Shared feature: emit one tuple for each unequal descriptor field, reason dtype,shape,unit or frame. Multiple changes on the same feature are all reported.

Sort by(dataset_id,feature_name,reason), all ASCII. Empty snapshots are valid; equal snapshots return[]. Preserve inputs. Malformed containers, fields, tuples, types, identifiers or bounds raise ValueError. Schema differences are reported regardless of whether the dataset version changed. A version difference alone is not assumed incompatible, and this function performs no migration or safety decision.

## Worked examples

### Same shape, changed physical meaning

~~~python
expected={"robot_data":{"version":"v1","features":{"pose":("float64",(3,),"m","base")}}}
observed={"robot_data":{"version":"v2","features":{"pose":("float64",(3,),"cm","tool")}}}
dataset_contract_drift(expected,observed)
# [("robot_data","","version"),("robot_data","pose","frame"),
#  ("robot_data","pose","unit")]
~~~

Equal dtype and shape do not erase changed units or coordinate frames.

### A replaced feature and a new dataset

~~~python
expected={"a":{"version":"v1","features":{"x":("float32",(),"m","base")}}}
observed={"a":{"version":"v1","features":{"y":("float32",(),"m","base")}},
          "b":{"version":"v1","features":{"z":("bool",(),"unitless","none")}}}
dataset_contract_drift(expected,observed)
# [("a","x","missing_feature"),("a","y","unexpected_feature"),
#  ("b","","unexpected_dataset")]
~~~

Dataset b gets one dataset-level issue; its feature is not redundantly expanded.

## Source and scope

Open X-Embodiment motivates preserving heterogeneous data meaning and reporting cross-embodiment results. This bounded deterministic interface is an original teaching decomposition, not the full RT-X model, dataset tooling or experimental protocol. [Primary source](https://arxiv.org/abs/2310.08864).

