# Finite-Difference Gradient Check

Implement check_calibration_gradient(design, parameters, target, analytic, step, tolerance) -> dict.

design is NumPy float64(M,D), parameters and analytic float64(D,), target float64(M,),1<=M<=64,1<=D<=32. Arrays finite with magnitude<=100. step is finite built-in non-bool numeric in[1e-6,1e-2]; tolerance finite built-in numeric in[0,1], non-bool. Define loss(x)=0.5*sum((design@x-target)**2), no division by M. For each parameter independently evaluate loss at x±step*unit_vector; numeric[j]=(loss_plus-loss_minus)/(2*step). Return numeric:float64(D,), relative_error:float64(D,)=abs(numeric-analytic)/maximum(1,abs(numeric),abs(analytic)), passed:bool true iff every error<=tolerance. Preserve inputs; noncontiguous valid. Invalid contracts raise ValueError.

The design is a dimensionless normalized local sensor-calibration model, parameters normalized calibration offsets, target normalized residual measurements. This checks the supplied gradient against explicit finite differences of the stated objective, not an analytic shortcut. The finite difference is approximate; near-cancellation can require a larger step or tolerance. No simulator or differentiable framework is invoked.

## Worked examples

### Correct gradient
A=[[2]], x=[1], target=[1], analytic=[2], step0.001,tolerance1e-8 returns numeric approximately[2], relative_error approximately[0], passedTrue.

### Wrong sign
Same inputs with analytic[-2] returns numeric approximately[2], relative_error approximately[2], passedFalse.

## Source and scope

Original robotics evaluation exercise. [NumPy reference](https://numpy.org/doc/2.2/reference/) documents the array operations; the physical contract and synthetic examples are original.
