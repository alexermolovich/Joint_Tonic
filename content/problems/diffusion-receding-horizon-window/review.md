# Independent contract review

Status: reviewed; independent evaluator/sandbox approval remains separate.

Reviewer: code_issue_scout. Read all six draft files and staged reference code. Confirmed receding-horizon intent against Diffusion Policy primary manuscript. Independently recomputed both windows, checked no storage alias, and verified that one unavailable selected tick rejects the entire batch. Alignment offset is supplied, invalid unselected rows remain permitted, and actual robot execution is explicitly out of scope.

Six worked examples across this batch passed independent WSL numerical probes; CVAE and projection gradients were checked analytically. No blocking contract finding. Author owns final cases and actual isolated Run/Submit verification.


## Runtime verification — implementation worker

Reference passed 5 unique public/hidden checks in the actual Linux bubblewrap worker, using both public Run and complete Submit. Python3.12.3, NumPy2.2.4 and PyTorch2.6.0CPU where required; shared18s wall/10s CPU/4096MiB/64KiB caps. The checks cover the published contract, not full-paper reproduction. The evaluator source SHA-256 is pinned in blueprint.md; no OCI digest is claimed for the local environment. Static theory tables and original LaTeX are present; no source figure or paper code was copied.
