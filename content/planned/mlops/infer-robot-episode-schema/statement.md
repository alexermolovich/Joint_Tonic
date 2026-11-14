# Infer a Schema from Robot Episodes

Implement:

~~~python
def infer_episode_schema(episodes: list[dict]) -> dict[str, dict]:
    ...
~~~

episodes is a Python list of at most1,000 dictionaries. Each dictionary has at most128 signal-name keys; a name matches ASCII [a-z][a-z0-9_-]{0,63}. Empty episodes and an empty collection are valid. Each present signal maps to a dictionary with exactly values, unit, frame.

values is a finite NumPy float64 array(T,D), with 1<=T<=10,000,1<=D<=128 and abs(values)<=1e6. Total scalar entries across every input signal occurrence are at most2,000,000. Arrays may be noncontiguous. unit and frame are strings matching ASCII [a-z][a-z0-9_/-]{0,63}. They are provided metadata, not inferred units. Every occurrence of the same signal must have equal D, unit and frame; disagreement is ValueError. Sample counts T may differ across signals and episodes.

For each observed name return exactly:
- shape: the Python tuple (D,).
- unit and frame: the supplied strings.
- minimum and maximum: new float64 arrays(D,), the channel-wise extrema across all occurrences and rows.
- required: a Python bool, true exactly when that signal appears in every episode.

Return a dictionary keyed by signal name; dictionary insertion order is not graded. No aliases with input arrays or between returned minimum/maximum arrays; preserve all inputs. Empty collection returns {}, as does a collection of empty dictionaries. Every malformed container, record, identifier, dtype, bound or metadata inconsistency raises ValueError. No NaNs, implicit interpolation, categorical inference, filesystem access or internal randomness.

## Worked examples

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

## Source and scope

The paper motivates proposing schemas from observed data and reviewing them before enforcement. This numeric robot-signal schema and range policy are original; observed extrema are not hardware limits or a guarantee about unseen data. [Primary source](https://research.google/pubs/data-validation-for-machine-learning/).
