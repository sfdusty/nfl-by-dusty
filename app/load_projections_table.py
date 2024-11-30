import os
import pandas as pd
import streamlit as st


def show_initial_table():
    """
    Load and display the initial player projections table.
    """
    # Define the file path to the projections CSV
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # Locate the `nfl/` root directory
    projections_path = os.path.join(base_dir, "data", "merged_projections.csv")  # Adjust path to `merged_projections.csv`

    # Load the player pool
    try:
        player_pool = pd.read_csv(projections_path)
    except FileNotFoundError:
        st.error("Error: Merged projections file not found.")
        return None

    # Display the table
    st.markdown("### Initial Player Projections")
    st.dataframe(player_pool, use_container_width=True)

    return player_pool
