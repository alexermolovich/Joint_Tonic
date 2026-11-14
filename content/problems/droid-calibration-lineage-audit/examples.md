# Worked examples

Calibration k(session s, robot r, hash"1"*64, valid[0,10)) and episode a(s, r, k, samehash,[0,10)) yields[].

The same calibration with episode b(session other, robot r, k, hash"2"*64,[9,11)) yields[(b,"digest_mismatch"),(b,"session_mismatch"),(b,"validity_gap")].
