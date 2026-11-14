# Independent review

Status: reviewed for implementation. Reviewer: vla_implementation.

Approved for implementation. Reviewed all six draft files, the rectangular injective assignment contract, empty targets, exact index validity, objective tolerance and tied optima. Exhaustive enumeration independently confirms both worked objectives (4 and 2). The [official DETR matcher](https://github.com/facebookresearch/detr/blob/main/models/matcher.py) confirms matching true targets to a distinct subset of queries and leaving other queries unmatched. This exercise implements its own polynomial solver without SciPy.

Theory correction applied during review: the rectangular dual needs nonpositive query potentials and zero potentials on unused queries at a complementary optimum. Reduced-cost feasibility alone was not a complete certificate; the explanation now includes these conditions. Test negative costs, rectangular inputs and ties without requiring a particular tie order.

Reference/evaluator correctness and actual isolated Run/Submit remain publication gates; this approval is for the documented contract and pedagogy.
