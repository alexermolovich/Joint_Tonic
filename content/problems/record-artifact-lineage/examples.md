# Worked examples

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

These examples use original synthetic fixtures. Hidden tests will exercise the same documented rules with different inputs.
