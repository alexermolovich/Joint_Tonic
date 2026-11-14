# Worked examples

## A partially transparent ray

weights=[[.5,.25]], colors=[[[1,0,0],[0,1,0]]], depths=[[2,4]], background=[.25], background_rgb=[0,0,1]. Return rgb=[[.5,.25,.25]], depth=[8/3], valid=[True]. The foreground moment2 is divided by foreground mass.75.

## No foreground evidence

weights=[[0,0]], colors=[[[1,1,1],[0,0,0]]], depths=[[1,3]], background=[1], background_rgb=[.2,.3,.4]. Return rgb=[[.2,.3,.4]], depth=[NaN], valid=[False]. A visible background color does not establish a surface depth.
