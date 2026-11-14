# Worked examples

### A frequent easy task hides a failed hard task

~~~python
records = [("expert","easy",True)]*9 + [("expert","hard",False)]
quality_performance(records)
# {"by_slice":[("expert","easy",9,9,1.0),("expert","hard",1,0,0.0)],
#  "by_quality":[("expert",10,9,0.9,0.5)]}
~~~

Pooled success is9/10. Equal weighting of the two task rates gives(1+0)/2=0.5.

### Separate quality conditions

~~~python
quality_performance([("mixed","lift",False),("expert","lift",True),
                     ("mixed","lift",True)])
# {"by_slice":[("expert","lift",1,1,1.0),("mixed","lift",2,1,0.5)],
#  "by_quality":[("expert",1,1,1.0,1.0),("mixed",2,1,0.5,0.5)]}
~~~

Quality labels define separate experiment groups even when task labels match.

These examples use original synthetic fixtures. Hidden tests will exercise the same documented rules with different inputs.

