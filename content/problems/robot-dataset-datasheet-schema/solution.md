# Solution explanation

Compute missing and unexpected field sets. Validate each present required field independently, using stripped text only for nonemptiness/length and original strings for ID/version/hash syntax. A literal unknown is a supported reported value only for license and calibration hash. Validate a complete list before using a set for duplicate detection, so unhashable elements become field issues. Work bounded by text/list input size plus sorted issue output.
