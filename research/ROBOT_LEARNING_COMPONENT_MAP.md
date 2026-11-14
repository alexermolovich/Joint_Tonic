# Robot learning and dexterity component mapping

The main agent read and mapped all 27 pre-existing cards in `robot-learning-rl/` and `humanoid-dexterity-tactile/`: 81 explained stages, 10 runnable primitive associations, and 103 planned component placements. The newly collected Mobile ALOHA card was mapped separately by the research curator.

Each association appears both in execution-flow metadata and beside the corresponding mathematical explanation. Planned titles remain original authoring ideas unless separately approved through a problem blueprint; they do not silently expand the 189-entry curriculum. Runnable links retain explicit component limits.

Independent review by `code_issue_scout` inspected all 81 stage titles and checked the higher-risk DP3, UMI, dexterous-hand, DrEureka and SAC associations against the actual problem contracts. No correction remained requested. In particular:

- DP3 links max pooling after per-point features, supplied-noise construction, epsilon-prediction loss and action-prefix extraction; these do not imply a trained 3D policy or reverse sampler.
- UMI links point-frame transformation practice without claiming calibration, pose tracking or cross-time pose composition.
- Dynamics-randomization tasks sample explicitly supplied bounded distributions; they do not reproduce a full transfer pipeline.
- CLIPort and R3M do not link an unrelated CLIP training loss as their robot objective.
- Automatic SAC temperature tuning is labeled as a later extension and cites its own primary source.

The shared audit validates stage headings, published slugs, planned-title bounds and full stage coverage. Run `npm run validate:paper-links -- --write` to refresh [the complete component map](FLOW_PROBLEM_MAP.md). This review is an implementation-association check, not an independent reproduction of every paper's experiments.
