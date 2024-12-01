import pandas as pd
from optimizer.builder import optimize_lineup
from optimizer.variance import generate_projection_sets
from optimizer.opto_utils import calculate_player_exposures
from optimizer.constants import ROSTER_REQUIREMENTS


def run_optimizer_workflow(player_pool, num_lineups, min_salary, max_salary, min_uniques, variance_range):
    """
    Orchestrates the entire optimization workflow.

    Args:
        player_pool (pd.DataFrame): Player pool with projections and salary.
        num_lineups (int): Number of lineups to generate.
        min_salary (int): Minimum salary cap.
        max_salary (int): Maximum salary cap.
        min_uniques (int): Minimum unique players across lineups.
        variance_range (float): Maximum percentage variance applied to projections.

    Returns:
        tuple: (all_lineups, player_exposures)
    """
    print("Debug: Starting optimizer workflow")
    print(f"Variance Range: {variance_range * 100}%")

    # Generate multiple projection sets with variance applied
    projection_sets = generate_projection_sets(player_pool, num_sets=num_lineups, variance_range=variance_range)
    print(f"Debug: {len(projection_sets)} projection sets generated")

    # Optimize lineups for each projection set
    all_lineups = []
    for i, projection_set in enumerate(projection_sets):
        print(f"Debug: Optimizing lineup for projection set {i + 1}")
        lineups = optimize_lineup(
            player_pool=projection_set,
            roster_requirements=ROSTER_REQUIREMENTS,
            min_salary=min_salary,
            max_salary=max_salary,
            num_lineups=1,  # Optimize one lineup per set
            min_uniques=min_uniques,
        )
        all_lineups.extend(lineups)

    # Calculate and store player exposures
    player_exposures = calculate_player_exposures(all_lineups)
    print("Debug: Optimization workflow completed")

    return all_lineups, player_exposures
