# Solution explanation

Validate the ordered task list and each event. Keep a map from evaluation ID to its immutable evidence tuple, increment each new trial once, and divide successes only where counts are positive. Work O(E+K squared), storage O(E+K squared).
