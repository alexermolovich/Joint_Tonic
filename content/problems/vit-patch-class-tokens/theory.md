# Assemble the input sequence of a Vision Transformer

## Intuition

Patch vectors contain pixels; attention expects vectors in a shared embedding space. A learned projection supplies that space. A separate class token provides a place for the eventual image-level summary, and positional vectors tell the otherwise order-agnostic attention which patch came from where.

## The three operations

Let $X\in\mathbb R^{B\times N\times F}$ contain B images, N patches per image, and F features per patch. Let $W\in\mathbb R^{F\times D}$ and $b\in\mathbb R^D$ be the patch projection; D is embedding width. The learned class token is $c\in\mathbb R^D$ and positions are $P\in\mathbb R^{(N+1)\times D}$. All coordinates are dimensionless. For batch index a,

$$
Z_{a,0,:}=c+P_{0,:},\qquad
Z_{a,n+1,:}=X_{a,n,:}W+b+P_{n+1,:}.
$$

The class token uses its own positional row. It is never projected with W or shifted by the patch bias. Shared parameters are broadcast over B, so their gradients accumulate contributions from all images.

## Visual: token assembly

| Stage | Shape | First example |
|---|---|---|
| Patch input | B,N,F | [1,2]; [3,4] |
| Affine patch projection | B,N,D | [2,3]; [4,7] |
| Prepend class token | B,N+1,D | [10,20]; [2,3]; [4,7] |
| Add positions | B,N+1,D | [10.1,20.2]; [2.3,3.4]; [4.5,7.6] |

Read downward to follow one image. This static shape trace is also the text alternative. A class token is shared initially, but later attention can make its representation image-dependent.

## Gradients and the empty batch

The projection and concatenation must remain differentiable. Detaching a correct-looking sequence would prevent learning W, c, or P. With B=0 there are no images and the result has zero rows; the declared sequence width still includes the class token.

## Why this matters on a robot

An exported VLM backbone must preserve the training patch traversal and positional indexing. Off-by-one position shifts can corrupt spatial features even when every tensor shape matches. Learned tokens also belong in the checkpoint; recreating random tokens at deployment changes the model.

## Questions and scope

Why does the class token receive a position vector? It occupies a defined sequence slot with its own learned offset. Does this function classify an image? No: transformer blocks and a readout are separate components.

Source: [ViT §3.1](https://arxiv.org/abs/2010.11929). First complete [patchification](/problems/vit-patchify-reconstruct). The example isolates input assembly and makes no accuracy claim.
