# Solution explanation

Hash the supplied bytes and reject any expected-digest mismatch. Validate the exact metadata schema before canonical serialization. Hash the three-field manifest before adding its own digest, then return independent metadata. Work/storage O(byte count + metadata size). This establishes content identity, not authenticity or validity of an executable model.
