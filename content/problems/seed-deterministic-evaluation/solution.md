# Solution explanation

Derive one local SeedSequence from root seed and episode ID. Draw that episode’s entire horizon-by-channel matrix from pinned PCG64, then scale and shift. Do not seed or consume the legacy global RNG. Work/output O(EHD); replay is independent of batch order.
