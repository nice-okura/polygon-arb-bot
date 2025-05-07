def bps(diff, ref):
    """Return basis-points (1/100 %) representation."""
    return (diff / ref) * 10_000 if ref else 0
