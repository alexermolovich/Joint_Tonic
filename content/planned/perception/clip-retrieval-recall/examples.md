# Worked examples

## Retrieval direction matters

scores=[[.9,.8],[.95,.1]], k=1. Image0 retrieves text0, image1 retrieves text0: image_to_text=0.5. Text0 retrieves image1, text1 retrieves image0: text_to_image=0.0. Output {'image_to_text':0.5,'text_to_image':0.0}.

## Deterministic ties

scores is a 3x3 all-zero float64 matrix; k=2. Every query selects candidates0,1. Two of three diagonal positives are included in each direction. Output both2/3. At k=3 both become1.
