# Worked examples

## Average directions, not magnitudes

images=[[1,0]], prompts=[[[2,0],[0,20]]],temperature=1. Both unit prompt directions contribute equally. Prototype=[sqrt(.5),sqrt(.5)], logits=[[sqrt(.5)]]. Averaging raw prompts would incorrectly favor the second axis.

## Two classes and temperature

images=[[3,4]], prompts=[[[1,0],[2,0]],[[0,1],[0,3]]],temperature=.5. Prototypes=[[1,0],[0,1]], logits=[[1.2,1.6]]. These are scores, not probabilities.
