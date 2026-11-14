# Validate a Continuous-Control Time Step

## Goal

A simulator transition carries both an episode-boundary marker and a bootstrap discount.

## Contract

validate_control_timestep(record, observation_size) -> list[str]. observation_size is built-in int1..4096. record must be a dict with string keys, at most16 keys; malformed outer arguments raise ValueError. Required EXACT fields are step_type,reward,discount,observation. Missing fields report missing:<field>; extra fields report unexpected:<field>. Present step_type must built-in int0(FIRST),1(MID),2(LAST), else invalid:step_type. observation must float32/64(observation_size,), all finite abs<=1e6, else invalid:observation. If step_type valid FIRST, present reward and discount must be None; otherwise each reports invalid:<field>. If valid MID/LAST, reward must built-in finite int/float excluding bool abs<=1e6, discount same scalar type in[0,1]. LAST discount need NOT be zero: nonzero allows bootstrap at time-limit truncation. Invalid or missing step_type suppresses dependent reward/discount value validation, but still report missing fields. Return unique sorted issues. This validates one supplied record, not sequence ordering or all released dm_env structures.

## Shared input rules

Original bounded CPU NumPy/Python components, not simulator integrations or reproduced benchmark results. Every array must be an actual NumPy ndarray of the stated dtype and shape; floating arrays use float32 or float64 with finite entries and absolute value <= 1e6 unless stated otherwise. All undocumented invalid types/shapes/ranges raise ValueError. Built-in integer scalars exclude bool; real scalar parameters accept built-in int/float excluding bool, finite and bounded as stated. Preserve inputs, support noncontiguous arrays, return fresh containers; floating outputs use float64, while IDs, counters and Boolean outputs retain the explicitly stated types. CPU Python3.12.3/NumPy2.2.4. No network, clock or global RNG consumption. Two public examples plus independent oracle, invalid, empty/minimal, noncontiguous/preservation and realistic-scale hidden families per task.

## Worked examples

### Example 1

{step_type:2,reward:1,discount:1,observation:array([0.])}, observation_size=1 -> []; LAST with discount1 is allowed.

### Example 2

{step_type:0,reward:0,observation:array([0.]),extra:True}, observation_size=1 -> ['invalid:reward','missing:discount','unexpected:extra'].

## Source and scope

Original bounded component associated with [2018-deepmind-control-suite](https://github.com/google-deepmind/dm_env/blob/master/dm_env/_environment.py). The scope and finite-sample or simulation conventions above are part of this exercise, not a claim of full-paper reproduction.
