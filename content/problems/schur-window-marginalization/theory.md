# Marginalize a Visual-Inertial Window with a Schur Complement

## Intuition

Removing old states should preserve what their measurements tell us about the states still being optimized. Algebraically minimize the quadratic over the removed variables instead of dropping their rows and columns.

## Mathematics and conventions

For dimensionless state blocks $x_a,x_b$, consider

$$E(x)=\tfrac12x^\top Hx-b^\top x,\qquad Hx=b.$$

At fixed retained $x_a$, stationarity in the removed coordinates gives $x_b=H_{bb}^{-1}(b_b-H_{ba}x_a)$. Substituting yields

$$H'=H_{aa}-H_{ab}H_{bb}^{-1}H_{ba},\qquad b'=b_a-H_{ab}H_{bb}^{-1}b_b,$$
$$E_{reduced}(x_a)=\tfrac12x_a^\top H'x_a-b'^\top x_a-\tfrac12b_b^\top H_{bb}^{-1}b_b.$$

Inverse notation describes the mathematics; implement linear solves. The positive-definite conditioning contract makes both the eliminated block and Schur complement solvable. This retains the current quadratic's information, including correlations, but cannot relinearize discarded nonlinear factors.

## Visual computation trace

| Coupled H=[[2,1],[1,2]], rhs=[1,0] | Value |
| --- | --- |
| Removed-state relation | xb=-xa/2 |
| Reduced curvature | 2-1*(1/2)*1=1.5 |
| Retained optimum | xa=1/1.5=2/3 |
| Reconstructed removed optimum | xb=-1/3 |

## Worked examples

1. H=`[[2.,1.],[1.,2.]]`, rhs=`[1.,0.]`, retained=1: reduced normal `[[1.5]]`, reduced rhs `[1.]`, retained step `[2/3]`, removed step `[-1/3]`, constant shift 0.
2. H=diag(2,4), rhs=`[2.,8.]`, retained=1: reduced normal `[[2.]]`, reduced rhs `[2.]`, steps `[1.]` and `[2.]`, constant shift -8.

## Why this matters on a robot

Simply deleting old variables overstates or discards information depending on their coupling. A marginalized prior is tied to its linearization; reusing it after large state changes without the appropriate coordinate treatment can make an estimator inconsistent.

## Source and prerequisites

[Primary paper](https://arxiv.org/abs/1708.03852). Read the typed contract and coordinate conventions above.

This static explanation has no animation; its tables and shape traces are the text equivalent of the computation.
