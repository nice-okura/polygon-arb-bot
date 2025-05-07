class RiskManager:
    def __init__(self, max_drawdown_pct: float):
        self.max_dd = max_drawdown_pct / 100
        self.equity_start = 1.0
        self.equity_cur = 1.0

    def update_pnl(self, pnl_pct: float):
        self.equity_cur *= 1 + pnl_pct
        dd = 1 - (self.equity_cur / self.equity_start)
        return dd

    def is_stop(self):
        dd = 1 - (self.equity_cur / self.equity_start)
        return dd >= self.max_dd
