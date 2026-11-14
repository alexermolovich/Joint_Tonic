# Normalize and Multiply Quaternions

Implement **compose_quaternions(q_after, q_before)** for active right-handed rotations in one fixed Cartesian basis. Each input is a finite real integer/floating array-like of shape (4,), in scalar-first Hamilton order [w,x,y,z]. Component magnitudes must be <=1e6 and at least one component must be nonzero. Reject bool, complex, string and object dtypes.

Normalize both inputs using a scale-safe norm (divide by max(abs(q)) before taking the norm). Return a new float64 unit quaternion representing q_before followed by q_after, using the Hamilton product. Normalize the product once more. Preserve its computed sign: do not force w>=0 or flip either input. Thus negating exactly one input negates the output while leaving the represented rotation unchanged.

No batching, translation, timestamp estimation or frame conversion. The rotations describe the same static coordinate basis. Every documented violation raises ValueError; preserve inputs and independent output storage. Tiny nonzero float64 quaternions such as [1e-300,0,0,0] are valid.

NumPy CPU; numerical tolerance rtol=1e-7, atol=1e-9. Masks, shapes and errors are exact.
