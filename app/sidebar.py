import streamlit as st


def render_sidebar():
    """
    Render the settings and controls in the sidebar.

    Returns:
        dict: A dictionary of user-selected settings.
    """
    with st.sidebar:
        st.header("Settings")
        num_lineups = st.slider("Number of Lineups", min_value=1, max_value=50, value=10, step=1)
        min_salary = st.slider("Minimum Salary", min_value=0, max_value=50000, value=49500, step=500)
        max_salary = st.slider("Maximum Salary", min_value=0, max_value=50000, value=50000, step=500)
        min_uniques = st.slider("Minimum Unique Players", min_value=0, max_value=9, value=2, step=1)

        st.write("---")

        # Add more sidebar settings if needed

    # Return the selected settings as a dictionary
    return {
        "num_lineups": num_lineups,
        "min_salary": min_salary,
        "max_salary": max_salary,
        "min_uniques": min_uniques,
    }
