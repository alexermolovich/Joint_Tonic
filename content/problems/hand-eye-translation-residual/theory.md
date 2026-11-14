# Solve a Small Hand-Eye Calibration Residual

## Intuition

Hand-eye calibration relates a camera rigidly attached to a robot to the robot’s own motion. If orientation is already known, each motion pair gives three linear constraints on the unknown mounting translation.

## Mathematics and physical meaning

Write $A_i=(R_{A_i},t_{A_i})$, $B_i=(R_{B_i},t_{B_i})$, and $X=(R_X,t_X)$. The translation blocks of $A_iX=XB_i$ give
$$R_{A_i}t_X+t_{A_i}=R_Xt_{B_i}+t_X.$$
Thus $C_it_X=d_i$ with $C_i=R_{A_i}-I_3$ and $d_i=R_Xt_{B_i}-t_{A_i}$. Stack $C\in\mathbb R^{3N\times3}$ and $d\in\mathbb R^{3N}$, then solve
$$\widehat t_X=\arg\min_t\|Ct-d\|_2^2,\qquad e_i=C_i\widehat t_X-d_i.$$
Translations and residuals are metres. Rank three is required for unique translation observability. Repeating only rotations around one axis cannot reveal translation along that axis.

## Visual trace

| Motion pair with R_X=I | Rotation A | Constraint on unknown t_X |
|---|---|---|
| 1 | 180° about x | y and z components |
| 2 | 180° about y | x and z components |
| Together | independent rotation axes | all three components observable |

This static table is also the text alternative; no animation is required.

## Worked examples

1. Let both A translations be zero, R_A1=diag(1,-1,-1), R_A2=diag(-1,1,-1), and R_X=I. Use B with the same respective rotations and translations `[0,-4,-6]`, `[-2,0,-6]`. Return t=`[1,2,3]` and zero residuals.
2. Same rotations with every A/B translation zero returns t=`[0,0,0]` and zero residuals. Repeating only the first rotation instead must raise ValueError.

## Why this matters on a robot

A numerical least-squares routine can return a vector even when mounting translation is unobservable. Inspecting rank prevents presenting that arbitrary vector as a calibration. Small translation residuals do not verify the supplied rotation or synchronization.

## Sources and prerequisites

Original pedagogical robotics component; no external data or paper reproduction claim.
