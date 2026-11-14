# Solution explanation

Map exact task and seed IDs to compact sorted axes. Accumulate cell counts and float64 sums, divide measured cells, and average each row over its measured cells. Average the row means equally. Work O(E log E+MS), storage O(E+MS).
