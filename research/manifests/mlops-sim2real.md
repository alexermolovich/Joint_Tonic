# Physical AI MLOps, Deployment, Data, and Sim-to-Real Papers

Last verified: 2026-11-13

## Scope and selection rationale

This is a curated starter set, not a claim to contain every relevant paper. It emphasizes the operational layer that turns a robotics model into a maintainable physical-AI system:

- production ML architecture, testing, monitoring, and data validation;
- reproducible robot datasets and cross-robot data normalization;
- measurable, hardware-aware inference and robotics compute benchmarking; and
- visual and dynamics randomization for simulation-to-real transfer.

The set intentionally mixes foundational systems papers with robotics-specific data and deployment work. Each paper can support small, testable coding problems before it becomes a full paper-reproduction track. Before serving these PDFs from a public website, review each publisher's redistribution terms; open access for reading does not automatically grant every form of republication.

Every PDF has a same-basename Markdown paper card beside it. Those cards are the agent-facing source for original theory pages: verified metadata, an implementation decomposition, essential equations where appropriate, executable problem blueprints, and a visual teaching plan. The cards summarize and interpret the work; they do not transcribe the papers.

## Classification tags

| Tag | Meaning |
| --- | --- |
| `mlops-foundations` | System design, dependency risk, lifecycle architecture, or production-readiness practices |
| `data-quality` | Schema inference, anomaly detection, skew detection, dataset quality, or lineage |
| `robot-data` | Demonstration datasets, embodiment normalization, sampling, or offline evaluation |
| `inference-systems` | Compilers, model specialization, latency, throughput, memory, or hardware portability |
| `benchmarking` | Reproducible workload definitions, measurement rules, auditability, or robotics compute evaluation |
| `sim-to-real` | Randomization and robustness methods for crossing visual or dynamics reality gaps |
| `monitoring-safety` | Tests and gates that prevent degraded or unready models from deployment |

## Paper catalog and problem map

