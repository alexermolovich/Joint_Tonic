# Evaluation and failure analysis

[Open the integration problem](/problems/smoothquant-calibrated-layer-integration). Run exposes the two documented scalar/zero-channel examples. Submit also checks an independent scalar pipeline oracle, calibration-only range statistics, float32 promotion, zero guards, nonzero-subnormal quantizer underflow, repeated-alpha tie behavior, preservation, invalid contracts and a case where minimum MSE disagrees with the absolute-error gate.

The outputs answer distinct questions: output_mse ranks supplied configurations; row_max_abs locates token regressions; accepted applies the explicit tolerance; selected_output preserves the actual quantized prediction. The selected index minimizes MSE across all candidates, even when another candidate alone passes the gate. A failed gate is evidence to inspect, not a reason to silently change the selection policy.

Failure-analysis exercise: introduce a large validation-only activation channel and explain why calibration scales must remain unchanged. Then compare two candidates whose average errors and worst-token errors rank differently. A layer-level pass cannot establish downstream VLM accuracy or safe robot actions.

The reference is tested in the local isolated worker. Starter code, a calibration-leak mutant and a gate-filter mutant are rejected. These tests establish the documented synthetic contract, not performance on the paper's model/data suite.
