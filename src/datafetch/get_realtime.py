import os
import pandas as pd
import sys
import json
import subprocess


def process_realtime_file(directory_path, company):
    try:
        result = subprocess.run(['python', 'src/realtime/llm_esg_realtime_info_search.py'], capture_output=True, text=True, check=True)
        results = []
        for filename in os.listdir(directory_path):
            if filename.endswith('.json'):
                file_path = os.path.join(directory_path, filename)
        
        
        return {
            'message': 'Process completed successfully!',
            'output': result.stdout
        }
    except subprocess.CalledProcessError as e:
        return {
            'message': 'Process failed!',
            'error': e.stderr
        }
        
