# Hints

1. Keep train/evaluation inputs separate through every update.
2. Reuse the background-aware analytic renderer derivatives, then apply the sigmoid/softplus chain rule.
3. Clip one combined weight/bias gradient norm before simultaneous SGD.
