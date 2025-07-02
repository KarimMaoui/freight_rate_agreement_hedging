import numpy as np
from freight_simulation import simulate_freight_paths
from fra_pricing import simulate_fra_pnl

def run_fra_scenario(S0, sigma, T, strike_rate=14500, notional=100, duration=1/12, eval_day=None):
    """
    Simule un scénario de couverture FRA et retourne la moyenne et la vol du PnL
    """
    paths = simulate_freight_paths(S0=S0, sigma=sigma, T=T, dt=1/252, n_paths=1000)
    n_steps = paths.shape[1]

    if eval_day is None:
        eval_day = min(int(duration * 252) - 1, n_steps - 1)  # Empêche overflow

    # Ajout défensif : si eval_day < 0 (ex: duration très courte)
    if eval_day < 0:
        raise ValueError(f"Evaluation day too small ({eval_day}). Increase duration or adjust T.")

    pnl = simulate_fra_pnl(paths, strike_rate, notional, duration, eval_day)
    return np.mean(pnl), np.std(pnl)
