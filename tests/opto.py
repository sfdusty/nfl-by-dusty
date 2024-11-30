import os
import pandas as pd
from pulp import LpMaximize, LpProblem, LpVariable, lpSum
import datetime

# Set up test file paths
TEST_DIR = os.path.dirname(os.path.abspath(__file__))
TEST_PLAYER_POOL_FILE = os.path.join(TEST_DIR, "test_player_pool.csv")

def preprocess_player_pool(player_pool):
    def extract_game_time(game_info):
        try:
            return datetime.datetime.strptime(game_info.split(" ")[1] + " " + game_info.split(" ")[2], "%m/%d/%Y %I:%M%p")
        except:
            return None

    player_pool["GameTime"] = player_pool["Game Info"].apply(extract_game_time)
    player_pool["IsFLEX"] = player_pool["Roster Position"].str.contains("RB|WR|TE")
    player_pool["IsWR"] = player_pool["Roster Position"].str.contains("WR")
    player_pool["IsRB"] = player_pool["Roster Position"].str.contains("RB")
    player_pool["IsTE"] = player_pool["Roster Position"].str.contains("TE")
    player_pool["IsQB"] = player_pool["Roster Position"].str.contains("QB")
    player_pool["IsDST"] = player_pool["Roster Position"].str.contains("DST")
    return player_pool

from pulp import LpMaximize, LpProblem, LpVariable, lpSum

def optimize_lineup(player_pool, roster_requirements, min_salary=49500, max_salary=50000):
    """
    Optimizes the DraftKings NFL lineup based on constraints.

    Args:
        player_pool (pd.DataFrame): DataFrame containing the player pool with necessary columns.
        roster_requirements (dict): Dictionary specifying position requirements (e.g., {"QB": 1, "RB": 2, ...}).
        min_salary (int): Minimum salary usage for the lineup.
        max_salary (int): Maximum salary cap for the lineup.

    Returns:
        pd.DataFrame: Optimized lineup as a DataFrame.
    """
    # Define the optimization problem
    problem = LpProblem("DraftKings_NFL_Lineup_Optimization", LpMaximize)

    # Define variables
    player_vars = {i: LpVariable(f"player_{i}", cat="Binary") for i in player_pool.index}

    # Objective: Maximize total projected points
    problem += lpSum(player_pool.loc[i, "ProjPts"] * player_vars[i] for i in player_pool.index)

    # Salary constraints
    problem += lpSum(player_pool.loc[i, "Salary"] * player_vars[i] for i in player_pool.index) <= max_salary
    problem += lpSum(player_pool.loc[i, "Salary"] * player_vars[i] for i in player_pool.index) >= min_salary

    # Position constraints
    for pos, req in roster_requirements.items():
        if pos == "FLEX":
            # FLEX can be RB/WR/TE
            problem += lpSum(
                player_vars[i]
                for i in player_pool.index
                if player_pool.loc[i, "IsFLEX"]
            ) >= req
        else:
            problem += lpSum(
                player_vars[i]
                for i in player_pool.index
                if player_pool[f"Is{pos}"][i]
            ) == req

    # Total number of players in the lineup
    problem += lpSum(player_vars[i] for i in player_pool.index) == sum(roster_requirements.values())

    # Solve the problem
    problem.solve()

    # Extract the optimal lineup
    optimal_lineup = player_pool.loc[[i for i in player_pool.index if player_vars[i].value() == 1]].copy()

    return optimal_lineup
def format_lineup_for_display(optimal_lineup):
    """
    Formats the optimized lineup for display, sorting by desired order, and adds total metrics.

    Args:
        optimal_lineup (pd.DataFrame): The optimized lineup.

    Returns:
        pd.DataFrame: Lineup sorted and formatted for display, including totals.
    """
    # Determine the Flex player based on the latest game start time
    flex_candidates = optimal_lineup[optimal_lineup["IsFLEX"]]
    flex_player = flex_candidates.loc[flex_candidates["GameTime"].idxmax()]

    # Exclude the Flex player and Defense temporarily for sorting
    non_flex_dst_lineup = optimal_lineup.loc[
        ~optimal_lineup.index.isin([flex_player.name]) & ~optimal_lineup["IsDST"]
    ].copy()

    # Sort the remaining lineup by position
    position_order = ["QB", "RB", "WR", "TE"]
    non_flex_dst_lineup["Order"] = non_flex_dst_lineup["Roster Position"].apply(
        lambda pos: position_order.index(pos.split("/")[0]) if pos.split("/")[0] in position_order else 9
    )
    sorted_lineup = non_flex_dst_lineup.sort_values("Order")

    # Add Flex and Defense in the correct positions
    sorted_lineup = pd.concat(
        [
            sorted_lineup,
            flex_player.to_frame().T.assign(Order=7),  # Flex is second-to-last
            optimal_lineup[optimal_lineup["IsDST"]].assign(Order=8),  # Defense is last
        ],
        ignore_index=True,
    ).sort_values("Order")

    # Drop the temporary sorting column
    sorted_lineup = sorted_lineup.drop(columns="Order")

    # Calculate totals
    total_salary = sorted_lineup["Salary"].sum()
    total_proj_pts = sorted_lineup["ProjPts"].sum()
    total_proj_own = sorted_lineup["ProjOwn"].sum()

    # Create totals row
    totals_row = {
        "Name_x": "TOTALS",
        "TeamAbbrev": "",
        "Roster Position": "",
        "Salary": total_salary,
        "ProjPts": total_proj_pts,
        "ProjOwn": total_proj_own,
        "GameTime": "",
    }

    # Add totals row to the lineup
    sorted_lineup = pd.concat([sorted_lineup, pd.DataFrame([totals_row])], ignore_index=True)

    # Return the final lineup
    return sorted_lineup[["Name_x", "TeamAbbrev", "Roster Position", "Salary", "ProjPts", "ProjOwn", "GameTime"]]

def main():
    print("Loading test player pool...")
    player_pool = pd.read_csv(TEST_PLAYER_POOL_FILE)
    player_pool = preprocess_player_pool(player_pool)
    
    # Use correct argument names
    optimal_lineup = optimize_lineup(player_pool, roster_requirements={"QB": 1, "RB": 2, "WR": 3, "TE": 1, "FLEX": 1, "DST": 1}, min_salary=49500, max_salary=50000)
    
    if not optimal_lineup.empty:
        formatted_lineup = format_lineup_for_display(optimal_lineup)
        print(formatted_lineup)
