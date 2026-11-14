# Hints

## Hint 1

Check that the two key sets agree, then look up the student tensor using each teacher name. Zipping dictionary values is unsafe.

## Hint 2

Perform the update without creating an autograd graph. Returning student directly at momentum zero would violate both detachment and independent-storage requirements.

## Hint 3

Treat buffers as a separate contract rather than guessing which integer entries to copy. Empty dictionaries and scalar parameter tensors still have well-defined behavior.
