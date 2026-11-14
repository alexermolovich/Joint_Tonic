# Worked examples

## Example 1

Policy actions `[[0.1], [0.2], [0.3]]`, human actions `[[0.9], [0.8], [0.7]]`, intervention `[False, True, True]` and episodes `[0, 0, 0]` produce executed_actions `[[0.1], [0.8], [0.7]]`, segment_id `[-1, 0, 0]` and segments `[[0, 1, 3]]`.

## Example 2

Policy actions `[[0], [0]]`, human actions `[[0.4], [0.5]]`, intervention `[True, True]` and episodes `[0, 1]` produce executed_actions `[[0.4], [0.5]]`, segment_id `[0, 1]` and segments `[[0, 0, 1], [1, 1, 2]]`. The episode boundary splits the human run.
