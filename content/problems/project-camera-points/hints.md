# Progressive hints

## Hint 1

Read each row as camera-optical `(x,y,z)`: right, down, forward. The lateral ratios `x/z` and `y/z` become pixel displacements after multiplying by focal lengths.

## Hint 2

Allocate a pixel array filled with NaNs, then project only rows with `z > 1e-8`. A forward-facing point outside the image still receives calculated pixel coordinates; validity is a separate mask.

## Hint 3

Use half-open bounds for pixels: include zero and exclude width/height. Keep all three outputs aligned with the original row indices. Copy the depth column so downstream changes cannot modify the input points.
