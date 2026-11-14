# Worked examples

1. One occupied cell/predictor/class with identical boxes, confidence1,target_iou1,class_probability1 gives all losses0.
2. S=1,B=2,C=2, responsible0,target class0. Responsible width0.25 versus target width1 (all other coordinates equal) gives coordinate1.25. Confidences[0.5,0.2],target_iou1 give objectness0.25+0.02=0.27. Class probabilities[0.8,0.2] give0.08. Total1.60.
