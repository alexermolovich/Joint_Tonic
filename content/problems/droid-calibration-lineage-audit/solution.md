# Solution explanation

Validate every calibration record first and index it by calibration_id. Validate episodes, report only unknown_calibration for unresolved references, and otherwise compare robot, session, digest and complete half-open interval coverage independently. Retain timestamps as integers. Work O(E+C+I log I), where I is reported issue count; storage O(E+C+I).
