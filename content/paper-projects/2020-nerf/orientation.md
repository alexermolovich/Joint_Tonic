# Train a Tiny Radiance Field

Reproduce a small executable image-to-field learning loop: supplied coordinate features feed a shared density/color function, ordered volume rendering produces RGB, and analytic image gradients update the field. Finish by rendering held-out rays.

The integration uses an affine, view-independent field, fixed supplied samples, synthetic data and an explicit clipped SGD recipe. It omits the deep NeRF MLP, coarse/fine network training, view-direction conditioning, real camera datasets and headline benchmark comparisons. The separate hierarchical sampler is a stretch exercise, not an implicit feature of this task.

Before starting, check that you can explain why density attenuates downstream color and background. Use the renderer and gradient problems to diagnose that prerequisite. Keep one scene coordinate convention, normalized ray directions, metric intervals and linear RGB throughout.
