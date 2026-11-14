# Hints

1. Verify the supplied model bytes before packaging identity.
2. Canonicalize only the three pre-hash manifest fields.
3. Deep-copy metadata so later caller edits cannot alter the returned manifest.
