# Worked examples

1. World point `[[0.,0.,1.]]`, observed pixel `[[1.,0.]]`, identity pose, intrinsics `[1.,1.,0.,0.]`, std 1 and threshold 1: normalized squared error 1 and one inlier.
2. Add a second pose with camera-from-world x translation +1 m. Its projected pixel is `[1.,0.]`, giving zero error. Both hypotheses have one inlier, so the second pose wins on median error.
