from typing import Optional, Tuple
from utils.math_utils import bps
import yaml
from pathlib import Path

_cfg_path = Path(__file__).resolve().parents[2] / "config" / "settings.yaml"
with open(_cfg_path, "r", encoding="utf-8") as f:
    _CFG = yaml.safe_load(f)

_MIN_SPREAD_BPS = _CFG["min_spread_bps"]

class ArbitrageStrategy:
    """
    Compare price between Uniswap v3 and QuickSwap v3.
    If |spread| > threshold → return trade plan (buy_dex, sell_dex, size_eth).
    """

    def generate_plan(self, snapshot: dict) -> Optional[Tuple[str, str, float]]:
        uni_p = snapshot["uniswap"]["price"]
        quick_p = snapshot["quickswap"]["price"]

        spread = bps(uni_p - quick_p, quick_p)  # >0 ⇒ Uni expensive
        if spread > _MIN_SPREAD_BPS:
            return ("quickswap", "uniswap", 0.02)  # buy cheap @Quick, sell @Uni
        if spread < -_MIN_SPREAD_BPS:
            return ("uniswap", "quickswap", 0.02)  # reverse
        return None
