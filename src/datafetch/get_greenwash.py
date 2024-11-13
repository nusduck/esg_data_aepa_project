import os
import pandas as pd
import sys
import json
import subprocess


def process_greenwash_file(directory_path, company):
    try:
        results = []
        result = {}
        company = company + '_report'
        for filename in os.listdir(directory_path):
            if filename.endswith('.json'):
                file_path = os.path.join(directory_path, filename)
                with open(file_path, encoding='utf-8') as f:
                    data = json.load(f)
                    for item in data:
                        if item['report_name'] == company:
                            result = {
                                "rate": item['response']['rate'],
                                "reason": item['response']['reason']
                            }
                            results.append(result)
                            break
            if results:
                break
            
        if results is not None:
            results = json.dumps(results, separators=(',', ':'))
        else:
            results = json.dumps({'message': 'No matching report found'}, separators=(',', ':'))
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
        
