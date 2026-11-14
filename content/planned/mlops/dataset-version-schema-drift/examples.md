# Worked examples

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

These examples use original synthetic fixtures. Hidden tests will exercise the same documented rules with different inputs.

