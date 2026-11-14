# Normalize Heterogeneous Robot Observation Schemas

## Intuition

Robot datasets often describe the same signal under different keys and units. Normalize names and scales explicitly while refusing to guess missing channels or coordinate transforms from array shape.

## Mathematical mechanism

For canonical field c, let m(c) name its raw source and s_c be a positive conversion factor. Define $$Y_c[t,j]=s_c X_{m(c)}[t,j].$$ Each raw field X has T synchronized rows but can have its own width D. This operation changes units and labels; it does not apply an SE(3) transform or infer joint order.

## Visual computation trace

| Raw field | Mapping | Scale | Canonical values |
|---|---|---|---|
| position_cm=[100,200] | position | 0.01 | [1,2]m |
| gripper=[0,1] | grasp | 1 | [0,1] |

The table is the static visual and its text alternative; each row describes a transformation or decision.

## Worked calculation

raw={"p_cm":[[100],[200]]}, mapping={"position":"p_cm"}, scales={"position":0.01}, timestamps=[0,1] returns features={"position":[[1],[2]]} and timestamps=[0,1].

## Why this matters on a robot

Renaming camera-frame coordinates to base-frame coordinates does not transform them. A conversion factor must be tied to a versioned schema and calibration record. Validating unused raw fields prevents hidden malformed sensor channels from being silently retained upstream.

## Physical contract and limits

Caller supplies multiplicative conversion factors such as centimeters to meters0.01 or degrees to radianspi/180; output units are the declared canonical units. One synchronized strictly increasing timestamp vector applies to every field; this function cannot align unsynchronized records. Original shared-schema adapter motivated by Open X-Embodiment dataset standardization. Field mapping and scaling are explicit educational policy, not the complete OXE dataset transforms.

Source: [primary paper](https://arxiv.org/abs/2310.08864). Prerequisite: understand the observation/action schema supplied in the contract; no additional lesson is required.
