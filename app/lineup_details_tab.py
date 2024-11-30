import streamlit as st
import pandas as pd

def show_lineup_details_tab(all_lineups):
    """
    Displays the detailed or condensed view of the lineups.

    Args:
        all_lineups (list): List of DataFrames representing the lineups.
    """
    st.markdown("### Lineup Details")
    view_type = st.radio(
        "Select Lineup View:",
        options=["Condensed", "Detailed"],
        index=0,
        horizontal=True,
    )

    if view_type == "Condensed":
        show_condensed_lineups(all_lineups)
    else:
        show_detailed_lineups(all_lineups)

def show_condensed_lineups(all_lineups):
    """
    Displays lineups in a condensed format.

    Args:
        all_lineups (list): List of DataFrames representing the lineups.
    """
    st.markdown("#### Condensed Lineup View")
    formatted_lineups = []

    for i, lineup in enumerate(all_lineups):
        lineup_filtered = lineup.dropna(subset=["Name"])
        lineup_filtered = lineup_filtered[~lineup_filtered["Name"].str.contains("TOTALS", case=False, na=False)]

        players = ", ".join(lineup_filtered["Name"].astype(str))
        formatted_lineups.append({
            "Rank": i + 1,
            "Players": players,
            "Salary": lineup_filtered["Salary"].sum(),
            "Proj. Score": lineup_filtered["ProjPts"].sum(),
            "Proj. Ownership": lineup_filtered["ProjOwn"].sum(),
        })

    condensed_df = pd.DataFrame(formatted_lineups)
    st.dataframe(condensed_df, use_container_width=True, height=400)

def show_detailed_lineups(all_lineups):
    """
    Displays lineups in a detailed format.

    Args:
        all_lineups (list): List of DataFrames representing the lineups.
    """
    st.markdown("#### Detailed Lineup View")
    for idx, lineup in enumerate(all_lineups):
        st.markdown(f"**Lineup {idx + 1}:**")
        st.dataframe(lineup, use_container_width=True, height=300)
