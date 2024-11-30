import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Set user parameters
VARIANCE_RANGE = 0.1  # ±10% variance
NUM_PROJECTION_SETS = 100  # Number of unique projection sets to generate

# Set file paths
TEST_DIR = os.path.dirname(os.path.abspath(__file__))
TEST_PLAYER_POOL_FILE = os.path.join(TEST_DIR, "test_player_pool.csv")














def generate_projection_sets(player_pool, num_sets, variance_range):
    """
    Generates multiple sets of projections with asymmetric variance.

    Args:
        player_pool (pd.DataFrame): Original player pool with base projections.
        num_sets (int): Number of projection sets to generate.
        variance_range (float): Base variance range (percentage).

    Returns:
        list of pd.DataFrame: List of projection sets with adjusted projections.
    """
    projection_sets = []

    for _ in range(num_sets):
        # Generate asymmetric variance
        lower_variance = np.random.normal(
            loc=-0.5 * variance_range, scale=variance_range / 6, size=len(player_pool)
        )
        upper_variance = np.random.normal(
            loc=0.5 * variance_range, scale=variance_range / 3, size=len(player_pool)
        )
        total_variance = np.where(
            np.random.rand(len(player_pool)) < 0.5, lower_variance, upper_variance
        )

        # Apply variance to projections
        total_variance = np.clip(total_variance, -variance_range, variance_range)
        adjusted_projections = player_pool["ProjPts"] * (1 + total_variance)

        # Create new projection set
        projection_set = player_pool.copy()
        projection_set["AdjProjPts"] = adjusted_projections
        projection_sets.append(projection_set)

    return projection_sets






























def analyze_distribution(projection_sets, player_pool):
    """
    Analyzes and plots the distribution of percentage-based adjustments for each position.

    Args:
        projection_sets (list of pd.DataFrame): List of DataFrames with adjusted projections.
        player_pool (pd.DataFrame): Original player pool with base projections.
    """
    # Combine all projection sets into one DataFrame for easier visualization
    combined_data = pd.concat(projection_sets, keys=range(len(projection_sets)), names=["Set"])
    combined_data = combined_data.reset_index(level="Set").reset_index(drop=True)

    # Ensure that the base projections are repeated to match combined_data
    repeated_proj_pts = pd.concat([player_pool["ProjPts"]] * len(projection_sets), ignore_index=True)

    # Calculate the percentage adjustment
    combined_data["PctAdjustment"] = (
        (combined_data["AdjProjPts"] - repeated_proj_pts) / repeated_proj_pts
    ) * 100

    # Plot the distribution for each position
    positions = player_pool["Position"].unique()

    for pos in positions:
        pos_data = combined_data[combined_data["Position"] == pos]

        plt.figure(figsize=(8, 6))
        plt.hist(
            [pos_data[pos_data["PctAdjustment"] > 0]["PctAdjustment"],
             pos_data[pos_data["PctAdjustment"] < 0]["PctAdjustment"]],
            bins=30,
            stacked=True,
            label=[f"{pos} Gained", f"{pos} Lost"],
            color=["green", "red"]
        )
        plt.title(f"Distribution of Percentage Adjustments for {pos}")
        plt.xlabel("Percentage Adjustment (%)")
        plt.ylabel("Frequency")
        plt.legend()
        plt.tight_layout()
        plt.show()






def main():
    # Load the test player pool
    print("Loading test player pool...")
    try:
        player_pool = pd.read_csv(TEST_PLAYER_POOL_FILE)
    except FileNotFoundError:
        print(f"Error: Test player pool not found at {TEST_PLAYER_POOL_FILE}")
        return

    # Generate projection sets
    print("Generating projection sets...")
    projection_sets = generate_projection_sets(player_pool, NUM_PROJECTION_SETS, VARIANCE_RANGE)

    # Analyze variance and distribution
    print("Analyzing variance and distribution...")
    analyze_distribution(projection_sets, player_pool)


if __name__ == "__main__":
    main()
