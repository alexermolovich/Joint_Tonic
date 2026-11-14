# Normalize and Multiply Quaternions

Implement **compose_quaternions(q_after, q_before)** for active right-handed rotations in one fixed Cartesian basis. Each input is a finite real integer/floating array-like of shape (4,), in scalar-first Hamilton order [w,x,y,z]. Component magnitudes must be <=1e6 and at least one component must be nonzero. Reject bool, complex, string and object dtypes.

Normalize both inputs using a scale-safe norm (divide by max(abs(q)) before taking the norm). Return a new float64 unit quaternion representing q_before followed by q_after, using the Hamilton product. Normalize the product once more. Preserve its computed sign: do not force w>=0 or flip either input. Thus negating exactly one input negates the output while leaving the represented rotation unchanged.

No batching, translation, timestamp estimation or frame conversion. The rotations describe the same static coordinate basis. Every documented violation raises ValueError; preserve inputs and independent output storage. Tiny nonzero float64 quaternions such as [1e-300,0,0,0] are valid.

NumPy CPU; numerical tolerance rtol=1e-7, atol=1e-9. Masks, shapes and errors are exact.

## Worked examples

### Normalize before composing

q_after=[2,0,0,0], q_before=[0,0,0,3].

Return [0,0,0,1]. An identity rotation applied after a 180° z rotation leaves it unchanged.

### Two different axes

Let s=sqrt(0.5). q_after=[s,0,0,s] is +90° about z, q_before=[s,s,0,0] is +90° about x.

Return [0.5,0.5,0.5,0.5]. A vector initially along +y first moves to +z and stays +z under the second rotation. Reversing the input order produces [0.5,0.5,-0.5,0.5], a different rotation.

## Hints

1. Normalize each input by scaling its largest absolute component first.

2. Separate scalar and vector parts to organize the Hamilton product.

3. Keep the input/product sign; do not force a positive scalar component.
