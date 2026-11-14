# Worked examples

### Canonical physical factors
For simulator="mujoco_3.3.0", asset_sha256="a"*64, seed7, reset="episode", and factors[{name:"yaw",unit:"rad",low:-0.0,high:1},{name:"mass",unit:"kg",low:1,high:2}], normalized factors are mass then yaw, with bounds(1.0,2.0) and(0.0,1.0). The expected digest is `b4c64760cfb749c2893b9126842b995e8f7f176e6d48fb90bda97f3160647bc7`. Exact canonical JSON:

```json
{"asset_sha256":"aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa","factors":[{"high":2.0,"low":1.0,"name":"mass","unit":"kg"},{"high":1.0,"low":0.0,"name":"yaw","unit":"rad"}],"reset":"episode","seed":7,"simulator":"mujoco_3.3.0"}
```

### An impossible mass declaration
The same config with mass.low=0 raises ValueError: mass must remain strictly positive.
