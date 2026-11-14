---
schema_version: 1
paper_id: "2020-digit-tactile-sensor"
title: "DIGIT: A Novel Design for a Low-Cost Compact High-Resolution Tactile Sensor with Application to In-Hand Manipulation"
authors: ["Lambeta, Mike","Chou, Po-Wei","Tian, Stephen","Yang, Brian","Maloon, Benjamin","Most, Victoria Rose","Stroud, Dave","Santos, Raymond","Byagowi, Ahmad","Kammerer, Gregg","Jayaraman, Dinesh","Calandra, Roberto"]
year: 2020
venue_or_status: "Author-deposited arXiv manuscript; final venue not asserted by this acquisition card."
primary_url: "https://arxiv.org/abs/2005.14679"
pdf_url: "https://arxiv.org/pdf/2005.14679"
local_pdf: "./2020-digit-tactile-sensor.pdf"
sha256: "dbcae130d003bcea9c4a61075458f3ea11597c60e029c18b88f254958fc97d14"
bytes: 7098575
pages: 8
topics: ["humanoid-dexterity-tactile","digit-tactile-sensor"]
modalities: ["proprioception","contacts","tactile","motion"]
track_role: "supporting"
open_access_status: "open-access-preprint"
redistribution_note: "Research copy only; verify the source license before redistribution."
execution_flow: {"title":"Core execution flow","description":"Follow the data through the mechanism. Training objectives and inference behavior are distinguished in the linked explanations.","nodes":[{"id":"stage-1","title":"Capture contact deformation","detail":"Observe elastomer appearance under contact.","column":0,"row":0,"section":"Capture contact deformation","problem_slugs":[],"planned_problems":["Validate a Tactile Image Capture Contract"]},{"id":"stage-2","title":"Extract tactile state","detail":"Use contact images or learned features for manipulation feedback.","column":1,"row":0,"section":"Extract tactile state","problem_slugs":[],"planned_problems":["Subtract a Tactile Reference Image","Estimate Contact Patch Statistics"]},{"id":"stage-3","title":"Predict and control contact","detail":"Use learned tactile dynamics to choose manipulation actions.","column":2,"row":0,"section":"Predict and control contact","problem_slugs":[],"planned_problems":["Align Tactile Frames with Robot Actions","Score Predicted Tactile Contact Outcomes"]}],"edges":[{"from":"stage-1","to":"stage-2","label":"tactile images"},{"from":"stage-2","to":"stage-3","label":"tactile state"}]}
---

## Core paper explanation

DIGIT is a compact vision-based tactile sensor: a camera observes an illuminated deformable elastomer as it contacts objects. The paper contributes sensor design and demonstrates tactile model-based manipulation, rather than claiming pixels directly measure calibrated contact force.

## Execution flow

Follow the data through the mechanism. Training objectives and inference behavior are distinguished in the linked explanations.

### Capture contact deformation

A tactile image can be modeled conceptually as $I=\mathcal R(\mathrm{deformation},\mathrm{lighting},\mathrm{optics})$. This is a teaching observation model. Material properties, illumination, and camera calibration affect the signal; image brightness is not force in newtons.


**Planned exercise:** Validate a Tactile Image Capture Contract.


### Extract tactile state

A simple diagnostic difference is $\Delta I_t=I_t-I_{\mathrm{reference}}$. It can highlight contact but also responds to lighting drift and sensor aging. Any mapping $\hat F=f_\theta(I)$ to physical force requires separate calibration and labels; it is not supplied automatically by the hardware.


**Planned exercise:** Subtract a Tactile Reference Image.

**Planned exercise:** Estimate Contact Patch Statistics.


### Predict and control contact

The demonstrated model-based control idea predicts future tactile observations $\hat I_{t+1}=f_\theta(I_t,a_t)$ and scores candidate actions against a desired tactile outcome. This equation expresses the interface, not a full reproduction of the paper's controller. Validate contact-state prediction and task success independently.


**Planned exercise:** Align Tactile Frames with Robot Actions.

**Planned exercise:** Score Predicted Tactile Contact Outcomes.


## Implement the components

Exercises are attached to the corresponding execution stages and mathematical explanations above. Runnable links implement only their stated component scope. Planned titles are original authoring ideas, not reviewed contracts, runnable tasks, or claims of a reproduced paper. They enter the approved curriculum only through blueprint review.

- **Capture contact deformation:** Validate a Tactile Image Capture Contract (planned).
- **Extract tactile state:** Subtract a Tactile Reference Image (planned); Estimate Contact Patch Statistics (planned).
- **Predict and control contact:** Align Tactile Frames with Robot Actions (planned); Score Predicted Tactile Contact Outcomes (planned).

## Why this matters on a robot

Tactile sensing can reveal contact and slip hidden from external cameras. Elastomer wear, contamination, and changes in illumination alter the measurement process and require ongoing calibration checks.

## Sources and scope

[Primary paper](https://arxiv.org/abs/2005.14679) · [Open-access manuscript](https://arxiv.org/pdf/2005.14679)

This is an original explanation of selected mechanisms. Equations use the notation defined here; simplified teaching models are identified explicitly. Small component exercises do not reproduce the paper's full experiments. The local PDF is a research reference; its redistribution terms remain those recorded in the metadata.
