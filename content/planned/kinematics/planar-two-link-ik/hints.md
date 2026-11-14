# Progressive hints

## Hint 1

Check the target distance against the arm's inner and outer reachable radii before computing angles.

## Hint 2

The triangle determines the elbow cosine. Select the positive elbow branch, then subtract the internal link-offset angle from the target bearing.

## Hint 3

Run forward kinematics on every returned answer. Treat singular extension/folding as reachable boundary cases, and handle the equal-length origin convention explicitly.
