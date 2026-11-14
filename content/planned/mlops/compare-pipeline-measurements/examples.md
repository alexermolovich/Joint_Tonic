# Worked examples

### Overlapping stages
`compare_pipeline_measurements([("r",0,10)],[("r","a",1,6),("r","b",4,8)])` returns `[("r",10,7,3,2)]`.

### No internal evidence
`compare_pipeline_measurements([("r",100,105)],[])` returns `[("r",5,0,5,0)]`.
