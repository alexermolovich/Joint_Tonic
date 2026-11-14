# Worked examples

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

These examples use original synthetic fixtures. Hidden tests will exercise the same documented rules with different inputs.

