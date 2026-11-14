## Worked examples

1. Let T_base_wrist translate `[1,0,0]` and T_wrist_camera translate `[0,2,0]`. Resolving source="camera", target="base" returns translation `[1,2,0]` with identity rotation.
2. Reversing those query frames returns translation `[-1,-2,0]`. A known frame to itself returns identity.
