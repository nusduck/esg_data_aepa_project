import os
import pandas as pd
import sys
import json

def process_csv_files(directory_path, company):
    results = []
    for filename in os.listdir(directory_path):
        if filename.endswith('.csv'):
            file_path = os.path.join(directory_path, filename)
            df = pd.read_csv(file_path)
            # Remove rows with same campany name
            df = df.drop_duplicates(subset='Company', keep='first')
            if company:
                company = company + '_report'
                df = df[df['Company'] == company]
                # keep 2 decimal places
                df = df.round(2)
            results.append(df.to_dict(orient='records'))
    return results

if __name__ == "__main__":
    directory_path = sys.argv[1]
    company = sys.argv[2] if len(sys.argv) > 2 else None
    results = process_csv_files(directory_path, company)
    print(json.dumps(results))