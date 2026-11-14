# Version a Simulation Scenario Distribution

Implement version_scenario_distribution(config) -> dict.

config is an exact Python dict with keys simulator, asset_sha256, seed, reset, factors. simulator is ASCII[a-z][a-z0-9_.-]{0,63}; asset_sha256 is64 lowercase hex; seed is a built-in int0..2**32-1 excluding bool; reset must equal "episode". factors is a list of1..32 exact dicts {name,unit,low,high}. Names are unique ASCII[a-z][a-z0-9_-]{0,63}. Unit is one of kg, rad, s, ratio. low/high are built-in finite non-bool int/float with -1e6<=low<=high<=1e6; kg must have low>0, s and ratio low>=0; rad is bounded to[-pi,pi].

Normalize by sorting factors by name, converting low/high to Python float, replacing either signed zero by +0.0, and retaining all other fields. Return {"config":normalized independent dict,"sha256":digest}. Digest is SHA-256 of json.dumps(normalized,sort_keys=True,separators=(",",":"),ensure_ascii=True,allow_nan=False).encode("utf-8"). Preserve input and raise ValueError for every invalid schema/type/range.

Every factor describes an independent uniform distribution (a fixed value when low=high), sampled once per episode. Units are explicit; rad is a caller-named angular parameter, not an inferred rotation frame. This versions declarations and asset identity; it does not sample, open a simulator, check asset bytes, establish statistical equivalence of simulator versions, or prove safety.

## Worked examples

### Canonical physical factors
For simulator="mujoco_3.3.0", asset_sha256="a"*64, seed7, reset="episode", and factors[{name:"yaw",unit:"rad",low:-0.0,high:1},{name:"mass",unit:"kg",low:1,high:2}], normalized factors are mass then yaw, with bounds(1.0,2.0) and(0.0,1.0). The expected digest is `b4c64760cfb749c2893b9126842b995e8f7f176e6d48fb90bda97f3160647bc7`. Exact canonical JSON:

```json
{"asset_sha256":"aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa","factors":[{"high":2.0,"low":1.0,"name":"mass","unit":"kg"},{"high":1.0,"low":0.0,"name":"yaw","unit":"rad"}],"reset":"episode","seed":7,"simulator":"mujoco_3.3.0"}
```

### An impossible mass declaration
The same config with mass.low=0 raises ValueError: mass must remain strictly positive.

## Source and scope

This original bounded component is motivated by [2017-domain-randomization](https://arxiv.org/abs/1703.06907). It does not reproduce the full paper, trained model or benchmark protocol.
