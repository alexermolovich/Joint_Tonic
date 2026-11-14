# Solution explanation

Validate all arrays and per-axis parameter bounds, including on empty batches. Broadcast mass and damping over batch rows, calculate acceleration, then velocity and position in order. Return independent arrays. Work and storage O(BD).
