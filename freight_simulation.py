
import numpy as np

def simulate_freight_paths(S0=15000, mu=0.0, sigma=0.2, T=1.0, dt=1/252, n_paths=1000):
    """
    Simule des trajectoires de taux de fret selon un processus de type GBM (Geometric Brownian Motion)

    Args:
        S0 (float): taux initial en USD (ex: 15000 USD / jour)
        mu (float): drift
        sigma (float): volatilité annuelle
        T (float): maturité (en années)
        dt (float): pas de temps (par défaut = journalier)
        n_paths (int): nombre de trajectoires à simuler

    Returns:
        np.ndarray: matrice [n_paths, n_steps] des trajectoires simulées
    """
    n_steps = int(T / dt)
    paths = np.zeros((n_paths, n_steps))
    paths[:, 0] = S0

    for t in range(1, n_steps):
        z = np.random.standard_normal(n_paths)
        paths[:, t] = paths[:, t-1] * np.exp((mu - 0.5 * sigma ** 2) * dt + sigma * np.sqrt(dt) * z)

    return paths
