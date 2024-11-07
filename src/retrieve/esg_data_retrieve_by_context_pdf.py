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

# Create necessary directories
def create_directories():
    directories = ['src/log/llm_retrieve', 'data/esg_retrieve']
    for directory in directories:
        os.makedirs(directory, exist_ok=True)

# Set up logging
def setup_logging():
    current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_dir = 'src/log/llm_retrieve'
    log_file = os.path.join(log_dir, f'llm_parse_{current_time}.log')
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
    def __init__(self, config):
        self.config = config
        self.api_key_manager = APIKeyManager(config['google']['api_keys'])
        self.safety_settings, self.generation_config = get_model_config()
        self.model = self.configure_model()
        self.max_retries = 3
        
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
        data_folder = 'data/esg_reports_pdf'
        files = []
        file_contents = []
        
        for file_path in Path(data_folder).glob('*.pdf'):
            with open(file_path, 'rb') as f:
                files.append(file_path.stem)  # Store filename without extension
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
        file = Part(inline_data={'mime_type': 'application/pdf', 'data': file_content})
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
                f"based on the reports answer the question: {question}"
            )
        except Exception as e:
            logging.error(f'Error sending message: {str(e)}')
            self.rotate_api_key()  # Rotate API key before retry
            raise  # Re-raise the exception for retry mechanism
    
    def process_and_save_results(self):
        files, file_contents = self.read_txt_files()
        questions = self.read_questions()
        results = {}
        
        for i, (filename, content) in enumerate(zip(files, file_contents)):
            retry_count = 0
            while retry_count < self.max_retries:
                try:
                    chat_session = self.retrieve_esg_data(content)
                    if not chat_session:
                        retry_count += 1
                        continue

                    file_results = []
                    for j in range(len(questions)):
                        question_id = questions.iloc[j, 0]
                        question = questions.iloc[j, 1]
                        
                        try:
                            response = self.send_message(chat_session, question)
                            
                            if response:
                                logging.info(f'Retrieved data for {question_id}')
                                try:
                                    response_data = json.loads(response.text)
                                    file_results.append({
                                        'question_id': question_id,
                                        'response': response_data
                                    })
                                except json.JSONDecodeError as e:
                                    logging.error(f'Error parsing JSON response for {question_id}: {str(e)}')
                            else:
                                logging.error(f'No response for {question_id}')
                                
                        except Exception as e:
                            logging.error(f'Error processing question {question_id}: {str(e)}')
                            continue

                    results[filename] = file_results
                    break  # Success, break the retry loop
                
                except Exception as e:
                    retry_count += 1
                    logging.error(f'Attempt {retry_count} failed for file {filename}: {str(e)}')
                    if retry_count < self.max_retries:
                        time.sleep(2 ** retry_count)  # Exponential backoff
                    else:
                        logging.error(f'Failed to process file {filename} after {self.max_retries} attempts')
        
        # Save results to JSON file
        output_path = os.path.join('data/esg_retrieve', f'results_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json')
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        
        logging.info(f'Results saved to {output_path}')

def main():
    create_directories()
    setup_logging()
    config = load_config()
    
    retriever = ESGDataRetriever(config)
    retriever.process_and_save_results()

if __name__ == '__main__':
    main()