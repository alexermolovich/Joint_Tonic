# Balance a Multi-Dataset Training Mixture

Implement allocate_dataset_batch(weights: dict[str,int], batch_size: int) -> dict[str,int].

weights has1–10,000 dataset IDs matching ASCII [a-z][a-z0-9_-]{0,63}, mapped to built-in non-bool integer weights in[0,10**12]. At least one weight is positive. batch_size is a built-in non-bool int in[0,1,000,000]. Empty/all-zero weights are invalid even for batch_size0.

Let W=sum(weights). For each dataset i compute base_i=(batch_size*weight_i)//W and remainder_i=(batch_size*weight_i)%W with exact integer arithmetic. Let R=batch_size-sum(base_i). Give one additional item to each of the first R datasets sorted by descending remainder_i then ASCII ID. No dataset receives more than one remainder item.

Return every ID, including zero-weight IDs, with its allocated built-in int count. Dictionary insertion order must be ASCII ID order. Counts are nonnegative and sum exactly to batch_size; input dictionary remains unchanged. A zero-sized batch returns all IDs with zero counts. No random sampling, file loading, replacement policy or floating normalization occurs. Dataset weights are configured influence, not inferred from file counts. All malformed types, IDs, bounds or zero-total configurations raise ValueError.

## Worked examples

### Two items cannot split equally across three datasets

~~~python
allocate_dataset_batch({"c":1,"a":1,"b":1},2)
# {"a":1,"b":1,"c":0}
~~~

Each ideal quota is2/3. All remainders tie; ASCII IDs a and b receive the two items.

### Unequal weights preserve the largest remainder

~~~python
allocate_dataset_batch({"large":30,"small":10,"disabled":0},5)
# {"disabled":0,"large":4,"small":1}
~~~

Ideal quotas are3.75 and1.25. Bases3 and1 leave one item, assigned to large's remainder30 rather than small's10.

## Source and scope

Open X-Embodiment motivates deliberate mixture composition. Hamilton largest-remainder allocation is an original deterministic batch-construction exercise, not a claim that RT-X uses this exact sampler. [Primary source](https://arxiv.org/abs/2310.08864).

