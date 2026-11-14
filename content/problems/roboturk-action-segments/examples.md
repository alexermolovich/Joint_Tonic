# Worked examples

times[0,10,20,30], actions[[0],[0],[1],[0]], all observed flags=True, max_command[2], deadband=0.1, min_samples=2, min_duration_ns=10 yields corrupt[F, F, F, F], paused[T, T, F, F], segments[(0,2,10)].

With times[0,10,20], actions[[0],[NaN],[0]], all observed flags=True, max_command[2], deadband=0.1, min_samples=2, min_duration_ns=0, corrupt[F, T, F], paused[F, F, F], segments[]. The corrupt row separates two short runs.
