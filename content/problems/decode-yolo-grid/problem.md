# Decode YOLO Grid Predictions

A detector emits numbers relative to a grid. Your robot's downstream perception pipeline expects image-space boxes with explicit class IDs and scores. Implement `decode_yolo(predictions, image_size, score_threshold=0.25)` for the teaching codec below.

## Prediction contract

`predictions` is a finite real NumPy-compatible tensor with shape `(Sy,Sx,B,5+C)`, where all grid sizes, B, and C are positive. Its channels are:

| Channel | Meaning | Unit/range |
|---|---|---|
| 0, 1 | center offsets `tx,ty` inside the cell | cell fractions, `[0,1]` |
| 2, 3 | box width `w`, height `h` | direct fractions of full image size, `[0,1]` |
| 4 | objectness | `[0,1]` |
| 5 onward | per-box class probabilities | each independently in `[0,1]` |

Class probabilities need not sum to one. Width and height are **direct sizes**: do not exponentiate or square them. This original teaching layout is inspired by YOLO v1's grid formulation and deliberately differs from its shared-per-cell class layout and from other YOLO versions.

`image_size=(width,height)` contains positive integers, excluding booleans. `score_threshold` is a finite real scalar in `[0,1]`.

## Required decoding

For cell `(row,col)`, convert its center to pixels using `cx=(col+tx)*width/Sx` and `cy=(row+ty)*height/Sy`. Pixel width is `w*width`; height is `h*height`. Convert center/size to `xyxy` and clip each coordinate to `[0,width]` or `[0,height]` respectively. Skip boxes with zero clipped area.

For **each class**, emit a detection when `objectness * class_probability >= score_threshold`. A box can therefore emit multiple class detections. Do not apply NMS here.

Return a list of dictionaries:

```python
{"box": [x1, y1, x2, y2], "class_id": 0, "score": 0.6}
```

Box values and score must be Python floats; class ID a Python int. Sort by descending score. Equal scores preserve row, then column, then box, then class traversal order. Return `[]` if nothing survives. Preserve the input. Raise `ValueError` on malformed shape, nonfinite/complex/out-of-range values, invalid size, or invalid threshold.

## Example 1: one cell

```python
predictions = np.array([[[[.5,.5,.4,.5,.8,.75]]]])
decode_yolo(predictions, (100,80))
# [{"box":[30.,20.,70.,60.], "class_id":0, "score":.6}]
```

The center is `(50,40)`, dimensions `(40,40)`, and score is `.8*.75`.

## Example 2: multiple classes and filtering

```python
predictions = np.array([[[[.5,.5,.4,.5,.8,.75,.5]]]])
decode_yolo(predictions, (100,80), .5)
# [{"box":[30.,20.,70.,60.], "class_id":0, "score":.6}]
```

Class 1 has score `.4`, so it is filtered. At threshold `.4`, both class records are retained.

## Constraints and hints

`1<=Sy,Sx<=32`, `1<=B<=4`, `1<=C<=20`. The cell count scales the center offset; the **image size** scales the width/height. Keep the codec version together with the exported model so inference uses the same convention as training.
