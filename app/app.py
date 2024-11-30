import os
import streamlit as st
import pandas as pd
from optimizer.builder import optimize_lineup
from optimizer.opto_utils import preprocess_player_pool, display_player_exposures, ROSTER_REQUIREMENTS
from sidebar import render_sidebar
from build_overview_tab import render_build_overview_tab
from lineup_details_tab import render_lineup_details_tab
from load_projections_table import show_initial_table


def main():
    # Set the page configuration
    st.set_page_config(page_title="NFL Lineup Optimizer", layout="wide")

    # Page title
    st.title("NFL Lineup Optimizer")

    # Sidebar
    build_settings = render_sidebar()

    # Projections file path
    base_dir = os.path.dirname(os.path.abspath(__file__))
    projections_path = os.path.join(base_dir, "../data/merged_projections.csv")

    # Session state initialization
    if "player_pool" not in st.session_state:
        # Load and preprocess player pool
        st.session_state.player_pool = pd.read_csv(projections_path)
        st.session_state.player_pool = preprocess_player_pool(st.session_state.player_pool)
        st.session_state.all_lineups = None
        st.session_state.player_exposures = None

    # Tabs
    tabs = st.tabs(["Projections", "Build Overview", "Lineup Details"])

    # Render the projections table tab
    with tabs[0]:
        show_initial_table(st.session_state.player_pool)

    # If the "Run Optimizer" button is clicked
    if build_settings["optimize_button"]:
        # Run optimization
        st.info("Running optimizer...")
        all_lineups = optimize_lineup(
            player_pool=st.session_state.player_pool,
            roster_requirements=ROSTER_REQUIREMENTS,
            num_lineups=build_settings["num_lineups"],
            min_salary=build_settings["min_salary"],
            max_salary=build_settings["max_salary"],
            min_uniques=build_settings["min_uniques"],
        )

        # Store the results in session state
        st.session_state.all_lineups = all_lineups
        st.session_state.player_exposures = display_player_exposures(all_lineups)

        # Display success notification
        st.success("Optimization Complete!")

    # Render the build overview tab
    with tabs[1]:
        if st.session_state.all_lineups:
            render_build_overview_tab(st.session_state.player_exposures, st.session_state.all_lineups)
        else:
            st.info("Run the optimizer to see build overview details.")

    # Render the lineup details tab
    with tabs[2]:
        if st.session_state.all_lineups:
            render_lineup_details_tab(st.session_state.all_lineups)
        else:
            st.info("Run the optimizer to view detailed lineups.")


if __name__ == "__main__":
    main()
