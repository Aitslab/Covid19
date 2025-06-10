import pandas as pd
import json

def filter_metadata_csv(input_csv: str, output_csv: str, license_list: list) -> pd.DataFrame:
    df = pd.read_csv(input_csv, low_memory=False)
    filtered_df = df[df['license'].isin(license_list)]
    final_df = filtered_df[['cord_uid', 'license']]
    final_df.to_csv(output_csv, index=False)
    return final_df

def filter_json_by_keys(json_file: str, valid_keys: set, output_json_file: str) -> int:
    with open(json_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    all_filtered_data = {}
    total_filtered_count = 0

    for i, batch in enumerate(data):
        filtered_batch = {k: v for k, v in batch.items() if k in valid_keys}
        batch_count = len(filtered_batch)
        total_filtered_count += batch_count
        print(f"Batch {i+1}: {batch_count} filtered objects")
        all_filtered_data.update(filtered_batch)

    with open(output_json_file, "w", encoding="utf-8") as f:
        json.dump(all_filtered_data, f, indent=2)

    return total_filtered_count

def main():
    license_list = ['cc-by', 'cc-by-nc', 'cc0', 'cc-by-nc-nd',
                    'cc-by-nc-sa', 'cc-by-nd', 'cc-by-sa', 'pd']
    
    # Step 1: Filter CSV by license
    filtered_df = filter_metadata_csv("metadata.csv", "filtered_output.csv", license_list)
    
    # Step 2: Extract valid keys from filtered CSV
    valid_keys = set(filtered_df['cord_uid'].dropna().astype(str))
    
    # Step 3: Filter JSON by those keys
    total = filter_json_by_keys("DVVM_merged.json", valid_keys, "filtered_DVVM_merged.json")
    
    print(f"\nTotal filtered objects saved: {total}")

if __name__ == "__main__":
    main()