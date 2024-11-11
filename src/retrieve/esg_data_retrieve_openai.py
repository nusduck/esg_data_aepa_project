import os
import time
from datetime import datetime
import logging
import yaml
import pandas as pd
from openai import OpenAI
import json

# Create log directory if it doesn't exist
log_dir = 'src/log/llm_retrieve'
os.makedirs(log_dir, exist_ok=True)

# Set up logging
current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
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
with open('config/config.yaml', 'r') as config_file:
    config = yaml.safe_load(config_file)

def configure_client():
    """Initialize OpenAI client with API key"""
    return OpenAI(api_key=config['deepseek']['api_key'],base_url=config['deepseek']['base_url'])

# Initialize OpenAI client
client = configure_client()

# JSON schema for response structure
response_schema = {
    "type": "object",
    "properties": {
        "value": {"type": "string"},
        "unit": {"type": "string"},
        "from_sentences": {"type": "string"}
    },
    "required": ["value", "unit", "from_sentences"]
}

def read_txt_files():
    """Read all txt files from data/esg_cleaned_data folder"""
    data_folder = 'data/esg_cleaned_data'
    files = os.listdir(data_folder)
    data = []
    for file in files:
        with open(os.path.join(data_folder, file), 'rb') as f:
            data.append(f.read())
    return data

def read_excel_file():
    """Read the excel file containing retrieval questions"""
    data_folder = 'data/esg_retrieve'
    data = pd.read_excel(os.path.join(data_folder, 'retrieve_questions.xlsx'))
    return data


def retrieve_esg_data(file_content):
    """Create a chat session and return it"""
    try:
        # Convert binary content to string
        file_text = file_content.decode('utf-8')
        
        # Create initial system message
        messages = [
            {
                "role": "system",
                "content": """
                You are a data scientist specializing in ESG data. You are tasked with retrieving ESG data for a given company.
                The ESG data is contained in the following report. Please read the report and answer the questions based on the information provided.
                
                EXAMPLE JSON OUTPUT:
                {
                    "from_sentences": "our energy consumption across the region reduced by 2.3 per cent as compared with 2018, totalling 135.3 gigawatt-hours",
                    "unit": "gigawatt-hours",
                    "value": "135.3"
                }
                
                """

            },
            {
                "role": "user",
                "content": f"{file_text}\n\nPlease read this report carefully and prepare to answer the following questions about it."
            }
        ]
        
        
        # Return both the messages history and the initial response
        return {'messages': messages}
        
    except Exception as e:
        logging.error(f'Error in creating chat session: {str(e)}')
        return None

def send_message(chat_session, question):
    """Send a message in the chat session and get response"""
    try:
        # Add the new question to the message history
        chat_session['messages'].append({
            "role": "user",
            "content": f"{question}"
        })
        # logging.info(chat_session)
        # Get completion with the updated message history
        response = client.chat.completions.create(
            model=config['deepseek']['model'],
            messages=chat_session['messages'],
            response_format={
                'type': 'json_object'
            },
            temperature=1.0
        )
        
        chat_session["messages"].pop()
        
        return response.choices[0].message.content
        
    except Exception as e:
        logging.error(f'Error in sending message: {str(e)}')
        return None

if __name__ == '__main__':
    data = read_txt_files()
    questions = read_excel_file()
    
    for i in range(len(data)):
        chat_session = retrieve_esg_data(data[i])
        if chat_session:
            for j in range(len(questions)):
                response = send_message(chat_session, questions.iloc[j, 1])
                if response:
                    logging.info(f'Retrieved data for {questions.iloc[j, 0]}')
                    logging.info(response)
                else:
                    logging.error(f'Error in retrieving data for {questions.iloc[j, 0]}')