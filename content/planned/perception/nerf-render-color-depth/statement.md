# Render Color and Expected Depth Along a Ray

Implement render_rays(weights, colors, depths, background, background_rgb). All inputs are finite NumPy float64 arrays with shapes (R,S),(R,S,3),(R,S),(R,),(3,), R,S>=1, each dimension<=1024 and colors at most1,000,000 elements. Weights/background lie in [0,1]; require weights.sum(1)+background close to1 with atol1e-6,rtol0. Colors and background_rgb lie in [0,1] as linear RGB. Depths lie in [0,1e6] meters along normalized rays, nondecreasing per row. Compute rgb=sum(weights[...,None]*colors,axis=1)+background[:,None]*background_rgb. Return conditional foreground depth sum(weights*depths)/sum(weights) only where foreground mass>1e-8; elsewhere depth=NaN and valid=False. Return new float64 rgb/depth and bool valid, preserving inputs. TypeError for non-arrays, ValueError for all other violations. No clipping or renormalizing supplied compositing weights; depth normalization is intentionally conditional on a foreground hit. No gamma conversion, density evaluation, background depth assignment, or scene training.

## Worked examples

## A partially transparent ray

weights=[[.5,.25]], colors=[[[1,0,0],[0,1,0]]], depths=[[2,4]], background=[.25], background_rgb=[0,0,1]. Return rgb=[[.5,.25,.25]], depth=[8/3], valid=[True]. The foreground moment2 is divided by foreground mass.75.

## No foreground evidence

weights=[[0,0]], colors=[[[1,1,1],[0,0,0]]], depths=[[1,3]], background=[1], background_rgb=[.2,.3,.4]. Return rgb=[[.2,.3,.4]], depth=[NaN], valid=[False]. A visible background color does not establish a surface depth.
