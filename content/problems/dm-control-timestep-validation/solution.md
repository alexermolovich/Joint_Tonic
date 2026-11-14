# Solution explanation

Validate the outer bounded dictionary, accumulate missing and unexpected field issues, then check present fields. Validate reward/discount only when step_type is valid, retaining missing-field reports independently. Sort the final issues. Work O(D+F log F), with D observation coordinates and bounded F fields.
