# Hints

1. Validate the requested index range before slicing.
2. Check all selected validity entries; any false entry rejects the window.
3. Copy the slice so later replanning cannot mutate an already returned buffer.
