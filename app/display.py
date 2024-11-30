import streamlit as st
import pandas as pd

def show_initial_table(player_pool):
    """
    Displays the initial projections table.

    Args:
        player_pool (pd.DataFrame): The player pool DataFrame.

    Returns:
        None
    """
    st.markdown("### Initial Player Projections")
    st.dataframe(player_pool, use_container_width=True)


def display_lineups_and_exposures(all_lineups, player_exposures):
    """
    Display the generated lineups and player exposures.

    Args:
        all_lineups (list): List of DataFrames representing generated lineups.
        player_exposures (pd.DataFrame): DataFrame of player exposures.
    """
    col1, col2 = st.columns([1, 2])

    with col1:
        st.markdown("### Player Exposures")
        st.dataframe(player_exposures, use_container_width=True)

    with col2:
        st.markdown("### Generated Lineups")
        formatted_lineups_df = format_lineups_as_rows(all_lineups)
        st.dataframe(formatted_lineups_df, use_container_width=True)


def format_lineups_as_rows(all_lineups):
    """
    Format the lineups for a condensed single-row display in a DataFrame.

    Args:
        all_lineups (list): List of DataFrames representing generated lineups.

    Returns:
        pd.DataFrame: DataFrame with lineups formatted as rows.
    """
    formatted_lineups = []

    for i, lineup in enumerate(all_lineups):
        # Exclude rows where "Name" is NaN or "TOTALS"
        lineup_filtered = lineup.dropna(subset=["Name"])
        lineup_filtered = lineup_filtered[~lineup_filtered["Name"].str.contains("TOTALS", case=False, na=False)]

        # Join player names into a single string
        players = ", ".join(lineup_filtered["Name"].astype(str))

        # Append lineup summary
        formatted_lineups.append({
            "Rank": i + 1,
            "Players": players,
            "Salary": lineup_filtered["Salary"].sum(),
            "Proj. Score": lineup_filtered["ProjPts"].sum(),
            "Proj. Ownership": lineup_filtered["ProjOwn"].sum(),
        })

    return pd.DataFrame(formatted_lineups)
