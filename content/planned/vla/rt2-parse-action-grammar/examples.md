# Worked examples

## Recover ordered action bins

tokens=[[0,41,99],[1,7,41]], vocabulary=[41,7,99], all int64.

Return bins=[[0,2],[1,0]], termination=[0,1]. Lookup by vocabulary position recovers bin identity.

## Reject a malformed channel

tokens=[[0,41,1]], vocabulary=[41,7,99] raises ValueError: token1 is a termination flag, not an action-vocabulary entry. A valid single-channel row [[1,7]] returns bins=[[1]], termination=[1].
