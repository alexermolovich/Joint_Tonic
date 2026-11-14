## Approach

Validate synchronized shapes and masks, concatenate along feature width, apply the affine projection and mask the output after adding bias. Bitwise intersection allocates an independent validity tensor. Keeping the computation in PyTorch preserves gradients; masked rows have zero gradient.

See Theory for the mathematical derivation and worked gradient examples.
