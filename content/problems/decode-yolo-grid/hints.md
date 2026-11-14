# Progressive hints

## Hint 1

Separate the cell-relative center from the image-relative size. The cell column/row affects the center; the full image width/height scales the direct width/height channels.

## Hint 2

Convert center plus size into four corners, clip to image extents, and reject zero clipped area. Then evaluate `objectness × class_probability` separately for every class.

## Hint 3

Traverse rows, columns, boxes, then classes. An ordinary stable descending-score sort can preserve that traversal order for ties. Do not add NMS or a square/exponential size transform: those would change this explicitly declared teaching codec.
