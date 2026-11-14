---
schema_version: 1
paper_id: "2024-droid"
title: "DROID: A Large-Scale In-The-Wild Robot Manipulation Dataset"
authors: ["Khazatsky, Alexander","Pertsch, Karl","Nair, Suraj","Balakrishna, Ashwin","Dasari, Sudeep","Karamcheti, Siddharth","Nasiriany, Soroush","Srirama, Mohan Kumar","Chen, Lawrence Yunliang","Ellis, Kirsty","Fagan, Peter David","Hejna, Joey","Itkina, Masha","Lepert, Marion","Ma, Yecheng Jason","Miller, Patrick Tree","Wu, Jimmy","Belkhale, Suneel","Dass, Shivin","Ha, Huy","Jain, Arhan","Lee, Abraham","Lee, Youngwoon","Memmel, Marius","Park, Sungjae","Radosavovic, Ilija","Wang, Kaiyuan","Zhan, Albert","Black, Kevin","Chi, Cheng","Hatch, Kyle Beltran","Lin, Shan","Lu, Jingpei","Mercat, Jean","Rehman, Abdul","Sanketi, Pannag R","Sharma, Archit","Simpson, Cody","Vuong, Quan","Walke, Homer Rich","Wulfe, Blake","Xiao, Ted","Yang, Jonathan Heewon","Yavary, Arefeh","Zhao, Tony Z.","Agia, Christopher","Baijal, Rohan","Castro, Mateo Guaman","Chen, Daphne","Chen, Qiuyu","Chung, Trinity","Drake, Jaimyn","Foster, Ethan Paul","Gao, Jensen","Guizilini, Vitor","Herrera, David Antonio","Heo, Minho","Hsu, Kyle","Hu, Jiaheng","Irshad, Muhammad Zubair","Jackson, Donovon","Le, Charlotte","Li, Yunshuang","Lin, Kevin","Lin, Roy","Ma, Zehan","Maddukuri, Abhiram","Mirchandani, Suvir","Morton, Daniel","Nguyen, Tony","O'Neill, Abigail","Scalise, Rosario","Seale, Derick","Son, Victor","Tian, Stephen","Tran, Emi","Wang, Andrew E.","Wu, Yilin","Xie, Annie","Yang, Jingyun","Yin, Patrick","Zhang, Yunchu","Bastani, Osbert","Berseth, Glen","Bohg, Jeannette","Goldberg, Ken","Gupta, Abhinav","Gupta, Abhishek","Jayaraman, Dinesh","Lim, Joseph J","Malik, Jitendra","Martín-Martín, Roberto","Ramamoorthy, Subramanian","Sadigh, Dorsa","Song, Shuran","Wu, Jiajun","Yip, Michael C.","Zhu, Yuke","Kollar, Thomas","Levine, Sergey","Finn, Chelsea"]
year: 2024
venue_or_status: "Author-deposited arXiv manuscript; final venue not asserted by this acquisition card."
primary_url: "https://arxiv.org/abs/2403.12945"
pdf_url: "https://arxiv.org/pdf/2403.12945"
local_pdf: "./2024-droid.pdf"
sha256: "9e40a9c934ce78ea315d2c05593d60f9e18edf6dcd3785cd66439518965c3b07"
bytes: 9707714
pages: 26
topics: ["mlops-data-deployment","droid"]
modalities: ["datasets","model-artifacts","logs","metrics"]
track_role: "supporting"
open_access_status: "open-access-preprint"
redistribution_note: "Research copy only; verify the source license before redistribution."
execution_flow: {"title":"Core execution flow","description":"Follow the data through the mechanism. Training objectives and inference behavior are distinguished in the linked explanations.","nodes":[{"id":"stage-1","title":"Collect calibrated multi-view episodes","detail":"Record robot behavior together with synchronized sensor context.","column":0,"row":0,"section":"Collect calibrated multi-view episodes","problem_slugs":[],"planned_problems":["Audit Data and Calibration Lineage"]},{"id":"stage-2","title":"Validate physical contracts","detail":"Check data completeness, action semantics, and calibration transforms.","column":1,"row":0,"section":"Validate physical contracts","problem_slugs":["validate-robot-episodes"],"planned_problems":["Validate a Distributed Robot Episode"]},{"id":"stage-3","title":"Train and evaluate across environments","detail":"Measure whether diverse collection improves held-out behavior.","column":2,"row":0,"section":"Train and evaluate across environments","problem_slugs":[],"planned_problems":["Split Demonstrations by Scene and Collector"]}],"edges":[{"from":"stage-1","to":"stage-2","label":"recorded episodes"},{"from":"stage-2","to":"stage-3","label":"curated data"}]}
---

## Core paper explanation

DROID scales real-world robot demonstrations through distributed collection across diverse environments. Its episodes include multiple camera streams, calibration, robot state/action information, and language descriptions, making data quality and provenance central interfaces.

## Execution flow

Follow the data through the mechanism. Training objectives and inference behavior are distinguished in the linked explanations.

### Collect calibrated multi-view episodes

For camera observation time $t_c$ and action time $t_a$, record $\Delta t=t_c-t_a$ rather than assuming array index equality means simultaneity. Preserve camera intrinsics, extrinsics, robot configuration, and collection-session identity.


**Component practice**

- Audit Data and Calibration Lineage — unreviewed idea; contract and evaluator required.

### Validate physical contracts

A calibration chain maps a camera point to the robot base:
$$p_B=T_{BC}p_C.$$
Translations use meters and rotation conventions must be declared. Validate timestamps, finite values, episode boundaries, and supported control modes before producing training windows.


**Component practice**

- Supporting prerequisite: [Validate a Multimodal Robot Episode Schema](/problems/validate-robot-episodes). Practices the stated data or mathematical operation; it does not implement this paper-specific stage in full.
- Validate a Distributed Robot Episode — unreviewed idea; contract and evaluator required.

### Train and evaluate across environments

A teaching site-held-out evaluation separates $D_{\mathrm{train}}\cap D_{\mathrm{test}}=\varnothing$ at the collection-environment level, not merely by frame. Report adaptation data and task success for each held-out condition. The dataset supports multiple learning methods rather than defining one universal training loss.


**Component practice**

- Split Demonstrations by Scene and Collector — unreviewed idea; contract and evaluator required.

## Implement the components

Each execution-flow node links the matching runnable component or names its planned problem. Planned titles are not runnable; labels distinguish reviewed drafts from unreviewed ideas.

- **Supporting prerequisite:** [Validate a Multimodal Robot Episode Schema](/problems/validate-robot-episodes).

**Planned component problems:**

- Audit Data and Calibration Lineage — unreviewed idea; contract and evaluator required.
- Validate a Distributed Robot Episode — unreviewed idea; contract and evaluator required.
- Split Demonstrations by Scene and Collector — unreviewed idea; contract and evaluator required.

These bounded exercises do not claim to reproduce the complete paper or its benchmark results.

## Why this matters on a robot

Distributed collection expands real-world coverage. Calibration drift, operator style, and repeated environments can bias a large dataset; more trajectories do not remove the need for careful splits and physical metadata.

## Sources and scope

[Primary paper](https://arxiv.org/abs/2403.12945) · [Open-access manuscript](https://arxiv.org/pdf/2403.12945)

This is an original explanation of selected mechanisms. Equations use the notation defined here; simplified teaching models are identified explicitly. Small component exercises do not reproduce the paper's full experiments. The local PDF is a research reference; its redistribution terms remain those recorded in the metadata.
