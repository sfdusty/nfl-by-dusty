import os
import sys
import streamlit as st
import pandas as pd

# Dynamically add root directory to path
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

# Import from optimizer module
from optimizer.main_opto import run_optimizer_workflow


def main():
    st.set_page_config(page_title="NFL Lineup Optimizer", layout="wide")

    # Sidebar Logic
    st.sidebar.header("Settings")
    num_lineups = st.sidebar.slider("Number of Lineups", min_value=1, max_value=50, value=10, step=1)
    min_salary = st.sidebar.slider("Minimum Salary", min_value=0, max_value=50000, value=49500, step=500)
    max_salary = st.sidebar.slider("Maximum Salary", min_value=0, max_value=50000, value=50000, step=500)
    min_uniques = st.sidebar.slider("Minimum Unique Players", min_value=0, max_value=9, value=2, step=1)
    variance_range = st.sidebar.slider(
        "Variance Range (%)", min_value=0, max_value=50, value=10, step=1,
        help="Adjust the maximum percentage variance applied to projections (e.g., 10% = ±10%)."
    )
    st.sidebar.write("---")

    # Run Optimizer button
    if "optimize_button_clicked" not in st.session_state:
        st.session_state["optimize_button_clicked"] = False

    if st.sidebar.button("Run Optimizer"):
        st.session_state["optimize_button_clicked"] = True

    # Define projections file path
    projections_path = os.path.join("data", "merged_projections.csv")

    # Initialize session state variables
    if "all_lineups" not in st.session_state:
        st.session_state["all_lineups"] = None
    if "player_exposures" not in st.session_state:
        st.session_state["player_exposures"] = None

    # Debug: Show session state at the start
    st.write("Debug: Initial session state")
    st.write(st.session_state)

    # Main Page Content
    st.title("NFL Lineup Optimizer")

    # Load projections table
    try:
        st.write("Debug: Loading projections table")
        player_pool = pd.read_csv(projections_path)
        st.write("Debug: Projections file loaded successfully")
        st.dataframe(player_pool, use_container_width=True)

        # Run optimizer workflow if button clicked
        if st.session_state["optimize_button_clicked"]:
            st.write("Debug: Optimize button clicked")
            try:
                all_lineups, player_exposures = run_optimizer_workflow(
                    player_pool, num_lineups, min_salary, max_salary, min_uniques, variance_range / 100
                )

                # Update session state with results
                st.session_state["all_lineups"] = all_lineups
                st.session_state["player_exposures"] = player_exposures

                st.success("Optimization completed successfully!")
                st.write("Debug: Results updated in session state")
                st.dataframe(player_exposures, use_container_width=True)

                # Reset optimize button state
                st.session_state["optimize_button_clicked"] = False

            except Exception as e:
                st.error(f"An error occurred during optimization: {e}")
                st.write(f"Debug: Exception - {e}")

    except FileNotFoundError:
        st.error("Projections file not found. Please ensure the file exists in the 'data/' directory.")
    except Exception as e:
        st.error(f"An error occurred: {e}")
        st.write(f"Debug: Exception - {e}")


if __name__ == "__main__":
    main()
