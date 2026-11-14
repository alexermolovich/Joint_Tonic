# Build a Prompt-Ensembled Zero-Shot Classifier

Implement prompt_ensemble_classifier(images, prompts, temperature). images and prompts are finite NumPy float64 arrays shaped(B,D),(C,P,D),1<=B<=256,1<=C<=1000,1<=P<=64,1<=D<=512; each array at most1,000,000 elements. Each image/prompt vector has L2 norm in[1e-6,1e6]. First normalize each prompt independently, average P unit prompts within each class, then normalize each class mean; reject a class mean with norm<1e-6. Normalize image rows and compute logits=unit_images @ prototypes.T / temperature. temperature is built-in int/float excluding bool in[1e-4,1e4]. Return new float64 (logits,prototypes), preserving inputs and noncontiguous support. TypeError for non-array inputs; ValueError for other violations. No softmax, tokenization, encoder, class-label output, or averaging raw unnormalized prompts. Rows/classes/prompt grouping preserve caller order. Features are dimensionless; each prompt group describes one class. This is inference prototype construction, not a gradient-based training API.

## Worked examples

## Average directions, not magnitudes

images=[[1,0]], prompts=[[[2,0],[0,20]]],temperature=1. Both unit prompt directions contribute equally. Prototype=[sqrt(.5),sqrt(.5)], logits=[[sqrt(.5)]]. Averaging raw prompts would incorrectly favor the second axis.

## Two classes and temperature

images=[[3,4]], prompts=[[[1,0],[2,0]],[[0,1],[0,3]]],temperature=.5. Prototypes=[[1,0],[0,1]], logits=[[1.2,1.6]]. These are scores, not probabilities.

## Hints

1. Normalize along D for every class/prompt pair.
2. Average only the prompt axis, then normalize the class means.
3. Divide the image-to-class cosine matrix by the supplied temperature.
