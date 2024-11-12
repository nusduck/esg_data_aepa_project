import os
import time
import json
from pathlib import Path
import google.generativeai as genai
from google.ai.generativelanguage_v1beta.types import content
from google.generativeai.types import HarmCategory, HarmBlockThreshold
from google.generativeai.protos import Part
from datetime import datetime
import logging
import yaml
import pandas as pd
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from src.utils.file_io_read import read_text
from src.utils.file_io_save import save_json

# Create necessary directories
def create_directories():
    directories = ['src/log/llm_retrieve', 'data/esg_retrieve']
    for directory in directories:
        os.makedirs(directory, exist_ok=True)

# Set up logging
def setup_logging():
    current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_dir = 'src/log/llm_retrieve'
    log_file = os.path.join(log_dir, f'llm_retrieve_{current_time}.log')
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )

# Load configuration
def load_config():
    with open('config/config.yaml', 'r') as config_file:
        return yaml.safe_load(config_file)

# Initialize Gemini model configuration
def get_model_config():
    safety_settings = {
        HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
    }
    
    response_schema = content.Schema(
        type=content.Type.OBJECT,
        required = ['value', 'unit', 'from_sentences'],
        properties={
            "value": content.Schema(type=content.Type.STRING),
            "unit": content.Schema(type=content.Type.STRING),
            "from_sentences": content.Schema(type=content.Type.STRING),
        },
    )
    
    return safety_settings, genai.GenerationConfig(
        response_mime_type="application/json",
        response_schema=response_schema
    )

class APIKeyManager:
    def __init__(self, api_keys):
        self.api_keys = api_keys
        self.current_index = 0
        self.max_index = len(api_keys) - 1

    def get_next_key(self):
        self.current_index = (self.current_index + 1) % len(self.api_keys)
        return self.api_keys[self.current_index]

    def get_current_key(self):
        return self.api_keys[self.current_index]

