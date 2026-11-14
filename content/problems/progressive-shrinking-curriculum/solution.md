# Solution explanation

Validate ordered choices, construct the phase-dependent legal lists, then draw one local PCG64 (N,3) matrix. Always consume every column, even for a singleton axis, to preserve the declared replay rule. Gather each discrete choice by floor(u times list length). Work/output O(N); no global RNG change.
