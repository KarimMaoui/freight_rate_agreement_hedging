import numpy as np

def fra_payoff(realized_rate, strike_rate, notional, duration_years):
    """
    Calcule le cashflow d’un FRA à la date de fixation.
    """
    return (realized_rate - strike_rate) * notional * duration_years

def simulate_fra_pnl(paths, strike_rate, notional, duration_years, eval_day):
    """
    Calcule les P&L simulés d’un FRA selon les trajectoires de taux.

    Args:
        paths: matrice des taux simulés
        strike_rate: taux fixe du FRA (ex: 14000 USD)
        notional: nombre de jours multipliés par le nombre de contrats
        duration_years: durée du contrat (par ex : 1/12 pour 1 mois)
        eval_day: index du jour auquel le taux est observé

    Returns:
        np.array des gains ou pertes
    """
    realized_rates = paths[:, eval_day]
    return fra_payoff(realized_rates, strike_rate, notional, duration_years)

def calculate_unhedged_cost(realized_rates, notional, duration_years):
    """
    Coût si on reste exposé au taux variable
    """
    return realized_rates * notional * duration_years

def calculate_total_hedged_cost(realized_rates, strike_rate, notional, duration_years):
    """
    Coût total en cas de couverture (variable + payoff FRA)
    """
    unhedged = calculate_unhedged_cost(realized_rates, notional, duration_years)
    hedge_pnl = fra_payoff(realized_rates, strike_rate, notional, duration_years)
    return unhedged - hedge_pnl

