# Progressive hints

## Hint 1

Reuse the pinhole projection convention, but do not require an image-bounds test when no image size is supplied.

## Hint 2

Subtract prediction from measurement in the stated order. Preserve NaNs for points behind the camera.

## Hint 3

Compute one squared 2D distance per valid point before averaging. Return no RMSE value when the valid set is empty; zero would imply perfect evidence.
