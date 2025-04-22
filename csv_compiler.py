import os
import re
import json
import pandas as pd

def parse_filename(filename):
    pattern = r"result_(\d+)_percent_registered_users(\d+)_ramp(true|false)_(full|login)\.json"
    match = re.match(pattern, filename)
    if match:
        return {
            "registered_pct": int(match.group(1)),
            "user_count": int(match.group(2)),
            "ramp": match.group(3) == "true",
            "scenario": match.group(4)  
        }
    return {}

def flatten_dict(d, parent_key='', sep='_'):
    items = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)

def compile_to_csv(folder_path, output_csv="compiled_results.csv"):
    records = []

    for filename in os.listdir(folder_path):
        if filename.endswith(".json"):
            filepath = os.path.join(folder_path, filename)
            with open(filepath, 'r') as file:
                data = json.load(file)

            meta = parse_filename(filename)
            flat_metrics = flatten_dict(data.get("metrics", {}))
            flat_root_group = flatten_dict(data.get("root_group", {}))

            record = {**meta, **flat_metrics, **flat_root_group}
            record["filename"] = filename
            records.append(record)

    df = pd.DataFrame(records)
    df.to_csv(output_csv, index=False)
    return df

if __name__ == "__main__":
    folder_path = "./load_testing/results" 
    df = compile_to_csv(folder_path)
    print(df.head())
