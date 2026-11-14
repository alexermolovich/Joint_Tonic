# Validate a Generated Reward Program

A small arithmetic reward language makes each generated term inspectable. Walk its syntax tree explicitly so the supported computations and resource limits are part of the contract.

## Contract

expression is built-in str of length 1..512, parsed as a Python expression but never executed with eval/exec. features is dict with 1..16 keys matching ASCII [a-z][a-z0-9_]{0,31}, values real (B,) with shared 0<=B<=4096, finite abs<=100. Allowed AST: Expression, binary +,-,*, unary +,-, feature Name, numeric literal built-in int/float excluding bool with finite abs<=100; parentheses only group. Maximum 128 AST nodes (including operator/context nodes from ast.walk), maximum 16 expression-value levels excluding outer Expression: each leaf depth 1; operator depth 1+max child depth. Reject all other syntax and unknown names, including in empty batches. Validate every produced array element finite abs<=1e6; no clipping. With B=0 these elementwise bounds are vacuous, but syntax, literal bounds, feature names, node count and depth are always checked before evaluation. Return dict reward float64(B,), used_features list[str] sorted unique referenced feature names, node_count Python int len(list(ast.walk(tree))). Numeric constant expressions broadcast to B. This original restricted arithmetic language provides inspectable reward formulas; it is not a security sandbox for arbitrary Python, a complete generated reward function, or a claim about the paper's program grammar.

Unless a tighter bound is stated below, numeric array-like inputs must have real integer/floating dtype after `np.asarray`, be finite with absolute values <=1e6 and at most 1,000,000 entries. Boolean, complex, string and object numeric arrays are invalid; Boolean masks must have Boolean dtype. Integer arrays/scalars exclude booleans. All invalid inputs raise ValueError. Return new arrays, preserve inputs, and compute floating outputs in float64 on CPU. No automatic differentiation is required.

## Physical context and scope

Reward contributions and independent progress/success metrics are dimensionless and already normalized. Observations are recorded rollout steps; paired comparisons share seed identity by column. No coordinate transform or simulator execution is implicit. Original bounded reward-design diagnostic or arithmetic teaching language. It does not reproduce language-model search, policy training or real-robot transfer.

## Example 1

expression "progress - 2 * effort", features progress [3,4], effort [1,.5] -> reward [1,3], used_features ["effort","progress"], node_count 10.

## Example 2

expression "1 + 2", any one valid feature array of length 2 -> reward [3,3], used_features [], node_count 5. Attribute access, calls, division, powers and indexing all raise ValueError.
