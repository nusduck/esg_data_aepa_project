import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
from typing import List, Dict, Optional
import logging
import yaml
import os
import time
import concurrent.futures
import json
from datetime import datetime
from dataclasses import dataclass
from pathlib import Path

@dataclass
class AnnotationConfig:
    """Configuration class for annotation settings"""
    api_keys: List[str]
    model_name: str
    max_retries: int = 2
    retry_delay: int = 3
    safety_settings: Dict = None
    
    def __post_init__(self):
        if not self.safety_settings:
            self.safety_settings = {
                HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
            }

class GeminiAnnotator:
    def __init__(self, config_path: str):
        self.config = self._load_config(config_path)
        self.current_api_key_index = 0
        self.prompts = self._load_prompts()
        self._setup_logging()
        
    @staticmethod
    def _load_config(config_path: str) -> AnnotationConfig:
        with open(config_path, 'r') as f:
            config_data = yaml.safe_load(f)
        return AnnotationConfig(
            api_keys=config_data['google']['api_keys'],
            model_name=config_data['google']['model']
        )
    
    def _load_prompts(self) -> Dict[str, str]:
        prompts = {}
        prompt_files = {
            'default': 'data/prompt/anotation/user_prompt.txt',
            'system': 'data/prompt/anotation/system_prompt.txt'
        }
        for key, path in prompt_files.items():
            with open(path, 'r', encoding='utf-8') as f:
                prompts[key] = f.read()
        return prompts
    
    def _setup_logging(self):
        log_dir = Path('src/log/llm_label')
        log_dir.mkdir(parents=True, exist_ok=True)
        
        current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = log_dir / f'llm_label_{current_time}.log'
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
    
    def _configure_model(self) -> genai.GenerativeModel:
        genai.configure(api_key=self.config.api_keys[self.current_api_key_index])
        generation_config = {
        "temperature": 0,
        "top_p": 0.95,
        "top_k": 40,
        "max_output_tokens": 8192,
        "response_mime_type": "text/plain",
        }
        return genai.GenerativeModel(
            self.config.model_name,
            safety_settings=self.config.safety_settings,
            system_instruction=self.prompts['system'],
            generation_config=generation_config
        )
    
    def _rotate_api_key(self):
        self.current_api_key_index = (self.current_api_key_index + 1) % len(self.config.api_keys)
        logging.info(f"Rotating API key to: {self.config.api_keys[self.current_api_key_index]}")
    
    @staticmethod
    def _convert_to_json(text_content: str) -> str:
        """Convert BIO labeled text to JSON format"""
        lines = [line for line in text_content.split('\n') if len(line.split()) >= 2]
        current_text = []
        entity_spans = []
        
        for line in lines:
            word, label = line.rsplit(' ', 1)
            word = word.strip()
            label = label.strip()
            current_text.append(word)
            
            start_idx = len(' '.join(current_text)) - len(word)
            end_idx = start_idx + len(word)
            
            entity_spans.append({
                "start": start_idx,
                "end": end_idx,
                "text": word,
                "labels": [label]
            })
        
        return json.dumps({
            "text": ' '.join(current_text),
            "entity": entity_spans
        }, ensure_ascii=False, indent=2)

    def _process_single_text(self, text: str, index: int, model: genai.GenerativeModel) -> tuple:
        """Process a single text with retries"""
        for attempt in range(self.config.max_retries):
            try:
                # response = model.generate_content([self.prompts['default'], text])
                chat = model.start_chat(
                history=[
                    {"role": "user", "parts": self.prompts['default']},
                    ]
                )
                response = chat.send_message(text)
                
                if not response.candidates or not response.candidates[0].content:
                    raise ValueError(f"No content generated for text {index}")
                
                content = response.candidates[0].content.parts[0].text
                if '```' in content:
                    content = content.replace('```', '')
                # logging.info(f"Text{index}:\n {text} content:\n {content}")
                return index, self._convert_to_json(content)
                
            except Exception as e:
                logging.error(f"Attempt {attempt + 1} failed for text {index}: {str(e)}")
                if attempt < self.config.max_retries - 1:
                    self._rotate_api_key()
                    model = self._configure_model()
                    time.sleep(self.config.retry_delay)
                else:
                    return index, json.dumps({"error": f"Failed to process text {index}"})
                

    def process_texts(self, texts: List[str], output_dir: str, filename: str, 
                     max_workers: int = 1) -> None:
        """Process multiple texts concurrently"""
        output_path = Path(output_dir) / filename
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        model = self._configure_model()
        results = [None] * len(texts)
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_text = {
                executor.submit(self._process_single_text, text, idx, model): idx 
                for idx, text in enumerate(texts)
            }
            
            for future in concurrent.futures.as_completed(future_to_text):
                idx, content = future.result()
                results[idx] = content
                
        # Write results to file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write('[\n' + ',\n'.join(result for result in results if result) + '\n]')

def process_folder(folder_path: str, config_path: str, output_dir: str, max_workers: int = 2):
    """Process all files in a folder"""
    annotator = GeminiAnnotator(config_path)
    folder_path = Path(folder_path)
    
    for file_path in folder_path.glob('*.txt'):
        texts = []
        with open(file_path, 'r', encoding='utf-8') as f:
            texts.extend(line for line in f.read().split('\n') if line.strip())
        
        output_filename = file_path.stem + '.json'
        annotator.process_texts(
            texts=texts,
            output_dir=output_dir,
            filename=output_filename,
            max_workers=max_workers
        )

if __name__ == '__main__':
    process_folder(
        folder_path="data/esg_cleaned_data/",
        config_path="config/config.yaml",
        output_dir="data/esg_label_result",
        max_workers=1
    )