# Apply SE(3) Exponential and Logarithm Maps

Implement `se3_maps(tangent, transform)`.

Compute an SE(3) exponential and principal logarithm with explicit translation/rotation coupling.

`tangent` is float64 `(6,)`, ordered `[rho_x,rho_y,rho_z,phi_x,phi_y,phi_z]`. Rho is a translation tangent in meters, with norm<=1e6; phi is a rotation vector in radians, with norm<=pi-1e-4. `transform` is a proper float64 `(4,4)` rigid transform with translation in meters and principal rotation angle<=pi-1e-4. Validate rotation and homogeneous row at atol=1e-9, rtol=0. The two inputs are independent: neither must be the map of the other.

Return a dictionary with fresh float64 `exponential (4,4)=Exp(tangent)` and `logarithm (6,)=Log(transform)`. Write Omega=skew(phi), theta=norm(phi). Rotation is `I+(sin(theta)/theta)*Omega+((1-cos(theta))/theta**2)*Omega**2`. The translation is `V@rho`, where `V=I+((1-cos(theta))/theta**2)*Omega+((theta-sin(theta))/theta**3)*Omega**2`. Use continuous series limits at zero. For Log, recover the principal rotation vector, build its V, then solve `V@rho=translation`.

These right-handed maps define an increment; no pose composition, left/right update or interpolation is performed. The ambiguous pi branch and its immediate 1e-4-radian neighborhood are outside this bounded contract. Translation is generally not equal to rho when rotation is nonzero.

## Validation and runtime

All array arguments must be NumPy arrays with the stated rank and dtype: real arrays use float64, index arrays int64, masks bool. Real entries must be finite with absolute value at most 1e6 unless a tighter range is stated. All malformed types, shapes, ranges, or scalar arguments raise ValueError. Support noncontiguous arrays, preserve every input, and return fresh arrays (no input storage alias). CPU only; no implicit batch dimension. Comparisons use rtol=1e-6 and atol=1e-7. Fixtures are original synthetic data (CC0-1.0).

## Worked examples

1. Tangent `[1.,0.,0.,0.,0.,0.]` and identity transform yield an exponential that translates one meter along x, and a zero logarithm.
2. Tangent `[1.,0.,0.,0.,0.,pi/2]` yields a 90-degree z rotation with translation `[2/pi,2/pi,0]`, not `[1,0,0]`. Supplying this resulting transform to Log recovers the same six-vector.

## Source and scope

[Primary source](https://arxiv.org/abs/1812.01537). This isolates the stated component using synthetic fixtures; completing it does not reproduce the full paper.
