# Evaluation and failure analysis

Run checks a zero-error field and one analytically worked SGD update. Submit adds an independent scalar renderer, finite-difference parameter gradients, an active global-clipping case, held-out data isolation, maximum shapes, zero-step behavior and malformed inputs. Passing validates the declared bounded training loop; it is not evidence that a real scene has been reconstructed.

Inspect training loss and held-out RGB MSE separately. Change only evaluation targets and verify that learned parameters and training traces stay identical. Compare a bright background with a black one to expose missing background gradients. Inspect clipping norms; frequent clipping can mask a poor scale or learning-rate choice. Image agreement alone does not certify surface geometry, free space or robot safety.

Record the limitations of fixed features and sample locations. A future extension can compare supplied hierarchical samples or a deeper field, but it must introduce a reviewed contract and its own reproducibility evidence.
