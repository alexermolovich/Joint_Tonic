# Gate Sim-to-Real Release with Robustness Evidence

Implement robustness_release_gate(required, evidence, expected_distribution, min_trials, min_success_rate, min_worst_return) -> dict.

required is a Python list of1..128 unique ASCII slice IDs[a-z][a-z0-9_-]{0,63}. expected_distribution is64 lowercase hex. min_trials is a built-in non-bool int1..1e6; min_success_rate is a finite built-in non-bool int/float in[0,1]; min_worst_return finite in[-1e6,1e6]. evidence is a Python list of0..128 exact dicts with keys slice, distribution_sha256, trials, successes, worst_return. Slice IDs are unique and must be required. Distribution digest has the same hex schema; trials is a built-in int1..1e6, successes a built-in int0..trials, and worst_return a finite built-in numeric in[-1e6,1e6]. Validate every evidence record even when another record already fails.

Return {"approved":bool,"reasons":list[str]}. For each required slice in lexicographic order, emit slice+":missing" if absent. Otherwise emit every failing reason in this fixed order: distribution (digest mismatch), trials (trials<min_trials), success (successes/trials<min_success_rate), worst-return (worst_return<min_worst_return). Equality passes. Invalid contracts raise ValueError; missing/weak/mismatched valid evidence returns rejection reasons. Preserve inputs.

Trials are per-slice independent scenario episodes; success fractions and comparable normalized returns are dimensionless. The distribution hash identifies a declared simulation protocol. This original deterministic evidence checklist does not certify real-robot safety, verify raw logs, estimate confidence, deploy a policy or replace hardware validation.

## Worked examples

### Exact thresholds pass
required["a"], expected_distribution="a"*64, thresholds min_trials10,min_success_rate0.8,min_worst_return=-1, evidence[{slice:"a",distribution_sha256:"a"*64,trials:10,successes:8,worst_return:-1}] returns approvedTrue,reasons[].

### All independent failures are visible
required["b","a"], same thresholds, evidence[{slice:"a",distribution_sha256:"b"*64,trials:5,successes:1,worst_return:-2}] returns approvedFalse,reasons["a:distribution","a:trials","a:success","a:worst-return","b:missing"].

## Source and scope

This original bounded component is motivated by [2018-dynamics-randomization](https://arxiv.org/abs/1710.06537). It does not reproduce the full paper, trained model or benchmark protocol.
