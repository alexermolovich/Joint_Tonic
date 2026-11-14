# Worked examples

For both examples, the complete header is model_id="policy", artifacts={weights:"1"*64, preprocessing:"2"*64, action_decoder:"3"*64, runtime:"4"*64}, intended_embodiments=["fr3"], limitations="One room only". Add the metrics field specified below.

With valid model/artifact/embodiment/limitations fields and metrics=[{slice_id:"day", trials:10, successes:2}], required_slices=["day"] yields[]. Low performance is reported, not hidden by a schema error.

Same valid header, metrics=[{slice_id:"night", trials:0, successes:1}], required_slices=["day","night"] yields[("day","missing"),("night","invalid_success_count"),("night","no_trials")].
