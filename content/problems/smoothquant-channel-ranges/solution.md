# Solution explanation

Reduce absolute activations over tokens and absolute weights over outputs. The two reductions meet at the shared input-channel axis C. Return maxima without a guard so zero channels remain distinguishable. Work O(NC+CD), extra output storage O(C).
