import os
import pandas as pd
from datetime import datetime
import shutil

def find_csv_with_keywords(*keywords):
    """
    Search the current directory for a CSV file containing all specified keywords in its name.

    Args:
        *keywords (str): Keywords to search for in the filename.

    Returns:
        str: The path to the found CSV file.
    """
    for file in os.listdir('.'):
        if file.endswith('.csv') and all(keyword in file for keyword in keywords):
            return file
    raise FileNotFoundError(f"No CSV file found with keywords: {', '.join(keywords)}.")

def merge_dk_ftn(dk_file, ftn_file):
    """
    Merge the DraftKings CSV with the FTN projections CSV based on the 'Id' column.

    Args:
        dk_file (str): Path to the DraftKings CSV file.
        ftn_file (str): Path to the FTN projections CSV file.

    Returns:
        pd.DataFrame: Merged DataFrame.
    """
    # Load the DraftKings and FTN projections files
    dk_df = pd.read_csv(dk_file)
    ftn_df = pd.read_csv(ftn_file)

    # Standardize headers for merge consistency
    dk_df.rename(columns={'ID': 'Id'}, inplace=True)
    dk_df['Id'] = dk_df['Id'].astype(str)
    ftn_df['Id'] = ftn_df['Id'].astype(str)

    # Merge the files (left join to retain all DraftKings players)
    merged_df = dk_df.merge(ftn_df, on='Id', how='left')

    # Fill missing projections with default values
    merged_df['ProjPts'] = merged_df['ProjPts'].fillna(0)
    merged_df['ProjOwn'] = merged_df['ProjOwn'].fillna(0)

    # Add a timestamp column
    merge_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    merged_df['merge_time'] = merge_time

    return merged_df

def move_ftn_to_previous(ftn_file, target_dir='data/ftn_previous/'):
    """
    Move the processed FTN file to the ftn_previous subdirectory.

    Args:
        ftn_file (str): Path to the FTN projections CSV file.
        target_dir (str): Directory where the file should be moved.
    """
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
    shutil.move(ftn_file, os.path.join(target_dir, os.path.basename(ftn_file)))

def main():
    try:
        # Dynamically locate the CSV files
        dk_file = find_csv_with_keywords('DK', 'Salaries')
        ftn_file = find_csv_with_keywords('ftn', 'projections')

        print(f"DraftKings CSV found: {dk_file}")
        print(f"FTN Projections CSV found: {ftn_file}")

        # Merge the files
        merged_df = merge_dk_ftn(dk_file, ftn_file)

        # Print results to terminal for verification
        print("Merged Data:")
        print(merged_df.head())

        # Save the merged file
        merged_df.to_csv('merged_projections.csv', index=False)
        print("\nMerged projections saved as 'merged_projections.csv'.")

        # Move the FTN file to the ftn_previous directory
        move_ftn_to_previous(ftn_file)
        print(f"FTN Projections CSV moved to 'ftn_previous/'.")

    except FileNotFoundError as e:
        print(e)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()

