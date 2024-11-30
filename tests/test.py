import pandas as pd
from pulp import LpMaximize, LpProblem, LpVariable, lpSum
import numpy as np

# Load the player pool
player_pool = pd.read_csv('nfl/tests/test_player_pool.csv')

# DraftKings constraints
SALARY_CAP = 50000
MIN_SALARY = 49500  # Minimum salary usage to ensure a competitive lineup
ROSTER_REQUIREMENTS = {
    "QB": 1,
    "RB": 2,
    "WR": 3,  # At least 3 WRs
    "TE": 1,
    "FLEX": 1,
    "DST": 1,
}

# Add FLEX eligibility
player_pool["IsFLEX"] = player_pool["Position"].str.contains("FLEX")
player_pool["IsWR"] = player_pool["Position"].str.contains("WR")

# Generate multiple lineups with variance
lineups = []
for lineup_num in range(10):
    # Apply small random variance to projections
    player_pool["AdjProjPts"] = player_pool["ProjPts"] + np.random.uniform(-1, 1, len(player_pool))

    # Define the optimization problem
    problem = LpProblem(f"DraftKings_NFL_Lineup_Optimization_{lineup_num}", LpMaximize)

    # Define variables
    player_vars = {i: LpVariable(f"player_{i}", cat="Binary") for i in player_pool.index}

    # Objective: Maximize total adjusted projected points
    problem += lpSum(player_pool.loc[i, "AdjProjPts"] * player_vars[i] for i in player_pool.index)

    # Constraint: Total salary must be within the cap
    problem += lpSum(player_pool.loc[i, "Salary"] * player_vars[i] for i in player_pool.index) <= SALARY_CAP

    # Constraint: Ensure minimum salary usage
    problem += lpSum(player_pool.loc[i, "Salary"] * player_vars[i] for i in player_pool.index) >= MIN_SALARY

    # Constraint: Enforce roster requirements
    for pos, req in ROSTER_REQUIREMENTS.items():
        if pos == "FLEX":
            # FLEX can be RB/WR/TE
            problem += lpSum(
                player_vars[i]
                for i in player_pool.index
                if player_pool.loc[i, "IsFLEX"]
            ) >= req
        elif pos == "WR":
            # WR minimum of 3 players, including WRs in the FLEX spot
            problem += lpSum(
                player_vars[i]
                for i in player_pool.index
                if player_pool.loc[i, "IsWR"]
            ) >= req
        else:
            problem += lpSum(
                player_vars[i]
                for i in player_pool.index
                if pos in player_pool.loc[i, "Position"]
            ) == req

    # Constraint: Maximum number of players in the lineup
    problem += lpSum(player_vars[i] for i in player_pool.index) == sum(ROSTER_REQUIREMENTS.values())

    # Solve the problem
    problem.solve()

    # Output the optimal lineup
    optimal_lineup = player_pool.loc[[i for i in player_pool.index if player_vars[i].value() == 1]]
    total_salary = optimal_lineup["Salary"].sum()
    total_proj_pts = optimal_lineup["AdjProjPts"].sum()

    # Save lineup to the list
    lineups.append((lineup_num + 1, total_salary, total_proj_pts, optimal_lineup))

# Prepare lineups for single-line CSV format
single_line_lineups = []
for lineup_num, total_salary, total_proj_pts, lineup in lineups:
    lineup_dict = {
        "Lineup": lineup_num,
        "Total Salary": total_salary,
        "Total Projection": total_proj_pts,
    }
    for idx, row in lineup.iterrows():
        lineup_dict[f"Player {idx + 1} Name"] = row["Name"]
        lineup_dict[f"Player {idx + 1} Position"] = row["Position"]
        lineup_dict[f"Player {idx + 1} Salary"] = row["Salary"]
        lineup_dict[f"Player {idx + 1} Points"] = row["AdjProjPts"]
    single_line_lineups.append(lineup_dict)

# Convert to DataFrame and save to CSV
single_line_df = pd.DataFrame(single_line_lineups)
single_line_file_path = "lineups_single_line.csv"
single_line_df.to_csv(single_line_file_path, index=False)

print(f"All lineups saved to {single_line_file_path} in single-line format.")
