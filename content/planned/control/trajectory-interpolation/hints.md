# Progressive hints

## Hint 1

Find the time interval before mixing joint values. The interval is determined by timestamps, not by rounding the query time.

## Hint 2

Use the same interpolation fraction for every channel, but compute a vector slope from the two bracketing joint rows.

## Hint 3

Handle endpoint holds before interval division. At an interior knot, choose the right interval so the reported velocity has one unambiguous meaning.

