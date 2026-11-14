# Hints

1. Split off row0 before any reshape.
2. Move D to the channel axis for the interpolation operator.
3. Restore grid-row/grid-column order before joining the class position.
