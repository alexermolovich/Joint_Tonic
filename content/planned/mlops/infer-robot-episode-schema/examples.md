# Worked examples

### Required joints and optional force

~~~python
episodes = [
 {"joints":{"values":np.array([[0.,2.],[1.,4.]]),"unit":"rad","frame":"robot"},
  "force":{"values":np.array([[5.]]),"unit":"n","frame":"tool"}},
 {"joints":{"values":np.array([[-1.,3.]]),"unit":"rad","frame":"robot"}}
]
infer_episode_schema(episodes)
# {"joints":{"shape":(2,), "unit":"rad","frame":"robot",
#            "minimum":array([-1.,2.]),"maximum":array([1.,4.]),"required":True},
#  "force":{"shape":(1,), "unit":"n","frame":"tool",
#           "minimum":array([5.]),"maximum":array([5.]),"required":False}}
~~~

Extrema are per channel. force appears in one of two episodes, so it is optional in this proposal.

### An empty episode changes presence, not range

~~~python
episodes = [{}, {"speed":{"values":np.array([[2.],[4.]]),
                         "unit":"m/s","frame":"base"}}]
infer_episode_schema(episodes)
# {"speed":{"shape":(1,), "unit":"m/s","frame":"base",
#           "minimum":array([2.]),"maximum":array([4.]),"required":False}}
~~~

No value is invented for the empty episode. infer_episode_schema([]) returns {}.

These examples use original synthetic fixtures. Hidden tests will exercise the same documented rules with different inputs.
