import os
import pandas as pd
import sys
import json
import subprocess


def process_greenwash_file(directory_path, company):
    try:
        results = []
        company = company + '_report'
        with open(directory_path, encoding='utf-8') as f:
            data = json.load(f)
            data = data.get(company)
            results.append(data)
        results = json.dumps(results, separators=(',', ':')) 
        return results
    except subprocess.CalledProcessError as e:
        return {
            'message': 'Process failed!',
            'error': e.stderr
        }
        
if __name__ == '__main__':
    directory_path = sys.argv[1]
    company = sys.argv[2]
    print(process_greenwash_file(directory_path, company))
        
