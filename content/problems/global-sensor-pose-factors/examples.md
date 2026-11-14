# Worked examples

1. Body and sensor transforms are identity. GPS [1,2,3], magnetic [1,0,0], world field [1,0,0], height 4, all standard deviations 1 and all sensors available give raw [1,2,3,0,0,0,4] and cost 15.
2. The body is identity; the sensor has translation [1,0,0] and a 90-degree z rotation. GPS [1,0,0], sensor magnetic [0,-2,0], world field [5,0,0], and height 0 give zero residuals.
