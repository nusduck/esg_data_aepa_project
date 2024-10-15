import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
from typing import List, Tuple, Optional, Dict
import logging
import yaml
import os
import time
import concurrent.futures
import json
import datetime

# Load configuration
with open('config/demo_config.yaml', 'r') as config_file:
    config = yaml.safe_load(config_file)

# Initialize Gemini-Flash model
api_keys = config['google']['api_keys']
current_api_key_index = 0
safety_settings = {
    HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
}



with open('data/prompt/label_prompt.txt', 'r') as file:
    DEFAULT_PROMPT = file.read()

def configure_ner_model():
    global current_api_key_index
    genai.configure(api_key=api_keys[current_api_key_index])
    return genai.GenerativeModel(config['google']['model'], safety_settings=safety_settings, system_instruction=DEFAULT_PROMPT)


def _gemini_annotate_text(
        texts: List[str],
        prompt_dict: Optional[Dict] = None,
        output_dir: str = './',
        file_name: str = ' ',
        verbose: bool = False,
        gemini_worker: int = 1
) -> str:
    """
    Use the Google Gemini model to automatically annotate the text and save the annotation results.
    """
    if isinstance(prompt_dict, dict) and 'prompt' in prompt_dict:
        prompt = prompt_dict['prompt']
        logging.info("Use user prompt")
    else:
        prompt = DEFAULT_PROMPT
        logging.info("Use default prompt")

    def _process_text(index: int, text: str) -> Tuple[int, str]:
        global ner_model, current_api_key_index
        logging.info(f'Gemini annotate text: {index}')

        try:
            # use the Gemini model for NER annotation
            response = ner_model.generate_content([prompt, text])
            logging.info(f"Generate annotated content for text: {index}")

            if not response.candidates or not response.candidates[0].content:
                logging.warning(f"NO.{index} text response has no content or is blocked.")
                return index, f"[NO.{index} does not generate any annotated content.]"

            content = response.candidates[0].content.parts[0].text

            if not content:
                logging.warning(f"NO.{index} text response has no content")
                return index, f"[NO.{index} does not generate any annotated content.]"
            
            content = txt_to_json(content)
            
            return index, content

        except Exception as e:
            logging.error(f"Error processing NO.{index} : {str(e)}")
            current_api_key_index = (current_api_key_index + 1) % len(api_keys)
            ner_model = configure_ner_model()
            time.sleep(60)
            return _process_text(index, text)  # retry

    contents = [None] * len(texts)
    with concurrent.futures.ThreadPoolExecutor(max_workers=gemini_worker) as executor:
        futures = [executor.submit(_process_text, index, text) for index, text in enumerate(texts)]
        for future in concurrent.futures.as_completed(futures):
            index, content = future.result()
            print(content) if not verbose else None
            contents[index] = content

    output_path = os.path.join(output_dir, file_name)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('[' + ',\n'.join(contents) + ']')

    return '[' + ',\n'.join(contents) + ']'

def process_strings_with_annotations(
        strings: List[str],
        output_dir: str = './',
        file_name: str = ' ',
        verbose: bool = False,
        gemini_worker: int = 1
):
    """
    Annotate the string list with NER and output the annotation results.
    """
    result = _gemini_annotate_text(
        texts=strings,
        output_dir=output_dir,
        file_name=file_name,
        verbose=verbose,
        gemini_worker=gemini_worker
    )
    logging.info("Complete the annotation of the text.")

def txt_to_json(txt_content):
    # Read the data
    data = txt_content.split('\n')
    total = []  # store the final result

    # initial the variable
    current_text = []
    entity_spans = []

    # Iterate through the BIO labeled rows
    for line in data:
        # Check if it's a legal line (must have words and tags)
        if len(line.split(' ')) < 2:
            continue

        word, label = line.rsplit(' ', 1)  # Obtain words and tags
        current_text.append(word)  # Add words to complete text

        # Calculate the start and end positions of the current word
        start_idx = len(' '.join(current_text)) - len(word)  # Starting index of the current word
        end_idx = start_idx + len(word)  # End index of the current word

        # Add each word and label to the list of entities
        entity_spans.append({
            "start": start_idx,
            "end": end_idx,
            "text": word,
            "labels": [label]
        })
        
    # Concatenate complete text into strings
    combined_text = ' '.join(current_text)

    # Construct the output JSON structure
    output_entry = {
        "text": combined_text,
        "entity": entity_spans
    }
    # Output
    json_content = json.dumps(output_entry, ensure_ascii=False, indent=2)
    return json_content

if __name__ == '__main__':
    # Create log directory if it doesn't exist
    log_dir = 'src/log/llm_label'
    os.makedirs(log_dir, exist_ok=True)

    # Set up logging
    current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = os.path.join(log_dir, f'llm_label_{current_time}.log')
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s',
                        handlers=[
                            logging.FileHandler(log_file),
                            logging.StreamHandler()
                        ])
    
    texts = []
    
    folder_path = "data/esg_filtered_report/" # filepath to the folder to be processed
    for filename in os.listdir(folder_path):
        print(filename)
        txt_filepath = os.path.join(folder_path, filename)
        with open(txt_filepath, "r", encoding="utf-8") as file:
            txt_content = file.read()
        for sentence in txt_content.split('\n'):
            if sentence != '':
                texts.append(sentence)
            
        ner_model = configure_ner_model()
    
        base_output_dir = 'data/esg_label_result'
        os.makedirs(base_output_dir, exist_ok=True)
        filename = filename.split(".")[0] + ".json"
        process_strings_with_annotations(strings=texts, output_dir=base_output_dir, file_name=filename, verbose=True, gemini_worker=2)
    