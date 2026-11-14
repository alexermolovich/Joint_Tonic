# Solution explanation

Filter each stage with a half-open window. Subtract integer timestamps before computing population gap statistics; count all retained events, including ties. The rate denominator is the entire window, not the span between events. Work O(N + S log S), retained storage O(N).
