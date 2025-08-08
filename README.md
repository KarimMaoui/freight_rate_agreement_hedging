# Freight Rate Agreement Hedging Simulation 

This Python project simulates the performance of Freight Rate Agreements (FRAs) as hedging instruments against freight rate volatility. It models freight rate paths, applies FRA contracts, and evaluates their P&L impact under various market conditions.

##  Use Case

Shipping companies and commodity traders are exposed to fluctuations in freight rates. This project models how FRA contracts can hedge such exposure.

##  Project Structure

freight_rate_agreement_hedging/
├── main.py # Run a full simulation and visualize results
├── freight_simulation.py # GBM simulation of freight rates
├── fra_pricing.py # FRA payoff and P&L calculations
├── sensitivity_analysis.py # Scenario testing (rate, vol, maturity)
├── plots/ # Generated charts
├── requirements.txt
└── README.md


## 🚀 How to Run

```bash
# Clone repository
git clone https://github.com/yourusername/freight_rate_agreement_hedging.git
cd freight_rate_agreement_hedging

# (Optional) Create a virtual environment
python3 -m venv env
source env/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run main simulation
python main.py


numpy
matplotlib
seaborn
pandas

Nota Bene: Even though FRA payoffs are linear and volatility has little impact on average P&L, risk managers still care about dispersion of outcomes. This project visualizes both dimensions.
