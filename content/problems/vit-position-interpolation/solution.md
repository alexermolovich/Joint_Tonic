# Solution

Separate the class row, reshape patch positions from the row-major sequence into H0×W0×D, and permute to channels-first format. Apply the pinned bicubic interpolation with align_corners=False and antialias=False, restore row-major sequence order, and concatenate the unchanged class row. Concatenation allocates independent storage and keeps both branches connected to autograd. Work is linear in D times the input and output spatial sizes.
