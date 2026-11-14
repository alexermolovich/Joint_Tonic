# Worked examples

## Example 1: inverse lookup shifts sampled columns

~~~python
previous = np.array([[[1.],[2.],[3.]], [[4.],[5.],[6.]]])
previous_from_current = np.array([[1.,0.,1.],[0.,1.,0.],[0.,0.,1.]])
warp_previous_bev(previous,previous_from_current,1.,np.zeros(2))
# array([[[2.],[3.],[0.]], [[5.],[6.],[0.]]])
~~~

Each current cell asks for a location one metre farther along previous-frame x. A forward-scatter implementation would shift in the opposite direction.

## Example 2: partial border weights remain partial

~~~python
previous_from_current = np.array([[1.,0.,0.5],[0.,1.,0.],[0.,0.,1.]])
warp_previous_bev(previous,previous_from_current,1.,np.zeros(2))
# array([[[1.5],[2.5],[1.5]], [[4.5],[5.5],[3.]]])
~~~

The final output column samples halfway between the final stored column and a zero neighbor. It is neither clamped to the last value nor discarded entirely.

