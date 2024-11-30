import streamlit as st
import pandas as pd

def show_build_overview_tab(all_lineups, player_exposures):
    """
    Displays an overview of the build including exposures and lineup stats.

    Args:
        all_lineups (list): List of DataFrames representing the lineups.
        player_exposures (pd.DataFrame): DataFrame showing player exposures.
    """
    st.markdown("### Build Overview")

    # Create a scrollable container for player exposures
    st.markdown("#### Player Exposures")
    st.dataframe(player_exposures, use_container_width=True, height=400)

    # Show summary stats for the build
    st.markdown("#### Build Summary")
    summary = summarize_lineups(all_lineups)
    st.table(summary)

def summarize_lineups(all_lineups):
    """
    Summarizes the lineups by calculating aggregate stats.

    Args:
        all_lineups (list): List of DataFrames representing the lineups.

    Returns:
        pd.DataFrame: Summary of the build.
    """
    total_salary = [lineup["Salary"].sum() for lineup in all_lineups]
    total_proj_score = [lineup["ProjPts"].sum() for lineup in all_lineups]
    total_proj_ownership = [lineup["ProjOwn"].sum() for lineup in all_lineups]

    summary = {
        "Lineup": [f"Lineup {i+1}" for i in range(len(all_lineups))],
        "Total Salary": total_salary,
        "Total Projected Score": total_proj_score,
        "Total Projected Ownership": total_proj_ownership,
    }

    return pd.DataFrame(summary)
