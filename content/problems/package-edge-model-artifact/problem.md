# Package and Verify an Edge Model Artifact

Implement package_edge_model(model_bytes, metadata, expected_sha256) -> dict.

model_bytes is built-in bytes of1–1048576 bytes. expected_sha256 is64 lowercase hexadecimal characters and must equal SHA-256(model_bytes). metadata is exactly a dict with format in{"onnx","tflite"}, runtime a string ASCII[a-z][a-z0-9_.-]{0,63}, input_shape a tuple of1–4 positive built-in non-bool ints<=4096 with product<=1000000, input_dtype in{"float32","uint8"}, and calibration_sha256 a64-character lowercase hexadecimal string. These descriptors identify a supplied model interface; no actual model parsing occurs.

Return a fresh dict containing model_sha256, size_bytes, metadata (independent deep copy preserving its tuple shape), and manifest_sha256. The manifest hash is SHA-256 of UTF-8 json.dumps({"model_sha256":actual,"size_bytes":len(model_bytes),"metadata":metadata},sort_keys=True,separators=(",",":"),ensure_ascii=True). JSON converts input_shape's tuple to a JSON array. The manifest itself does not include manifest_sha256 in its hash. Preserve inputs. Invalid types/schema/bounds or mismatching expected digest raise ValueError.

This packages in-memory identity evidence, not a signed release, ONNX validator, file writer, or proof of execution safety. Calibration bytes are not supplied and their digest is only recorded, not independently verified. Model weights/input data remain dimensionless or quantized values under the declared external calibration contract.

## Worked examples

### Small synthetic bytes
For bytes b"abc", expected digest `ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad` and metadata{"format":"onnx","runtime":"cpu_v1","input_shape":(1,3),"input_dtype":"float32","calibration_sha256":"a"*64}, return size_bytes3, that model digest, an independent copy of metadata, and manifest_sha256 `621fac405d6f2388da61e02460f1b9e5e57b92762b5e02eae07c64105275358c` from the exact canonical JSON defined above. The synthetic bytes need not be a valid ONNX file because parsing is out of scope.

### Mismatching expected bytes
With b"abc", the same metadata and expected_sha256="0"*64, raise ValueError before returning a package.

## Source and scope

This original bounded component is motivated by [2020-once-for-all](https://arxiv.org/abs/1908.09791). It does not reproduce the full paper, trained model or benchmark protocol.
