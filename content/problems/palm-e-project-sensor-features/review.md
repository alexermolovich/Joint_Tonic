# Independent contract review

Status: reviewed; independent evaluator/sandbox approval remains separate.

Reviewer: code_issue_scout. Read all six draft files and staged reference code. Read paired card and verified PaLM-E primary HTML/proceedings. Affine projection is correctly scoped as a supplied component, not the entire modality encoder. Independently recomputed both examples and masked feature/bias gradients. Shapes, row preservation, empty tokens, finite padding and no downstream attention-mask guarantee are explicit.

Six worked examples across this batch passed independent WSL numerical probes; CVAE and projection gradients were checked analytically. No blocking contract finding. Author owns final cases and actual isolated Run/Submit verification.


## Runtime verification — implementation worker

Reference passed 6 unique public/hidden checks in the actual Linux bubblewrap worker, using both public Run and complete Submit. Python3.12.3, NumPy2.2.4 and PyTorch2.6.0CPU where required; shared18s wall/10s CPU/4096MiB/64KiB caps. The checks cover the published contract, not full-paper reproduction. The evaluator source SHA-256 is pinned in blueprint.md; no OCI digest is claimed for the local environment. Static theory tables and original LaTeX are present; no source figure or paper code was copied.
