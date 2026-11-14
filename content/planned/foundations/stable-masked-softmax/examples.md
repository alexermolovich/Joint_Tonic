# Worked examples

### Large equal valid logits
logits[[1000,1000,-1000]], valid[[True,True,False]] returns[[0.5,0.5,0]].

### Missing versus one available token
logits[[1,2],[5,9]], valid[[False,False],[True,False]] returns[[0,0],[1,0]].
