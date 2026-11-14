# Solution explanation

Validate every supplied summary before computing any rejection. Index records by slice; sort the required IDs and append all failing reasons in the declared order. Missing summaries get one missing reason. Work O(S log S), storage O(S); no automatic deployment or certification.
