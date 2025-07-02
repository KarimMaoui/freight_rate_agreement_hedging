import numpy as np
import matplotlib.pyplot as plt
from freight_simulation import simulate_freight_paths
from fra_pricing import simulate_fra_pnl, calculate_unhedged_cost, calculate_total_hedged_cost

from sensitivity_analysis import run_fra_scenario
import pandas as pd
import seaborn as sns

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
print(hedged,unhedged)
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



initial_rates = [12000, 14000, 16000, 18000]
volatilities = [0.10, 0.20, 0.30, 0.40]
maturities = [0.08, 0.25, 0.5]  # (1M, 3M, 6M)

results = []

for S0 in initial_rates:
    for sigma in volatilities:
        for T_fra in maturities:
            pnl_mean, pnl_std = run_fra_scenario(S0, sigma, T_fra)
            results.append({
                'Initial Rate': S0,
                'Volatility': sigma,
                'Maturity': T_fra,
                'Avg PnL': pnl_mean,
                'PnL StdDev': pnl_std
            })

df = pd.DataFrame(results)

# Heatmap sur l’Avg PnL (fixe Maturity = 0.25)
subset = df[df['Maturity'] == 0.25].pivot(index='Initial Rate', columns='Volatility', values='Avg PnL')
plt.figure(figsize=(8,6))
sns.heatmap(subset, annot=True, fmt=".0f", cmap='coolwarm')
plt.title('Average FRA PnL — Maturity = 3M')
plt.xlabel('Volatility')
plt.ylabel('Initial Rate')
plt.show()


# Simule différentes valeurs spot réalisées
spot_range = np.linspace(13000, 17000, 100)
notional = 1_200_000
delta = 30 / 360
fra_rate = 15000  # Strike du FRA

# Coût sans couverture = spot * notional * delta
unhedged_costs = spot_range * notional * delta

# Coût avec FRA = hedgé à taux fixe
hedged_costs = fra_rate * notional * delta * np.ones_like(spot_range)

# Plot
plt.figure(figsize=(10, 6))
plt.plot(spot_range, unhedged_costs, label='Unhedged Cost (Exposed)', color='red')
plt.plot(spot_range, hedged_costs, label='Hedged Cost (FRA @ 15,000)', color='green', linestyle='--')
plt.title('📉 Hedging Efficiency — Cost vs Spot Freight Rate')
plt.xlabel('Realized Spot Rate ($/day)')
plt.ylabel('Total Cost ($)')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
