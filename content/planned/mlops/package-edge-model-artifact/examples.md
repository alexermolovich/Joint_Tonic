# Worked examples

### Small synthetic bytes
For bytes b"abc", expected digest `ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad` and metadata{"format":"onnx","runtime":"cpu_v1","input_shape":(1,3),"input_dtype":"float32","calibration_sha256":"a"*64}, return size_bytes3, that model digest, an independent copy of metadata, and manifest_sha256 `621fac405d6f2388da61e02460f1b9e5e57b92762b5e02eae07c64105275358c` from the exact canonical JSON defined above. The synthetic bytes need not be a valid ONNX file because parsing is out of scope.

### Mismatching expected bytes
With b"abc", the same metadata and expected_sha256="0"*64, raise ValueError before returning a package.
