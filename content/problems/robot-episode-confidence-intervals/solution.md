# Solution explanation

Compute each metric’s mean and centered sample variance across complete episodes using E-1. Divide variance by E, take its square root, then apply the supplied critical multiplier without clipping. Work O(EM), output O(M), intermediate O(EM). Assumptions behind the multiplier remain explicit.
