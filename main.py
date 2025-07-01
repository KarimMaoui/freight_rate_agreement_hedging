import numpy as np
import matplotlib.pyplot as plt
from freight_simulation import simulate_freight_paths
from fra_pricing import simulate_fra_pnl, calculate_unhedged_cost, calculate_total_hedged_cost

# 1. Simulation des trajectoires de taux de fret
paths = simulate_freight_paths(S0=15000, mu=0.0, sigma=0.25, T=0.25, dt=1/252, n_paths=1000)

# 2. Paramètres du contrat FRA
strike_rate = 14500       # taux fixe convenu dans le contrat
notional = 100            # par ex. 100 jours de location
duration_years = 1/12     # équivalent à 1 mois
eval_day = 21             # date d’observation des taux (~1 mois)

# 3. Calcul du PnL sur les trajectoires simulées
pnl = simulate_fra_pnl(paths, strike_rate, notional, duration_years, eval_day)

# 4. Visualisation du PnL
plt.hist(pnl, bins=40, edgecolor='black', color='skyblue')
plt.title("FRA Hedge P&L Distribution")
plt.xlabel("PnL (USD)")
plt.ylabel("Frequency")
plt.grid(True)
plt.show()

# 5. Analyse complémentaire : hedged vs unhedged cost
realized_rates = paths[:, eval_day]
unhedged = calculate_unhedged_cost(realized_rates, notional, duration_years)
hedged = calculate_total_hedged_cost(realized_rates, strike_rate, notional, duration_years)

plt.figure(figsize=(10,5))
plt.hist(unhedged, bins=40, alpha=0.6, label='Unhedged Cost', color='red')
plt.hist(hedged, bins=40, alpha=0.6, label='Hedged Cost (FRA)', color='green')
plt.axvline(x=np.mean(unhedged), color='red', linestyle='--')
plt.axvline(x=np.mean(hedged), color='green', linestyle='--')
plt.title('Cashflow Comparison: Hedged vs Unhedged')
plt.xlabel('Total Cost (USD)')
plt.ylabel('Frequency')
plt.legend()
plt.grid(True)
plt.show()

