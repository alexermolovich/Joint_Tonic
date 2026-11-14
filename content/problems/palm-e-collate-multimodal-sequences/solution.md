## Approach

Find lengths, allocate bounded padded arrays, and copy each source prefix with its modality IDs. Presence derives from lengths, never embedding values.

O(B*Lmax*E) allocation/time and storage.
