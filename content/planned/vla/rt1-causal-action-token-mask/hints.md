# Progressive hints

## Hint 1

Use position modulo visual_tokens+action_tokens to determine token type. Do not infer type from the timestep alone.

## Hint 2

Start with the causal relation key_index<=query_index, then form the outer AND of action-slot indicators.

## Hint 3

Clear the action/action cells only. Check the V1 row from Case2 to catch the tempting but incorrect rule that blocks every action-key column.
