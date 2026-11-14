# Worked inputs and expected outcomes

## Example 1: a straight arm

`lengths=[1,0.5]`, `q=[0,0]`.

Expected origins: `[[0,0],[1,0],[1.5,0]]`. Expected tool pose: `[[1,0,1.5],[0,1,0],[0,0,1]]`.

Both local +x axes coincide with base +x.

## Example 2: an elbow cancels the shoulder orientation

`lengths=[1,0.5]`, `q=[pi/2,-pi/2]`.

Expected origins, within floating tolerance: `[[0,0],[0,1],[0.5,1]]`. Expected tool pose: `[[1,0,0.5],[0,1,1],[0,0,1]]`.

The shoulder turns the first link upward. The elbow's relative negative turn restores the second link's absolute orientation to zero.
