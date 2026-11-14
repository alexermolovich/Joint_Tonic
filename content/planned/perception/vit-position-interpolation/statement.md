# Interpolate 2D Positional Embeddings

Implement resize_positions(positions, old_grid, new_grid). positions is a finite CPU torch float32/float64 tensor, abs values<=100, shape(1,1+H0*W0,D),1<=D<=256. Each grid is a length2 tuple of built-in ints excluding bool; each dimension1..128. Input and output each have at most1,000,000 elements. Row0 is a class-token position and must remain exactly unchanged. Remaining rows are a row-major H0xW0 grid; reshape to channels-first, interpolate with torch.nn.functional.interpolate(size=new_grid,mode='bicubic',align_corners=False,antialias=False), then restore row-major sequence order and prepend row0. Return new independent storage preserving dtype/device and gradients. Noncontiguous input supported; input unchanged. TypeError for non-tensor; ValueError for other violations. No square-grid inference or image interpolation. Embeddings are dimensionless learned position coordinates, not metric robot poses. The interpolation convention is explicit; some model libraries use align_corners=True, which is outside this contract.

## Worked examples

## Average the symmetric2x2 grid

positions=[[[99],[1],[2],[3],[4]]], float64, old_grid=(2,2),new_grid=(1,1). Return [[[99],[2.5]]]. The class position is not averaged with spatial positions.

## Preserve a constant spatial field

positions=[[[7,8],[2,3],[2,3]]], float32, old_grid=(1,2),new_grid=(2,3). Return class[7,8] followed by six copies of[2,3], shape(1,7,2).
