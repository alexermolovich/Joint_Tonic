## Example 1

web_ids=[2], robot_ids=[8,9], robot_fraction=0.5, batch_size=5 returns source=[1,1,1,0,0], ids=[8,9,8,2,2].

## Example 2

web_ids=[4,5], robot_ids=empty int vector, robot_fraction=0, batch_size=3 returns source=[0,0,0], ids=[4,5,4]. An unused empty source is valid.
