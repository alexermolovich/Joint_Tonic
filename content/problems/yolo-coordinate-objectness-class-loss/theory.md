# Compute YOLO Coordinate, Objectness, and Class Losses

## Intuition

One cell supervises geometry, localization confidence and class identity, but those losses apply to different subsets. The responsibility mask determines which box receives localization learning; other boxes still receive background-confidence penalties.

## Math and loss routing

Let $\mathcal O$ be occupied cells, $b_i$ the supplied responsible predictor, $p_i,t_i\in\mathbb R^4$ its predicted/target box, $c_{ib}$ confidence and $u_i$ supplied target IoU. Coordinates x,y are cell-relative; widths/heights are image fractions.
$$L_{\mathrm{coord}}=5\sum_{i\in\mathcal O}\left[\|p_{i,xy}-t_{i,xy}\|_2^2+\|\sqrt{p_{i,wh}}-\sqrt{t_{i,wh}}\|_2^2\right].$$
$$L_{\mathrm{obj}}=\sum_{i\in\mathcal O}(c_{i,b_i}-u_i)^2+\tfrac12\sum_{(i,b)\text{ nonresponsible}}c_{ib}^2,\qquad L_{\mathrm{class}}=\sum_{i\in\mathcal O}\|a_i-e_{y_i}\|_2^2.$$
Here $a_i\in\mathbb R^C$ is the predicted class-probability vector and $e_{y_i}$ a one-hot target. Total is the unaveraged sum; all terms are dimensionless.

| Prediction | Occupied/responsible | Empty or nonresponsible |
|---|---|---|
| Box coordinates | weighted squared error | ignored |
| Confidence | squared error to supplied IoU | half-weighted square to zero |
| Cell class | squared one-hot error | ignored for empty cell |

Width0.25 versus1 yields square-root difference0.5, squared0.25, weighted1.25. Confidences0.5 and0.2 give0.25+0.5×0.04=0.27; class errors0.2 in two channels add0.08. Total is1.60.

## Why this matters on a robot

Incorrect masks can teach background boxes to explain real objects or train classes on empty cells. Confidence in YOLO-v1 includes localization quality, so replacing the supplied IoU target with1 changes the objective. This component omits responsibility selection and optimization, while preserving their explicit inputs.

## Source and prerequisites

[Primary paper](https://arxiv.org/abs/1506.02640). [yolo-responsible-cell-targets](/problems/yolo-responsible-cell-targets)

This static explanation has no animation; its tables and shape traces are the text equivalent of the computation.
