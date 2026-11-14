# Hints

1. Validate the exact declared shapes and masks before doing arithmetic.
2. Compute shared dot-product scores, apply two independent stable masked softmax operations, and multiply each weight matrix by the opposite modality's tokens.
3. Use the worked trace to check axis order and boundary conventions.
