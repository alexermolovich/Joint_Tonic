# Worked examples

### Explain every failed requirement

~~~python
required = ["slice/night","infra/rollback","infra/runtime","slice/rain"]
evidence = {"slice/night":("v2",900,"pass"),
            "infra/rollback":("v1",990,"pass"),
            "infra/runtime":("v2",950,"fail")}
release_rejections(required,evidence,"v2",1000,100)
# [("infra/rollback","wrong_version"),("infra/runtime","failed"),
#  ("slice/rain","missing")]
~~~

Night evidence is exactly100ms old and passes. The rain slice has no evidence.

### Freshness, future data, and duplicate requirements

~~~python
required = ["slice/fog","infra/timing","slice/fog"]
evidence = {"slice/fog":("v3",99,"pass"),
            "infra/timing":("v3",201,"pass")}
release_rejections(required,evidence,"v3",200,100)
# [("infra/timing","future"),("slice/fog","stale")]
~~~

Fog evidence is101ms old. Duplicating the requirement creates no duplicate result.

These examples use original synthetic fixtures. Hidden tests will exercise the same documented rules with different inputs.
