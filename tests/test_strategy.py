from strategy.arbitrage_strategy import ArbitrageStrategy

def test_plan_generation():
    strat = ArbitrageStrategy()
    snap = {
        "uniswap": {"price": 3000.0, "liquidity": 1},
        "quickswap": {"price": 2970.0, "liquidity": 1},
    }
    plan = strat.generate_plan(snap)
    assert plan is not None
