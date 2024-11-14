import os
import pandas as pd
import sys
import json

def process_csv_files(directory_path):
    results = []
    with open(file=directory_path, mode='r') as f:
        df = pd.read_csv(f)
        df = df.drop_duplicates(subset='report', keep='last')
        # keep 2 decimal places
        df = df.round(2)
        df = df[['report', 'total_missing_fields_count', 'final_score']]
        results.append(df.to_dict(orient='records'))
    
    return results

if __name__ == "__main__":
    directory_path = sys.argv[1]
    results = process_csv_files(directory_path)
    print(json.dumps(results))