# Worked examples

## Keep the best interpretation

masks=[[[1,0]],[[0,1]],[[1,1]]] as bool, scores=[.7,.9,.8], k=2. Output masks=[[[0,1]],[[1,1]]], indices=[1,2], scores=[.9,.8]. Geometry follows each chosen index unchanged.

## Preserve score ties and raw quality

masks=[[[1]],[[0]],[[1]]] as bool, scores=[1.2,1.2,-.1], k=2. Output indices=[0,1], masks=[[[1]],[[0]]], scores=[1.2,1.2]. Lower input index breaks the tie; scores are not clipped to one.
