# Mix Web and Robot Batches at a Target Ratio

## Intuition

Co-training mixes robot examples with web supervision, but a ratio alone does not specify finite batch rounding or what happens when a source is small. Make those decisions explicit so training is reproducible.

## Mathematical mechanism

For batch size B and target robot fraction r, use 

$$n_R=\lfloor Br+0.5\rfloor$$

 and $n_W=B-n_R$. Source-local position i selects $\mathrm{IDs}[i\bmod N]$ from its N available IDs. Achieved ratio $n_R/B$ can differ from r because examples are indivisible. The two sources keep distinct labels because their losses and physical semantics can differ.

## Visual computation trace

| B=5,r=0.5 | Quota | Source IDs | Emitted IDs |
|---|---|---|---|
| robot | 3 | [8,9] | [8,9,8] |
| web | 2 | [2] | [2,2] |

The table is the static visual and its text alternative; each row describes a transformation or decision.

## Worked calculation

web_ids=[2], robot_ids=[8,9], robot_fraction=0.5, batch_size=5 returns source=[1,1,1,0,0], ids=[8,9,8,2,2].

## Why this matters on a robot

Rounding each source independently can produce the wrong total batch size. Cycling small datasets also increases repeated exposure, so log achieved source counts and do not mistake a prescribed mixture for equal semantic diversity.

## Physical contract and limits

Dataset IDs/source labels and ratios are dimensionless; no common raw action space is assumed. This is one training batch assembly; per-source sequence order remains external. Original deterministic co-training mixer inspired by RT-2. Half-up rounding, source order and cycling are teaching rules rather than the paper’s training sampler.

Source: [primary paper](https://arxiv.org/abs/2307.15818). Prerequisite: understand the observation/action schema supplied in the contract; no additional lesson is required.
