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
---

# DROID: A Large-Scale In-The-Wild Robot Manipulation Dataset

## Agent brief

Study a distributed robot-demonstration dataset through its calibration, episode, and evaluation contracts. This acquisition card verifies the primary paper identity and local PDF, and proposes components that can become independently testable Joint Tonic problems. Full-text technical review is required before promoting an idea into a reviewed problem blueprint.

## Contribution

Study a distributed robot-demonstration dataset through its calibration, episode, and evaluation contracts.

The proposed exercises below are original teaching decompositions. They do not assert a full reproduction of the paper or any published performance number.

## Prerequisite concepts

- Versioned artifacts, data schemas, deterministic splits, latency percentiles, and release gates.

## Method map

| Component candidate | Input | Output | Core invariant | Good exercise boundary |
|---|---|---|---|---|
| Validate a Distributed Robot Episode | Versioned dataset records, artifact metadata, calibration records, or benchmark samples | Validated records, dependency decisions, compressed tensors, or reproducible evaluation reports | Check deterministic ordering, duplicate handling, missing metadata, leakage boundaries, threshold equality, and invalid measurement windows. | One bounded function or validation stage |
| Split Demonstrations by Scene and Collector | Versioned dataset records, artifact metadata, calibration records, or benchmark samples | Validated records, dependency decisions, compressed tensors, or reproducible evaluation reports | Check deterministic ordering, duplicate handling, missing metadata, leakage boundaries, threshold equality, and invalid measurement windows. | One bounded function or validation stage |
| Audit Data and Calibration Lineage | Versioned dataset records, artifact metadata, calibration records, or benchmark samples | Validated records, dependency decisions, compressed tensors, or reproducible evaluation reports | Check deterministic ordering, duplicate handling, missing metadata, leakage boundaries, threshold equality, and invalid measurement windows. | One bounded function or validation stage |

## Data and evaluation

A small teaching implementation should use synthetic or separately licensed fixtures. Check deterministic ordering, duplicate handling, missing metadata, leakage boundaries, threshold equality, and invalid measurement windows. Dataset names, exact protocol details, published metrics, and hardware requirements must be checked in the source PDF during full-text review; they are not inferred from an awesome-list entry. Keep educational component tests distinct from the paper's end-to-end evaluation.

## Limitations and failure modes

- This is a concise acquisition card, not a full-text technical review. Confirm equations, architecture details, and paper-stated limitations in the PDF before authoring theory.
- Passing synthetic component tests does not establish real-robot performance, robustness, or safe deployment.
- Make every report reproducible from code, data, preprocessing, runtime, and hardware identifiers; separate data/model regressions from platform failures.
- The paper, linked code, datasets, assets, and weights may carry different license conditions.

## Implementation decomposition

1. Validate a Distributed Robot Episode.
2. Split Demonstrations by Scene and Collector.
3. Audit Data and Calibration Lineage.
4. Integrate the components on a small fixed fixture and record all deviations from the paper.
5. Add failure slices and a reproducible artifact report.

## Problem blueprints

### Problem: Validate a Distributed Robot Episode

- **Type:** component
- **Difficulty:** medium
- **Learning objective:** Implement and explain the validate a distributed robot episode component.
- **Inputs:** Versioned dataset records, artifact metadata, calibration records, or benchmark samples; finalize exact shapes, dtypes, units, frames, masks, and valid ranges during blueprint review.
- **Outputs:** Validated records, dependency decisions, compressed tensors, or reproducible evaluation reports; specify order and mutation semantics in the reviewed blueprint.
- **Fixture:** Original synthetic examples; any paper dataset requires separate license and split review.
- **Grading:** Check deterministic ordering, duplicate handling, missing metadata, leakage boundaries, threshold equality, and invalid measurement windows. Add at least two public cases plus hidden tests for documented edge families.
- **Paper deviation:** Isolate one mechanism with bounded arrays or recorded trajectories; no claim of full-scale paper reproduction.

### Problem: Split Demonstrations by Scene and Collector

- **Type:** component
- **Difficulty:** hard
- **Learning objective:** Implement and explain the split demonstrations by scene and collector component.
- **Inputs:** Versioned dataset records, artifact metadata, calibration records, or benchmark samples; finalize exact shapes, dtypes, units, frames, masks, and valid ranges during blueprint review.
- **Outputs:** Validated records, dependency decisions, compressed tensors, or reproducible evaluation reports; specify order and mutation semantics in the reviewed blueprint.
- **Fixture:** Original synthetic examples; any paper dataset requires separate license and split review.
- **Grading:** Check deterministic ordering, duplicate handling, missing metadata, leakage boundaries, threshold equality, and invalid measurement windows. Add at least two public cases plus hidden tests for documented edge families.
- **Paper deviation:** Isolate one mechanism with bounded arrays or recorded trajectories; no claim of full-scale paper reproduction.

### Problem: Audit Data and Calibration Lineage

- **Type:** pipeline
- **Difficulty:** hard
- **Learning objective:** Implement and explain the audit data and calibration lineage component.
- **Inputs:** Versioned dataset records, artifact metadata, calibration records, or benchmark samples; finalize exact shapes, dtypes, units, frames, masks, and valid ranges during blueprint review.
- **Outputs:** Validated records, dependency decisions, compressed tensors, or reproducible evaluation reports; specify order and mutation semantics in the reviewed blueprint.
- **Fixture:** Original synthetic examples; any paper dataset requires separate license and split review.
- **Grading:** Check deterministic ordering, duplicate handling, missing metadata, leakage boundaries, threshold equality, and invalid measurement windows. Add at least two public cases plus hidden tests for documented edge families.
- **Paper deviation:** Isolate one mechanism with bounded arrays or recorded trajectories; no claim of full-scale paper reproduction.

## Visual teaching plan

- Show collection sites and episode metadata with split and calibration warnings.
- Provide labeled axes, units, coordinate frames, and an equivalent table/text view. Use discrete steps when reduced motion is requested.
- Author diagrams independently; do not copy paper figures or captions.

## MLOps and deployment extensions

- Make every report reproducible from code, data, preprocessing, runtime, and hardware identifiers; separate data/model regressions from platform failures.
- Store paper ID, fixture hash, evaluator version, dependency lock, runtime digest, seed, and resource class with every result.
- Use structured failure reasons and per-slice metrics to distinguish implementation mistakes, distribution shifts, and infrastructure failures.

## Canonical sources

- [Primary arXiv record](https://arxiv.org/abs/2403.12945)
- [Open-access author manuscript](https://arxiv.org/pdf/2403.12945)

Identity metadata was read from the primary arXiv record. Local file signature, byte count, page parsing, and SHA-256 were verified on acquisition.

