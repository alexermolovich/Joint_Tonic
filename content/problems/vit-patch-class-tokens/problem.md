# Build Learned Patch and Class Tokens

Implement build_vit_tokens(patches, projection, bias, cls, positions). All five arguments are finite CPU PyTorch tensors with the same dtype float32 or float64 and absolute values <=100. Require patches shape (B,N,F), projection (F,D), bias and cls (D,), positions (N+1,D). B may be zero; N,F,D are positive; the named dimensions B,N,F,D are each <=1024 (the positions sequence N+1 may be1025) and every input and output has at most 1,000,000 elements. Compute each patch row @ projection + bias, prepend the supplied learned cls vector to each batch item, then add positions to every batch. Return a new (B,N+1,D) tensor preserving dtype/device and gradient paths to all inputs. Do not alter inputs. No dropout, normalization, attention, image patchification, or parameter initialization. TypeError for non-tensors; ValueError for all other violations, including shapes, bounds, dtype/device. A zero batch returns (0,N+1,D). Feature and positional values are dimensionless; sequence order is caller-provided image-patch order, and all patches in a row belong to one exposure. This is the token-assembly step of ViT, not a trained encoder.

## Examples

## Two patches

patches=[[[1,2],[3,4]]], projection=[[1,0],[0,2]], bias=[1,-1], cls=[10,20], positions=[[.1,.2],[.3,.4],[.5,.6]], all float64. Output is [[[10.1,20.2],[2.3,3.4],[4.5,7.6]]]. The class token is not sent through the patch projection.

## One feature

patches=[[[2]]], projection=[[3]], bias=[1], cls=[-2], positions=[[.5],[1]], all float32. Output is [[[-1.5],[8]]]. The patch token is 2*3+1+1=8.

## Hints

1. Project only patch rows.
2. Expand the class token across the batch before concatenation.
3. Add the full N+1 position matrix after prepending.
