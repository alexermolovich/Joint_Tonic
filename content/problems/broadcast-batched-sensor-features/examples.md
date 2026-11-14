# Worked examples

### Mask the entire absent sample
sensor[[[2],[3]]], context[[9]], present[[True,False]] returns[[[2,9],[0,0]]].

### Two different robots
sensor[[[1]],[[2]]], context[[10,11],[20,21]], present[[True],[True]] returns[[[1,10,11]],[[2,20,21]]].
