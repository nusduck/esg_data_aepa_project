import os
import json
from pathlib import Path
import google.generativeai as genai
from google.ai.generativelanguage_v1beta.types import content
from google.generativeai.types import HarmCategory, HarmBlockThreshold
from datetime import datetime
import logging
import yaml
from src.utils.file_io_read import read_text
from src.utils.file_io_save import save_json

def create_directories():
    directories = ['src/log/llm_greenwash', 'data/esg_green_wash']
    for directory in directories:
        os.makedirs(directory, exist_ok=True)

def setup_logging():
    current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_dir = 'src/log/llm_greenwash'
    log_file = os.path.join(log_dir, f'llm_greenwash_{current_time}.log')
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
    
    response_schema = content.Schema(
        type=content.Type.OBJECT,
        properties={
            "rate": content.Schema(type=content.Type.STRING),
            "reason": content.Schema(type=content.Type.STRING),
        }
    )
    
    return safety_settings, genai.GenerationConfig(
        response_mime_type="application/json",
        response_schema=response_schema
    )

class ESGAnalyzer:
    def __init__(self, config, specific_report=None):
        self.config = config
        self.safety_settings, self.generation_config = get_model_config()
        genai.configure(api_key=config['google']['api_keys'][0])
        self.model = genai.GenerativeModel(
            config['google']['model'],
            safety_settings=self.safety_settings,
            generation_config=self.generation_config
        )
        self.specific_report = specific_report
        
    def read_user_prompt(self):
        prompt_path = 'data/prompt/greenwashing/user_prompt.txt'
        with open(prompt_path, 'r', encoding='utf-8') as f:
            return f.read().strip()
    
    def read_txt_files(self):
        data_folder = 'data/esg_cleaned_data'
        files = []
        file_contents = []
        
        file_paths = read_text(data_folder, self.specific_report)
        if not isinstance(file_paths, list):
            file_paths = [file_paths]  # 如果是单个文件，转换为列表
        
        for file_path in file_paths:
            with open(file_path, 'r') as f:
                # 提取文件名（不含扩展名）
                files.append(Path(file_path).stem)
                file_contents.append(f.read())
                
        return files, file_contents

    def analyze_report(self, file_content, user_prompt):
        try:
            chat = self.model.start_chat(history=[{
                "role": "user",
                "parts": [file_content, user_prompt]
            }])
            
            response = chat.send_message("Based on the report content, please provide your analysis.")
            return json.loads(response.text)
            
        except Exception as e:
            logging.error(f'Error in analysis: {str(e)}')
            return None
    
    def process_and_save_results(self):
        files, file_contents = self.read_txt_files()
        user_prompt = self.read_user_prompt()
        results = {}
        
        for filename, content in zip(files, file_contents):
            logging.info(f'Processing file: {filename}')
            response = self.analyze_report(content, user_prompt)
            
            if response:
                # results.append({
                #     "report_name": filename,
                #     "response": response
                # })
                results[filename] = response
            else:
                logging.error(f'Failed to analyze file: {filename}')
        
        # Save results to JSON file
        # output_path = os.path.join(
        #     'data/esg_green_wash', 
        #     f'greenwashing_analysis_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
        # )
        
        # with open(output_path, 'w', encoding='utf-8') as f:
        #     json.dump(results, f, ensure_ascii=False, indent=2)
        output_path = 'data/esg_green_wash/greenwashing_analysis_result.json'
        save_json(results, output_path, self.specific_report)
        
        logging.info(f'Results saved to {output_path}')

def esg_washgreen_check(specific_report=None):
    create_directories()
    setup_logging()
    config = load_config()
    
    analyzer = ESGAnalyzer(config, specific_report)
    analyzer.process_and_save_results()

if __name__ == '__main__':
    esg_washgreen_check(specific_report="Singapore Reinsurance Corporation Limited_report.pdf")