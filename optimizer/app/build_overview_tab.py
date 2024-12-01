import streamlit as st


def render_build_overview_tab():
    """
    Renders the Build Overview tab with player exposures and lineup insights.
    """
    st.markdown("### Build Overview")

    # Display player exposures
    if "player_exposures" in st.session_state and st.session_state["player_exposures"] is not None:
        st.markdown("#### Player Exposures")
        st.dataframe(st.session_state["player_exposures"], use_container_width=True)
    else:
        st.warning("No player exposures available. Please optimize lineups first.")
