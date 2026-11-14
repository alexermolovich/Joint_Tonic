# Solution explanation

Validate only observed pixel values, form one MSE per observed frame, and accumulate counts and errors by horizon. Divide supported horizons and the global total separately. Work O(BTHWC), memory O(BTHWC) for the simple promoted-input implementation.
