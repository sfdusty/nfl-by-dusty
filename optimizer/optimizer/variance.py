import numpy as np
import pandas as pd

def generate_projection_sets(player_pool, num_sets=10, variance_range=0.1):
    """
    Generates multiple sets of adjusted projections with variance applied.

    Args:
        player_pool (pd.DataFrame): The player pool with projections.
        num_sets (int): Number of projection sets to generate.
        variance_range (float): Maximum percentage adjustment for variance (e.g., 0.1 for ±10%).

    Returns:
        list of pd.DataFrame: List of player pools with adjusted projections.
    """
    projection_sets = []

    for _ in range(num_sets):
        adjusted_player_pool = player_pool.copy()
        # Apply random variance to projections
        adjusted_player_pool["ProjPts"] = adjusted_player_pool["ProjPts"] * (
            1 + np.random.uniform(-variance_range, variance_range, len(player_pool))
        )
        projection_sets.append(adjusted_player_pool)

    return projection_sets

