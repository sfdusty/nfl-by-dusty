from datetime import datetime
import numpy as np
import pandas as pd
from datetime import datetime
from optimizer.constants import ROSTER_REQUIREMENTS

import streamlit as st



def preprocess_player_pool(player_pool):
    print("Debug: Starting preprocess_player_pool function")
    validate_player_pool(player_pool)

    # Extract and parse game start time from the "Game Info" column
    player_pool["GameTime"] = player_pool["Game Info"].apply(extract_game_time)

    # Add position eligibility flags
    player_pool["IsFLEX"] = player_pool["Position"].str.contains("RB|WR|TE")
    player_pool["IsWR"] = player_pool["Position"].str.contains("WR")
    player_pool["IsRB"] = player_pool["Position"].str.contains("RB")
    player_pool["IsTE"] = player_pool["Position"].str.contains("TE")
    player_pool["IsQB"] = player_pool["Position"].str.contains("QB")
    player_pool["IsDST"] = player_pool["Position"].str.contains("DST")

    print("Debug: Preprocessing completed")
    return player_pool




def extract_game_time(game_info):
    """Extract and parse the game start time from the Game Info column."""
    try:
        return datetime.strptime(game_info.split(" ")[1] + " " + game_info.split(" ")[2], "%m/%d/%Y %I:%M%p")
    except:
        return None

def validate_player_pool(player_pool):
    """Ensure player pool contains required columns."""
    required_columns = { "Position", "Salary", "ProjPts", "Game Info"}
    missing = required_columns - set(player_pool.columns)
    if missing:
        raise ValueError(f"Missing required columns in player pool: {missing}")
        
    
    
    


def calculate_player_exposures(all_lineups):
    """
    Calculates player exposures and stores them in session state.

    Args:
        all_lineups (list): List of DataFrames representing generated lineups.

    Returns:
        pd.DataFrame: Player exposures DataFrame.
    """
    # Flatten all lineups into a single DataFrame
    combined_lineups = pd.concat(all_lineups, ignore_index=True)

    # Count appearances of each player
    exposures = combined_lineups["Name"].value_counts().reset_index()
    exposures.columns = ["Player", "Appearances"]

    # Store exposures in session state
    st.session_state["player_exposures"] = exposures

    return exposures





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


