import os
import streamlit as st
import pandas as pd
from optimizer.builder import optimize_lineup
from optimizer.opto_utils import preprocess_player_pool, display_player_exposures
from display import show_initial_table, display_lineups_and_exposures
from optimizer.opto_utils import ROSTER_REQUIREMENTS  # Import roster requirements


def main():
    st.set_page_config(page_title="NFL Lineup Optimizer", layout="wide")

    # Page title
    st.title("NFL Lineup Optimizer")

    # Sidebar for settings
    with st.sidebar:
        st.header("Settings")
        num_lineups = st.slider("Number of Lineups", min_value=1, max_value=50, value=10, step=1)
        min_salary = st.slider("Minimum Salary", min_value=0, max_value=50000, value=49500, step=500)
        max_salary = st.slider("Maximum Salary", min_value=0, max_value=50000, value=50000, step=500)
        min_uniques = st.slider("Minimum Unique Players", min_value=0, max_value=9, value=2, step=1)

        st.write("---")

        # Notification placeholder
        notification_placeholder = st.empty()

        optimize_button = st.button("Run Optimizer")

    # Define projections file path relative to the root directory
    base_dir = os.path.dirname(os.path.abspath(__file__))  # Get the current directory of the script
    projections_path = os.path.join(base_dir, "../data/merged_projections.csv")  # Adjust the path to `data/`

    if not optimize_button:
        # Display the initial player pool table
        player_pool = pd.read_csv(projections_path)
        show_initial_table(player_pool)
    else:
        # Run optimization process with accurate notifications
        notification_placeholder.text("Loading player pool...")

        # Load and preprocess player pool
        player_pool = pd.read_csv(projections_path)
        notification_placeholder.text("Preprocessing player pool...")
        preprocessed_player_pool = preprocess_player_pool(player_pool)

        # Optimize lineups
        notification_placeholder.text("Optimizing lineups...")
        all_lineups = optimize_lineup(
            player_pool=preprocessed_player_pool,
            roster_requirements=ROSTER_REQUIREMENTS,  # Pass roster requirements here
            num_lineups=num_lineups,
            min_salary=min_salary,
            max_salary=max_salary,
            min_uniques=min_uniques,
        )

        # Generate player exposures
        notification_placeholder.text("Calculating player exposures...")
        player_exposures = display_player_exposures(all_lineups)

        # Display results
        notification_placeholder.text("Displaying results...")
        display_lineups_and_exposures(all_lineups, player_exposures)

        # Final notification
        notification_placeholder.success("Optimization Complete!")


if __name__ == "__main__":
    main()