| Paper | Year | Authors | Venue / status | Tags | Primary landing page | Direct PDF | Local path | Contribution | Candidate coding problems |
| --- | ---: | --- | --- | --- | --- | --- | --- | --- | --- |
| Hidden Technical Debt in Machine Learning Systems | 2015 | D. Sculley, Gary Holt, Daniel Golovin, Eugene Davydov, Todd Phillips, Dietmar Ebner, Vinay Chaudhary, Michael Young, Jean-Francois Crespo, Dan Dennison | NeurIPS 2015 | `mlops-foundations`, `monitoring-safety` | [NeurIPS proceedings](https://proceedings.neurips.cc/paper/2015/hash/86df7dcfd896fcaf2674f757a2463eba-Abstract.html) | [PDF](https://proceedings.neurips.cc/paper_files/paper/2015/file/86df7dcfd896fcaf2674f757a2463eba-Paper.pdf) | `research/papers/mlops-sim2real/2015-hidden-technical-debt.pdf` | Defines ML-specific system debt such as data dependencies, feedback loops, glue code, and undeclared consumers. | Compute dependency-graph blast radius; detect feedback loops in a pipeline DAG; score a toy system against named debt risks. |
| TFX: A TensorFlow-Based Production-Scale Machine Learning Platform | 2017 | Denis Baylor, Eric Breck, Heng-Tze Cheng, Noah Fiedel, Chuan Yu Foo, Zakaria Haque, Salem Haykal, Mustafa Ispir, Vihan Jain, Levent Koc, Chiu Yuen Koo, Lukasz Lew, Clemens Mewald, Akshay Naresh Modi, Neoklis Polyzotis, Sukriti Ramesh, Sudip Roy, Steven Euijong Whang, Martin Wicke, Jarek Wilkiewicz, Xin Zhang, Martin Zinkevich | KDD 2017 | `mlops-foundations`, `data-quality`, `monitoring-safety` | [Google Research](https://research.google/pubs/tfx-a-tensorflow-based-production-scale-machine-learning-platform/) | [PDF](https://storage.googleapis.com/gweb-research2023-media/pubtools/4795.pdf) | `research/papers/mlops-sim2real/2017-tfx-production-ml-platform.pdf` | Presents an integrated continuous-training platform spanning data analysis, transformation, validation, training, evaluation, and serving. | Topologically schedule a pipeline DAG; implement artifact lineage and cache invalidation; enforce identical train/serve transforms. |
| The ML Test Score: A Rubric for ML Production Readiness and Technical Debt Reduction | 2017 | Eric Breck, Shanqing Cai, Eric Nielsen, Michael Salib, D. Sculley | IEEE Big Data 2017 | `mlops-foundations`, `monitoring-safety` | [Google Research](https://research.google/pubs/the-ml-test-score-a-rubric-for-ml-production-readiness-and-technical-debt-reduction/) | [PDF](https://storage.googleapis.com/gweb-research2023-media/pubtools/4156.pdf) | `research/papers/mlops-sim2real/2017-ml-test-score.pdf` | Converts production readiness into concrete data, model, infrastructure, and monitoring tests. | Calculate a weighted production-readiness score; gate a deployment on slice regressions; trigger alerts for stale features or stale models. |
| Data Validation for Machine Learning | 2019 | Eric Breck, Marty Zinkevich, Neoklis Polyzotis, Steven Whang, Sudip Roy | SysML 2019 | `data-quality`, `monitoring-safety` | [Google Research](https://research.google/pubs/data-validation-for-machine-learning/) | [PDF](https://mlsys.org/Conferences/2019/doc/2019/167.pdf) | `research/papers/mlops-sim2real/2019-data-validation-for-ml.pdf` | Describes scalable schema-based anomaly detection and training-serving skew checks for continuously changing ML data. | Infer a schema from robot episodes; flag missing/range/domain anomalies; compare train and serving distributions with a skew threshold. |
| TVM: An Automated End-to-End Optimizing Compiler for Deep Learning | 2018 | Tianqi Chen, Thierry Moreau, Ziheng Jiang, Lianmin Zheng, Eddie Yan, Haichen Shen, Meghan Cowan, Leyuan Wang, Yuwei Hu, Luis Ceze, Carlos Guestrin, Arvind Krishnamurthy | OSDI 2018 | `inference-systems` | [USENIX](https://www.usenix.org/conference/osdi18/presentation/chen) | [PDF](https://www.usenix.org/system/files/osdi18-chen.pdf) | `research/papers/mlops-sim2real/2018-tvm.pdf` | Combines graph optimization, tensor scheduling, and learned cost models for portable inference across CPUs, GPUs, embedded devices, and accelerators. | Fuse compatible operators in a graph; search tile sizes with a toy cost model; plan tensor-buffer reuse under liveness constraints. |
| MLPerf Inference Benchmark | 2019 | Vijay Janapa Reddi et al. (MLPerf consortium) | arXiv 2019; industry benchmark paper | `benchmarking`, `inference-systems` | [arXiv](https://arxiv.org/abs/1911.02549) | [PDF](https://arxiv.org/pdf/1911.02549) | `research/papers/mlops-sim2real/2019-mlperf-inference.pdf` | Defines representative workloads, scenarios, quality targets, load generation, and audit rules for comparable inference measurements. | Compute p50/p90/p99 latency and throughput; simulate single-stream versus server load; reject benchmark runs that miss quality or latency constraints. |
| Once-for-All: Train One Network and Specialize it for Efficient Deployment | 2020 | Han Cai, Chuang Gan, Tianzhe Wang, Zhekai Zhang, Song Han | ICLR 2020 | `inference-systems` | [arXiv](https://arxiv.org/abs/1908.09791) | [PDF](https://arxiv.org/pdf/1908.09791) | `research/papers/mlops-sim2real/2020-once-for-all.pdf` | Trains a weight-sharing supernet and selects hardware-specific subnetworks without retraining each target model. | Extract a depth/width/kernel subnetwork; sample a progressive-shrinking curriculum; find a Pareto-optimal subnetwork under latency and accuracy constraints. |
| RobotPerf: An Open-Source, Vendor-Agnostic, Benchmarking Suite for Evaluating Robotics Computing System Performance | 2023 | Victor Mayoral-Vilches et al. | arXiv 2023; open benchmark suite | `benchmarking`, `inference-systems` | [arXiv](https://arxiv.org/abs/2309.09212) | [PDF](https://arxiv.org/pdf/2309.09212) | `research/papers/mlops-sim2real/2023-robotperf.pdf` | Adapts black-box and grey-box benchmarking to ROS 2 computational graphs and complete robotics pipelines. | Derive end-to-end latency from trace events; compute throughput and jitter for a ROS-style graph; compare black-box and grey-box measurements. |
| What Matters in Learning from Offline Human Demonstrations for Robot Manipulation | 2021 | Ajay Mandlekar, Danfei Xu, Josiah Wong, Soroush Nasiriany, Chen Wang, Rohun Kulkarni, Li Fei-Fei, Silvio Savarese, Yuke Zhu, Roberto Martin-Martin | CoRL 2021 (PMLR proceedings 2022) | `robot-data`, `benchmarking` | [arXiv](https://arxiv.org/abs/2108.03298) | [PDF](https://arxiv.org/pdf/2108.03298) | `research/papers/mlops-sim2real/2021-robomimic.pdf` | Establishes reproducible datasets and evaluation lessons for offline imitation learning from mixed-quality human robot demonstrations. | Create trajectory-safe train/validation splits; batch variable-length episodes with masks; select checkpoints when validation loss and rollout success disagree. |
| Open X-Embodiment: Robotic Learning Datasets and RT-X Models | 2024 | Open X-Embodiment Collaboration (Abby O'Neill et al.) | IEEE ICRA 2024 | `robot-data`, `data-quality` | [arXiv](https://arxiv.org/abs/2310.08864) | [PDF](https://arxiv.org/pdf/2310.08864) | `research/papers/mlops-sim2real/2024-open-x-embodiment.pdf` | Standardizes data from many robot embodiments and demonstrates cross-robot transfer with large shared policy models. | Normalize heterogeneous action spaces; sample a balanced multi-dataset training mixture; compute per-embodiment and transfer evaluation summaries. |
| Domain Randomization for Transferring Deep Neural Networks from Simulation to the Real World | 2017 | Josh Tobin, Rachel Fong, Alex Ray, Jonas Schneider, Wojciech Zaremba, Pieter Abbeel | IEEE/RSJ IROS 2017 | `sim-to-real`, `data-quality` | [arXiv](https://arxiv.org/abs/1703.06907) | [PDF](https://arxiv.org/pdf/1703.06907) | `research/papers/mlops-sim2real/2017-domain-randomization.pdf` | Shows that randomized simulator visuals can train perception that transfers to real robot manipulation without real-image pretraining. | Build a deterministic randomization sampler; generate stratified texture/light/camera configurations; measure accuracy across synthetic-to-real shift buckets. |
| Sim-to-Real Transfer of Robotic Control with Dynamics Randomization | 2018 | Xue Bin Peng, Marcin Andrychowicz, Wojciech Zaremba, Pieter Abbeel | IEEE ICRA 2018 | `sim-to-real`, `monitoring-safety` | [arXiv](https://arxiv.org/abs/1710.06537) | [PDF](https://arxiv.org/pdf/1710.06537) | `research/papers/mlops-sim2real/2018-dynamics-randomization.pdf` | Trains policies over randomized physical dynamics so they remain robust to calibration error and unseen real-world dynamics. | Sample mass/friction/delay distributions; aggregate worst-case and mean policy returns; quantify calibration sensitivity and choose safe randomization bounds. |

## Recommended prerequisite order

The papers can become four parallel study tracks after a shared MLOps foundation:

1. Start with **Hidden Technical Debt** to establish failure modes and vocabulary.
2. Continue with **TFX**, **The ML Test Score**, and **Data Validation for Machine Learning** to build pipeline, gating, and monitoring exercises.
3. For robot data, do **robomimic** before **Open X-Embodiment**. The first introduces episode quality and offline evaluation; the second adds heterogeneous embodiments and large-scale mixture design.
4. For deployment, do **MLPerf Inference** before **TVM** and **Once-for-All**, then finish with **RobotPerf**. This introduces correct measurement before optimization and finally integrates the metrics into robotics graphs.
5. For sim-to-real, do visual **Domain Randomization** before **Dynamics Randomization**. Both should reuse the data-validation and benchmark utilities from steps 2 and 4.

## Suggested first implementation tracks

### Track A: Production-ready robot policy

1. Robot episode schema inference.
2. Training/serving skew detection.
3. Pipeline DAG execution and artifact lineage.
4. Production-readiness score and deployment gate.
5. Model staleness and slice-regression monitor.

### Track B: Edge perception deployment

1. Benchmark scenario and latency statistics.
2. Graph fusion and buffer-liveness planning.
3. Hardware-aware subnetwork selection.
4. End-to-end robotics graph trace analysis.

### Track C: Cross-robot data engine

1. Variable-length episode batching.
2. Action-space normalization.
3. Balanced mixture sampling.
4. Per-embodiment metrics and transfer matrix.

### Track D: Sim-to-real reliability

1. Seeded visual randomization.
2. Dynamics-parameter sampling.
3. Robust return aggregation.
4. Calibration sensitivity report and release gate.

## Local PDF verification

Each file below was downloaded from the listed direct source, begins with `%PDF-`, opens successfully with Poppler `pdfinfo`, has a nonzero page count, and has a same-basename `.md` paper card.

| File | Bytes | Pages | SHA-256 |
| --- | ---: | ---: | --- |
| `2015-hidden-technical-debt.pdf` | 165614 | 9 | `1a67da09a8bd5ba9a3577176e30aa2fbd88534e6baf0bc31522b4999f643d2a1` |
| `2017-domain-randomization.pdf` | 4066798 | 8 | `3fc98c5f4cea050686d45858e647e1b704492121fdae80f8fcd5d560c107f11f` |
| `2017-ml-test-score.pdf` | 500055 | 10 | `8db5862dc7c7aaa2c55bb43bd42fc55531a0503782b7026b5811c00c98befd31` |
| `2017-tfx-production-ml-platform.pdf` | 826419 | 9 | `05b0236e9871214b0b790c332015e91c05b3542b0a36487b1848912603618ddb` |
| `2018-dynamics-randomization.pdf` | 2845918 | 8 | `a15cb24630a11218865027024ae2353f80f46d40371b42dccb2b24e9d00d62d8` |
| `2018-tvm.pdf` | 1292153 | 17 | `0ddc28deb2d66ce460d019588ea326ce59bb08290dad09bc2f6ca372b64333c6` |
| `2019-data-validation-for-ml.pdf` | 435587 | 14 | `4c26718460681e3cd8a2be65308f85352af1be46aef84cf749903f9387381f53` |
| `2019-mlperf-inference.pdf` | 1185996 | 15 | `ab71faac2c06fa5c317f559e3e96c7baa24a7d15bcf757efcee085ee1a3a1efd` |
| `2020-once-for-all.pdf` | 3616911 | 15 | `ed04dfd495ca56610bf19a6ae6a9974489ff0e9720a3349a47a3abc009c3935f` |
| `2021-robomimic.pdf` | 10782355 | 36 | `18283ff9cbb9645de4ccf32ca2de472f452e89761287e7ed578e3a1066bea5f1` |
| `2023-robotperf.pdf` | 2271155 | 9 | `fd61fd4331f547382bcc0063221c13f11c8c6953848c95eab1249e6ca71418b9` |
| `2024-open-x-embodiment.pdf` | 4011306 | 12 | `13f16aff5afdee583dc25b3c570e9bb0cf6baefb59b539928d919588cd8d9246` |

