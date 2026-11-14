## Example 1

Scores [[-1, 0, 1, 2, 3]], all valid, yield rewards [[0, 0.75, 1, 0.75, 0]], score gradients [[0, 0.5, 0, -0.5, 0]] and mean_reward 0.5.

## Example 2

Score 4 yields reward 0 and gradient 0. An invalid score 0 also yields zero reward and gradient; an entirely invalid batch has mean_reward 0.
