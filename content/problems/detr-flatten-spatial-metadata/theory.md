# Flatten Spatial Features with Position and Padding Metadata

## Intuition

Flattening is bookkeeping with physical consequences: a feature vector, its position and its padding flag must continue to refer to the same image location. Keep content and positional tokens separate so the downstream attention layer decides how to combine them.

## Mathematics and physical meaning

Let $F\in\mathbb R^{B\times H\times W\times D}$ be dimensionless features, $P\in\mathbb R^{H\times W\times D}$ positional vectors and $V\in\{0,1\}^{B\times H\times W}$ validity. Row $r$ increases downward and column $c$ rightward. The row-major token index is
$$j=rW+c,\qquad 0\le j<HW.$$
The two token arrays have shape $(B,HW,D)$:
$$X_{b,j,:}=V_{b,r,c}F_{b,r,c,:},\qquad Z_{b,j,:}=V_{b,r,c}P_{r,c,:}.$$
Padding is $\neg V$ flattened in the same order. The coordinate table $(HW,2)$ stores $(r,c)$ even for invalid slots. Multiplication here denotes a selection mask; it does not excuse nonfinite masked inputs. No resizing, camera projection or embedding addition occurs.

## Visual trace

| Pixel `(row,col)` | Slot | Content | Position | Padding |
|---|---:|---:|---:|---|
| `(0,0)` | 0 | 2 | 10 | false |
| `(0,1)` | 1 | 0 | 0 | true |

This static trace is also a complete text alternative; it requires no animation.

## Worked examples

**Example 1.** For a one-row grid, features are `[2, 4]`, positions `[10, 20]` and validity `[True, False]`, each with one channel. Output tokens `[2, 0]`, positional tokens `[10, 0]`, padding `[False, True]`, coordinates `[[0, 0],[0, 1]]` (batch/channel dimensions retained).

**Example 2.** Mark both pixels invalid. Output content and positional arrays are zero, padding is `[True, True]`, and coordinates remain `[[0, 0],[0, 1]]`.

## Why this matters on a robot

A detector can attend to the wrong location if position vectors use column-major order while features use row-major order. Padded regions must stay masked even when their zero features resemble a real dark region.

## Sources and prerequisites

[Primary paper](https://arxiv.org/abs/2005.12872). This explanation, table and code are original.

Prerequisites: comfortable reading the declared array shapes and the relevant physical coordinate convention. This task teaches the robotics/model component, not Python syntax.
