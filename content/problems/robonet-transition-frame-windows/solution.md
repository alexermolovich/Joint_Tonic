# Solution explanation

Validate all source arrays and output budgets before allocation. Scan each requested start/horizon pair; gather matching current frame, next frame and transition action only when the complete validity predicate holds. Work and output storage scale with the explicitly capped image/action output sizes.
