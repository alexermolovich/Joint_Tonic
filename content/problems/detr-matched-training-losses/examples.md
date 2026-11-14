# Worked examples

1. One query,one real class,zero logits,identical predicted/target box,assignment[0]: classification=ln2,l1=giou=0,total=ln2.
2. Prediction center(0.25,0.5),size(0.5,1),target center(0.75,0.5),same size: boxes touch,so IoU=GIoU=0,l1=0.5,giou loss1. With zero two-class logits,total=ln2+2.5+2.
