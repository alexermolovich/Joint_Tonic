# Worked examples

## Average the symmetric2x2 grid

positions=[[[99],[1],[2],[3],[4]]], float64, old_grid=(2,2),new_grid=(1,1). Return [[[99],[2.5]]]. The class position is not averaged with spatial positions.

## Preserve a constant spatial field

positions=[[[7,8],[2,3],[2,3]]], float32, old_grid=(1,2),new_grid=(2,3). Return class[7,8] followed by six copies of[2,3], shape(1,7,2).
