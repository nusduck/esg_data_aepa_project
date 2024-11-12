import os
import pandas as pd
import sys
import json
import subprocess


def process_realtime_file(directory_path, company):
    try:
        # result = subprocess.run(['python', 'src/realtime/llm_esg_realtime_info_search.py'], capture_output=True, text=True, check=True)
        results = []
        for filename in os.listdir(directory_path):
            if filename.endswith('.json'):
                file_path = os.path.join(directory_path, filename)
                with open(file_path, encoding='utf-8') as f:
                    data = json.load(f)
                    for i in data:
                        if i['company_name'] == company:
                            news = {
                                'insight': i['esg_insights'],
                                'timestamp': i['timestamp'].split('T')[0]
                            }
                            results.append(news)
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
    print(process_realtime_file(directory_path, company))
        
