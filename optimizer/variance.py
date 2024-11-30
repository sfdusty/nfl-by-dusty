import pandas as pd
import numpy as np

def apply_variance(player_pool, variance_by_position, team_variance):
    """
    Applies variance to player projections.

    Args:
        player_pool (pd.DataFrame): Player pool with projections.
        variance_by_position (dict): Variance levels by position (e.g., {"QB": 0.05, "RB": 0.1}).
        team_variance (float): Variance applied to team projections.

    Returns:
        pd.DataFrame: Player pool with adjusted projections.
    """
    # Apply variance by position
    for position, variance_level in variance_by_position.items():
        position_mask = player_pool["Position_y"] == position
        player_pool.loc[position_mask, "ProjPts"] += np.random.normal(
            0, variance_level * player_pool.loc[position_mask, "ProjPts"]
        )

    # Apply team-level variance
    for team in player_pool["Team"].unique():
        team_mask = player_pool["Team"] == team
        team_projection_adjustment = np.random.normal(0, team_variance)
        player_pool.loc[team_mask, "ProjPts"] += team_projection_adjustment

    return player_pool


