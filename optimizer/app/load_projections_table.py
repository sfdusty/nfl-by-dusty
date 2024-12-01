import streamlit as st
import pandas as pd

def show_initial_table(player_pool):
    """
    Display the initial player projections table.

    Args:
        player_pool (pd.DataFrame): The player pool DataFrame to display.
    """
    st.markdown("### Initial Player Projections")
    st.dataframe(player_pool, use_container_width=True)
