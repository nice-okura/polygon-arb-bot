import logging
from utils.web3_provider import get_web3

logger = logging.getLogger(__name__)
w3 = get_web3()

class TxExecutor:
    """
    Dummy executor for MVP:
    ─ Build & sign TX (omitted)
    ─ Submit via Flashbots RPC (omitted)
    """

    def execute(self, plan):
        buy_dex, sell_dex, size_eth = plan
        logger.info(
            "EXECUTE → Buy %f ETH on %s, sell on %s (dummy)", size_eth, buy_dex, sell_dex
        )
        # TODO: Replace with real router calls & Flashbots bundle
        return True
