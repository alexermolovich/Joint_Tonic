# Stratify Samples Along Near and Far Bounds

Implement stratified_samples(near, far, draws). All inputs are finite NumPy float64 arrays. near and far have shape (R,), 1<=R<=4096, satisfying 0<=near<far<=1e6 meters and far-near>=1e-6 m. draws has shape (R,S), 1<=S<=1024, at most1,000,000 elements, with values in [0,1). Divide each [near,far] into S equal-width bins; sample one depth per bin with the corresponding supplied draw. z[r,i]=near[r]+(i+draws[r,i])*(far[r]-near[r])/S. Return new float64 (R,S); no RNG calls, mutation or sorting. Noncontiguous arrays supported. TypeError for non-array inputs; ValueError for all other violations. Ray directions are already normalized, so z is meters along each ray, not camera optical z. One static scene exposure; no inverse-depth spacing, hierarchical PDF sampling, or appended infinity. Equal-width full-interval bins are the explicit teaching discretization, not every implementation's endpoint-midpoint convention.

## Worked examples

## Three equal bins

near=[1], far=[4], draws=[[0,.5,.75]]. Each bin is1m wide. Return [[1,2.5,3.75]].

## Independent ray bounds

near=[0,2], far=[2,6], draws=[[.25,.75],[.5,0]]. Return [[.25,1.75],[3,4]]. The second ray's bins are2m wide.

## Hints

1. Compute one bin width per ray.
2. Broadcast increasing bin indices over rays.
3. Apply each supplied draw inside its own bin; never call random.