class ESGDataRetriever:
    def __init__(self, config, specific_report=None):
        self.config = config
        self.api_key_manager = APIKeyManager(config['google']['api_keys'])
        self.safety_settings, self.generation_config = get_model_config()
        self.model = self.configure_model()
        self.max_retries = 3
        self.specific_report = specific_report
        
    def configure_model(self):
        genai.configure(api_key=self.api_key_manager.get_current_key())
        return genai.GenerativeModel(
            self.config['google']['model'],
            safety_settings=self.safety_settings,
            generation_config=self.generation_config
        )

    def rotate_api_key(self):
        """Rotate to next API key and reconfigure model"""
        new_key = self.api_key_manager.get_next_key()
        logging.info(f"Rotating to next API key...")
        genai.configure(api_key=new_key)
        self.model = genai.GenerativeModel(
            self.config['google']['model'],
            safety_settings=self.safety_settings,
            generation_config=self.generation_config
        )
    
    def read_txt_files(self):
        data_folder = 'data/esg_cleaned_data'
        files = []
        file_contents = []
        
        # 获取文件路径列表
        file_paths = read_text(data_folder, self.specific_report)
        if not isinstance(file_paths, list):
            file_paths = [file_paths]  # 如果是单个文件，转换为列表
        
        for file_path in file_paths:
            with open(file_path, 'rb') as f:
                # 提取文件名（不含扩展名）
                files.append(Path(file_path).stem)
                file_contents.append(f.read())
                
        return files, file_contents
    
    def read_questions(self):
        data_folder = 'data/esg_retrieve'
        return pd.read_excel(os.path.join(data_folder, 'retrieve_questions.xlsx'))

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        retry=retry_if_exception_type((Exception)),
        before_sleep=lambda retry_state: logging.warning(
            f"Attempt {retry_state.attempt_number} failed. Retrying in {retry_state.next_action.sleep} seconds..."
        )
    )
    def retrieve_esg_data(self, file_content):
        file = Part(inline_data={'mime_type': 'text/plain', 'data': file_content})
        history = [{
            "role": "user",
            "parts": [
                file,
                "please based on these reports answer me the following question, first please read it carefully."
            ],
        }]
        
        try:
            chat = self.model.start_chat(history=history)
            return chat
        except Exception as e:
            logging.error(f'Error in retrieving data: {str(e)}')
            self.rotate_api_key()  # Rotate API key before retry
            raise  # Re-raise the exception for retry mechanism

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        retry=retry_if_exception_type((Exception)),
        before_sleep=lambda retry_state: logging.warning(
            f"Attempt {retry_state.attempt_number} failed. Retrying in {retry_state.next_action.sleep} seconds..."
        )
    )
    def send_message(self, chat_session, question):
        try:
            return chat_session.send_message(
                f"based on the reports answer the question: {question} If you can't find the proper answer please return N/A to the value."
            )
        except Exception as e:
            logging.error(f'Error sending message: {str(e)}')
            self.rotate_api_key()  # Rotate API key before retry
            raise  # Re-raise the exception for retry mechanism
    
    def process_and_save_results(self):
        files, file_contents = self.read_txt_files()
        questions = self.read_questions()
        results = {}
        
        total_files = len(files)
        logging.info(f"开始处理共 {total_files} 个文件")
        
        for i, (filename, content) in enumerate(zip(files, file_contents), 1):
            logging.info(f"正在处理第 {i}/{total_files} 个文件: {filename}")
            retry_count = 0
            while retry_count < self.max_retries:
                try:
                    chat_session = self.retrieve_esg_data(content)
                    if not chat_session:
                        retry_count += 1
                        continue

                    file_results = []
                    logging.info(f"开始处理 {filename} 的问题回答")
                    for j in range(len(questions)):
                        question_id = questions.iloc[j, 0]
                        question = questions.iloc[j, 1]
                        
                        try:
                            response = self.send_message(chat_session, question)
                            
                            if response:
                                logging.info(f'文件 {filename}: 成功检索问题 {question_id}')
                                try:
                                    response_data = json.loads(response.text)
                                    file_results.append({
                                        'question_id': question_id,
                                        'response': response_data
                                    })
                                except json.JSONDecodeError as e:
                                    logging.error(f'文件 {filename}: 解析问题 {question_id} 的JSON响应时出错: {str(e)}')
                            else:
                                logging.error(f'文件 {filename}: 问题 {question_id} 未获得响应')
                                
                        except Exception as e:
                            logging.error(f'文件 {filename}: 处理问题 {question_id} 时出错: {str(e)}')
                            continue

                    results[filename] = file_results
                    logging.info(f"完成文件 {filename} 的处理 ({i}/{total_files})")
                    break  # Success, break the retry loop
                
                except Exception as e:
                    retry_count += 1
                    logging.error(f'文件 {filename} 的第 {retry_count} 次尝试失败: {str(e)}')
                    if retry_count < self.max_retries:
                        time.sleep(2 ** retry_count)  # Exponential backoff
                    else:
                        logging.error(f'文件 {filename} 在 {self.max_retries} 次尝试后处理失败')
        
        logging.info(f"所有 {total_files} 个文件处理完成")
        
        # Save results to JSON file
        # output_path = os.path.join('data/esg_retrieve', f'results_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json')
        # with open(output_path, 'w', encoding='utf-8') as f:
        #     json.dump(results, f, ensure_ascii=False, indent=2)
        output_path = 'data/esg_retrieve/esg_retrieve_result.json'
        save_json(results, output_path, self.specific_report)
        logging.info(f'结果已保存至 {output_path}')

def esg_data_retrieve(specific_report=None):
    create_directories()
    setup_logging()
    config = load_config()
    
    retriever = ESGDataRetriever(config, specific_report)
    retriever.process_and_save_results()

if __name__ == '__main__':
    esg_data_retrieve(specific_report='IFS Capital Limited_report.pdf')