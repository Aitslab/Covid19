import pandas as pd
import json
import os

def prepare_and_filter_json_batches(metadata_csv, json_dir, output_json_path, output_csv_path="filtered_output.csv"):
    """
    Filters CORD-19 metadata by license, then filters multiple JSON batch files based on valid 'cord_uid's.

    Parameters:
        metadata_csv (str): Path to the original metadata.csv file.
        json_dir (str): Directory containing batch JSON files (each file is a dictionary).
        output_json_path (str): Path to save the combined filtered JSON output.
        output_csv_path (str): Path to save filtered CSV with cord_uid and license (default: 'filtered_output.csv').
    """
    # Step 1: Filter metadata.csv by license
    license_list = ['cc-by', 'cc-by-nc', 'cc0', 'cc-by-nc-nd',
                    'cc-by-nc-sa', 'cc-by-nd', 'cc-by-sa', 'pd']
    
    df = pd.read_csv(metadata_csv, low_memory=False)
    filtered_df = df[df['license'].isin(license_list)]
    final_df = filtered_df[['cord_uid', 'license']]
    final_df.to_csv(output_csv_path, index=False)
    print(f"Filtered metadata saved to: {output_csv_path}")

    # Step 2: Load valid keys from filtered CSV
    valid_keys = set(final_df['cord_uid'].dropna().astype(str))

    # Step 3: Filter each JSON file
    json_files = sorted([f for f in os.listdir(json_dir) if f.endswith(".json")])
    all_filtered_data = {}
    total_filtered_count = 0
    total_original_count = 0

    for i, filename in enumerate(json_files):
        filepath = os.path.join(json_dir, filename)

        with open(filepath, "r", encoding="utf-8") as f:
            batch = json.load(f)

        if isinstance(batch, dict):
            original_count = len(batch)
            filtered_batch = {k: v for k, v in batch.items() if k in valid_keys}
            filtered_count = len(filtered_batch)

            total_original_count += original_count
            total_filtered_count += filtered_count

            print(f"{filename} (Batch {i+1}): original = {original_count}, filtered = {filtered_count}")

            all_filtered_data.update(filtered_batch)
        else:
            print(f"{filename} is not a dictionary. Skipping.")

    # Step 4: Save the merged filtered JSON
    with open(output_json_path, "w", encoding="utf-8") as f:
        json.dump(all_filtered_data, f, indent=2)

    # Final summary
    print(f"\nTotal original objects across all files: {total_original_count}")
    print(f"Total filtered objects saved: {total_filtered_count}")



def main():
    metadata_csv = "metadata.csv"
    json_dir = "DVVM/"  # Folder containing JSON batch files
    output_json_path = "new_filtered_DVVM_merged.json"
    output_csv_path = "filtered_output.csv"

    prepare_and_filter_json_batches(metadata_csv, json_dir, output_json_path, output_csv_path)

# Entry point
if __name__ == "__main__":
    main()