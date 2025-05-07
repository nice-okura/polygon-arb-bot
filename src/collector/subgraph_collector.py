import aiohttp
import asyncio
import logging
import yaml
from pathlib import Path
from typing import Dict

logger = logging.getLogger(__name__)
_cfg_path = Path(__file__).resolve().parents[2] / "config" / "settings.yaml"
with open(_cfg_path, "r", encoding="utf-8") as f:
    _CFG = yaml.safe_load(f)

POOL_QUERY = """
query ($token0: String!, $token1: String!) {
  pools(
    where: {
      token0: $token0,
      token1: $token1
    },
    first: 1
  ) {
    id
    token0Price
    token1Price
    sqrtPrice
    liquidity
    feeTier
  }
}
"""

class SubgraphCollector:
    def __init__(self):
        self.urls = {
            "uniswap": _CFG["uniswap_v3_subgraph"],
            "quickswap": _CFG["quickswap_v3_subgraph"],
        }
        pair = _CFG["pairs"][0]
        self.token0 = pair["base"].lower()
        self.token1 = pair["quote"].lower()

    async def fetch_price(self, dex: str) -> Dict:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                self.urls[dex],
                json={"query": POOL_QUERY, "variables": {"token0": self.token0, "token1": self.token1}},
                timeout=20,
            ) as resp:
                data = await resp.json()

                if "data" not in data or not data["data"].get("pools"):
                    logger.error("❌ No pool data from %s: %s", dex, data)
                    raise ValueError(f"Failed to fetch pool data from {dex}")

                pool = data["data"]["pools"][0]
                return {
                    "dex": dex,
                    "price": float(pool["token1Price"]),  # USDC per WETH
                    "liquidity": float(pool["liquidity"]),
                }

    async def snapshot(self):
        uni, quick = await asyncio.gather(
            self.fetch_price("uniswap"),
            self.fetch_price("quickswap"),
        )
        return {"uniswap": uni, "quickswap": quick}
