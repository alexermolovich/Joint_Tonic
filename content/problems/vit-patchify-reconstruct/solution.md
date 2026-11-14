# Solution

Validate the explicit image shape and patch size, then separate H and W into grid and within-patch axes. Transpose B,C,gridH,P,gridW,P to B,gridH,gridW,C,P,P before flattening. The inverse transposes those axes back. A final copy guarantees independent storage even for P=1 or a single patch. Both operations take O(BCHW) time and output memory; no pixel arithmetic is needed.
