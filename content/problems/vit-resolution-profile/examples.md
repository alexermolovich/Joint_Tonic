# Worked examples

1. Resolution (4,4),patch2,heads2,float32(4 bytes): L=5, score storage=2*25*4=200 bytes. Measurements `[1,2,3,4]` ms have nearest-rank p95=4 ms.
2. Resolution (8,8) under the same settings gives L=17 and 2312 bytes. Quadrupling patch count from4 to16 grows this tensor by2312/200, not4.
