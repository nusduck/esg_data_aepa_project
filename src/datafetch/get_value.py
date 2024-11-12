import json
import os
import sys
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from scipy.stats import zscore
import numpy as np  


def process_json_files(directory_path):
    results = []
    for filename in os.listdir(directory_path):
        if filename.endswith('.json'):
            file_path = os.path.join(directory_path, filename)
            with open(file_path, encoding='utf-8') as f:
                data = json.load(f)
                # Extract each company's question_id, value, and unit in the desired format
                extracted_data = {}

                for company, responses in data.items():
                    extracted_data[company] = []
                    for response in responses:
                        question_id = response.get("question_id")
                        value = response.get("response", {}).get("value")
                        unit = response.get("response", {}).get("unit")
                        
                        # Append extracted data for each question to the company list
                        extracted_data[company].append({
                            "metric": question_id,
                            "value": value,
                            "unit": unit
                        })

                # Save the extracted data to a new JSON file
                output_path = 'data/esg_scores/extracted_esg_data.json'  # 替换为保存路径
                with open(output_path, 'w', encoding='utf-8') as output_file:
                    json.dump(extracted_data, output_file, ensure_ascii=False, indent=2)
    return results

def get_company_value(directory_path, company):
    try:
        with open(directory_path, encoding='utf-8') as f:
            data = json.load(f)
            company = company + '_report'
            company_data = data.get(company)
            if company_data is None:
                return None

            company_value = {}
            for response in company_data:
                question_id = response.get("metric")
                value = response.get("value")
                unit = response.get("unit")
                company_value[question_id] = {
                    "value": value,
                    "unit": unit
                }

        return company_value
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


if __name__ == "__main__":
    process_json_files('data/esg_validation')
    directory_path = sys.argv[1]
    company = sys.argv[2] if len(sys.argv) > 2 else None
    results = get_company_value(directory_path, company)
    print(json.dumps(results, indent=2, separators=(',', ': ')))