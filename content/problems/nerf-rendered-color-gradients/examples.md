## Worked examples

**Example 1.** One ray/sample has density `0`, interval `1`, red sample color `[1, 0, 0]`, and black target/background. Output RGB is `[0, 0, 0]`, loss `0`, and both gradient arrays are zero.

**Example 2.** Replace density by `log(2)`. Output RGB is `[.5, 0, 0]`, loss `1/12`, density gradient `1/6`, and color gradient `[1/6, 0, 0]`, with original batch/sample dimensions retained.
