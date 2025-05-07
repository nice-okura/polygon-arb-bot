import asyncio
import logging
from collector.subgraph_collector import SubgraphCollector
from strategy.arbitrage_strategy import ArbitrageStrategy
from executor.tx_executor import TxExecutor
from risk.risk_manager import RiskManager
import yaml
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

_cfg_path = Path(__file__).resolve().parents[1] / "config" / "settings.yaml"
with open(_cfg_path, "r", encoding="utf-8") as f:
    CFG = yaml.safe_load(f)

collector = SubgraphCollector()
strategy = ArbitrageStrategy()
executor = TxExecutor()
risk = RiskManager(CFG["max_drawdown_pct"])

async def loop():
    while True:
        snap = await collector.snapshot()
        plan = strategy.generate_plan(snap)
        if plan and not risk.is_stop():
            success = executor.execute(plan)
            # 仮に +0.05% の手取りを想定
            dd = risk.update_pnl(0.0005 if success else -0.0005)
            logging.info("Current drawdown: %.2f %%", dd * 100)
        await asyncio.sleep(15)

if __name__ == "__main__":
    asyncio.run(loop())
