import streamlit as st


def render_lineup_details_tab():
    """
    Renders the Lineup Details tab with detailed lineup information.
    """
    st.markdown("### Lineup Details")

    if "all_lineups" in st.session_state and st.session_state["all_lineups"] is not None:
        for i, lineup in enumerate(st.session_state["all_lineups"]):
            st.markdown(f"#### Lineup {i + 1}")
            st.dataframe(lineup, use_container_width=True)
    else:
        st.warning("No lineups available. Please optimize lineups first.")
