# Reference approach

Validate the zero-skew calibration form. Build integer column/row grids and flatten in row-major order. For finite positive depth, multiply the normalized pinhole ray by z. Keep all missing rows as NaN and return a separate validity mask. Runtime and additional storage are O(HW). The forward projection of each valid point recovers its original integer pixel; that round trip checks axis and ordering mistakes.

The reference below validates the documented contract and preserves inputs. It uses original synthetic fixtures, not hardware control or a published benchmark reproduction.
