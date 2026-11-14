# Solution explanation

Validate the complete task/event sets, collapse identical attempt evidence, and reject conflicts. For each task, check committed success first, then initial pending state, attempt exhaustion, replay prohibition and retry in that order. Output lexical rows without executing any task. Work O(E+T log T), storage O(E+T).
