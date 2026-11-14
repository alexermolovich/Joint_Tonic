# Solution explanation

Map supplied axis IDs to their original positions. Sum successes and trials per pair, including repeated evidence, into independent int64 arrays. Mark positive trial counts observed and divide only there; leave unobserved rates NaN. This pools counts rather than averaging rates. Work is O(R+ST), storage O(ST), where R is record count and S,T axis sizes.
