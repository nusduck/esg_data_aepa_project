import os
import json
from pathlib import Path
import google.generativeai as genai
from google.ai.generativelanguage_v1beta.types import content
from google.generativeai.types import HarmCategory, HarmBlockThreshold
from datetime import datetime
import logging
import yaml
from src.utils.file_io_read import read_company_names
from src.utils.file_io_save import save_json

def create_directories():
    directories = ['src/log/llm_search', 'data/esg_realtime_info']
    for directory in directories:
        os.makedirs(directory, exist_ok=True)

def setup_logging():
    current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_dir = 'src/log/llm_search'
    log_file = os.path.join(log_dir, f'llm_search_{current_time}.log')
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )

def load_config():
    with open('config/config.yaml', 'r') as config_file:
        return yaml.safe_load(config_file)

def get_model_config():
    safety_settings = {
        HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
    }
    
    
    
    return safety_settings

class ESGAnalyzer:
    def __init__(self, config, specific_report=None):
        self.config = config
        self.safety_settings = get_model_config()
        genai.configure(api_key=config['google']['api_keys'][0])
        self.model = genai.GenerativeModel(
            config['google']['model'],
            safety_settings=self.safety_settings,
        )
        self.specific_report = specific_report
        
    def read_user_prompt(self):
        prompt_path = 'data/prompt/real_time_info/user_prompt.txt'
        with open(prompt_path, 'r', encoding='utf-8') as f:
            return f.read().strip()
    
    def get_company_names(self):
        data_folder = 'data/esg_cleaned_data'
        company_names = read_company_names(data_folder,specific_report=self.specific_report)
        
        # for file_path in Path(data_folder).glob('*.txt'):
        #     # Extract company name from filename (remove '_report.txt')
        #     company_name = file_path.stem.replace('_report', '')
        #     company_names.append(company_name)
                
        return company_names

    def analyze_company(self, company_name, user_prompt):
        try:
            # Format the prompt with company name
            formatted_prompt = user_prompt.format(company_name=company_name)
            
            # Use generate_content with web search enabled
            response = self.model.generate_content(
                formatted_prompt,
                tools='google_search_retrieval'
            )
            
            return response.text
            
        except Exception as e:
            logging.error(f'Error in analysis for {company_name}: {str(e)}')
            return None
    
    def process_and_save_results(self):
        company_names = self.get_company_names()
        user_prompt = self.read_user_prompt()
        results = {}
        
        for company_name in company_names:
            logging.info(f'Processing company: {company_name}')
            response = self.analyze_company(company_name, user_prompt)
            
            if response:
                # results.append({
                #     "company_name": company_name,
                #     "timestamp": datetime.now().isoformat(),
                #     "esg_insights": response
                # })
                results[company_name] = {
                    "timestamp": datetime.now().isoformat(),
                    "esg_insights": response
                }
            else:
                logging.error(f'Failed to analyze company: {company_name}')
        
        # Save results to JSON file
        # output_path = os.path.join(
        #     'data/esg_realtime_info', 
        #     f'esg_realtime_analysis_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
        # )
        
        # with open(output_path, 'w', encoding='utf-8') as f:
        #     json.dump(results, f, ensure_ascii=False, indent=2)
        output_path = 'data/esg_realtime_info/esg_realtime_info_obtain.json'
        save_json(results, output_path)
        
        logging.info(f'Results saved to {output_path}')

def esg_realtime_obtain(specific_report=None):
    create_directories()
    setup_logging()
    config = load_config()
    
    analyzer = ESGAnalyzer(config,specific_report)
    analyzer.process_and_save_results()

if __name__ == '__main__':
    esg_realtime_obtain(specific_report='IFS Capital Limited_report.pdf')