# Worked examples

## Example 1

Trial durations `[10, 20]`, human durations `[0, 5]`, reset durations `[2, 3]`, task success `[True, True]`, reset success `[True, False]`, all valid: trials `2`, autonomous_trials `1`, robot_time `35`, human_time `5`, reset_time `5`, human_fraction `1/6`, task_success_rate `1`, reset_success_rate `0.5` and autonomous_success_rate `1`.

## Example 2

For three empty duration arrays and three empty Boolean arrays, trials and autonomous_trials are `0`; robot_time, human_time and reset_time are `0.0`; human_fraction and all three success rates are `NaN`. No evidence is converted into a zero success rate.
