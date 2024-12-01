import pandas as pd
from pulp import LpMaximize, LpProblem, LpVariable, lpSum

def optimize_lineup(player_pool, roster_requirements, min_salary, max_salary, num_lineups, min_uniques):
    """
    Optimizes multiple lineups for DraftKings NFL contests with diversity constraints.

    Args:
        player_pool (pd.DataFrame): The player pool with projections and salary data.
        roster_requirements (dict): Position constraints for the lineup.
        min_salary (int): Minimum salary cap.
        max_salary (int): Maximum salary cap.
        num_lineups (int): Number of lineups to generate.
        min_unique_players (int): Minimum number of unique players across any two lineups.

    Returns:
        list of pd.DataFrame: List of optimized lineups.
    """
    # Add FLEX eligibility flags
    player_pool["IsFLEX"] = player_pool["Position"].str.contains("FLEX")
    player_pool["IsWR"] = player_pool["Position"].str.contains("WR")

    # Initialize list to store generated lineups
    lineups = []

    for lineup_num in range(num_lineups):
        # Define the optimization problem
        problem = LpProblem(f"DraftKings_NFL_Lineup_Optimization_{lineup_num}", LpMaximize)

        # Define variables
        player_vars = {i: LpVariable(f"player_{i}", cat="Binary") for i in player_pool.index}

        # Objective: Maximize total projected points
        problem += lpSum(player_pool.loc[i, "ProjPts"] * player_vars[i] for i in player_pool.index)

        # Add salary constraints
        salary_constraint = lpSum(player_pool.loc[i, "Salary"] * player_vars[i] for i in player_pool.index)
        problem += salary_constraint <= max_salary
        problem += salary_constraint >= min_salary

        # Add position constraints
        for pos, req in roster_requirements.items():
            if pos == "FLEX":
                problem += lpSum(
                    player_vars[i]
                    for i in player_pool.index
                    if player_pool.loc[i, "IsFLEX"]
                ) >= req
            elif pos == "WR":
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

        # Total number of players in the lineup
        problem += lpSum(player_vars[i] for i in player_pool.index) == sum(roster_requirements.values())

        # Enforce minimum unique players across lineups
        for prev_lineup in lineups:
            prev_player_indices = prev_lineup.index
            problem += lpSum(player_vars[i] for i in prev_player_indices) <= (len(prev_player_indices) - min_uniques)

        # Solve the problem
        problem.solve()

        # Extract the optimal lineup
        optimal_lineup = player_pool.loc[[i for i in player_pool.index if player_vars[i].value() == 1]].copy()

        # If no valid lineup is found, stop generating further lineups
        if optimal_lineup.empty:
            print(f"Unable to generate lineup {lineup_num + 1}. No feasible solution found.")
            break

        # Add lineup to the list
        lineups.append(optimal_lineup)

    return lineups