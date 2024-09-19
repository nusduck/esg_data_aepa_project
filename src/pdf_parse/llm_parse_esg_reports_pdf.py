import os
import time
from typing import List, Tuple, Optional, Dict
import logging
import cv2
import fitz
import numpy as np
from PIL import Image
import concurrent.futures
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
from openai_parse_image import analyze_image
from rapid_layout import RapidLayout, VisLayout
import yaml
from datetime import datetime

# Create log directory if it doesn't exist
log_dir = 'src/log/llm_parse'
os.makedirs(log_dir, exist_ok=True)

# Set up logging
current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
log_file = os.path.join(log_dir, f'llm_parse_{current_time}.log')
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[
                        logging.FileHandler(log_file),
                        logging.StreamHandler()
                    ])

# Load configuration
with open('config/config.yaml', 'r') as config_file:
    config = yaml.safe_load(config_file)

# Use configuration values
base_output_dir = 'data/esg_parse_result'
os.makedirs(base_output_dir, exist_ok=True)

layout_engine = RapidLayout(conf_thres=0.5, model_type="pp_layout_cdla")

# Initialize Gemini-Flash model
api_keys = config['google']['api_keys']

current_api_key_index = 0
safety_settings = {
    HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
}
def configure_model():
    global current_api_key_index
    genai.configure(api_key=api_keys[current_api_key_index])
    return genai.GenerativeModel(config['google']['model'], safety_settings=safety_settings, system_instruction="You are ChatGPT, a large language model trained by OpenAI")

model = configure_model()

# This Default Prompt Using Chinese and could be changed to other languages.
DEFAULT_PROMPT = """Convert the text recognized from the image into Markdown format. Follow these rules:

1. Output the text in the same language as recognized from the image. For example, if the text is in English, output in English.
2. Directly output the content without explanations or additional text. Do not include phrases like "Here is the Markdown text from the image."
3. Use $ $ for block formulas and inline formulas where applicable. Don not use ```markdown ``` or ``` ``` to wrap the content.
4. Ignore long straight lines and page numbers.
5. Convert charts (e.g., bar, line, pie) into Markdown tables when possible. If not possible, output all text from the charts as plain text.
"""
DEFAULT_RECT_PROMPT = """In the image, some areas are marked with red rectangles and names (%s). If the area is a table or image, directly output the markdown format table or text content.
"""
DEFAULT_ROLE_PROMPT = """You are a PDF document parser, outputting the content of images using Markdown and LaTeX syntax.
"""
def draw_boxes_only(image, boxes):
    img = image.copy()
    for box in boxes:
        x1, y1, x2, y2 = map(int, box)
        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 0, 255), 4)
    return img

def _parse_pdf_to_images(pdf_path: str, output_dir: str = './output') -> List[Tuple[str, List[str]]]:
    image_infos = []
    pdf_document = fitz.open(pdf_path)
    for page_index, page in enumerate(pdf_document):
        rect_images = []
        logging.info(f'parse page: {page_index}')
        # 保存页面为图片
        pix = page.get_pixmap(matrix=fitz.Matrix(4, 4))
        pix = Image.frombytes('RGB', [pix.width, pix.height], pix.samples)
        boxes, scores, class_names, elapse = layout_engine(pix)
        for index, (class_name, box) in enumerate(zip(class_names, boxes)):
            if class_name == 'figure' or class_name == 'table':
                name = f'{page_index}_{index}.png'
                sub_pix = pix.crop(box)
                sub_pix.save(os.path.join(output_dir, name))
                rect_images.append(name)

        boxes_ = []
        scores_ = []
        class_names_ = []
        for i, (class_name, box, score) in enumerate(zip(class_names, boxes, scores)):
            if class_name == 'figure' or class_name == 'table':
                boxes_.append(box)
                scores_.append(score)
                class_name = f'{page_index}_{i}.png'
                class_names_.append(class_name)
                
        page_image = os.path.join(output_dir, f'{page_index}.png')
        pix = np.array(pix)
        pix = cv2.cvtColor(pix, cv2.COLOR_RGB2BGR)
        # print(boxes_, scores_, class_names_)
        # ploted_img = VisLayout.draw_detections(pix, boxes_, scores_, class_names_)
        ploted_img = draw_boxes_only(pix, boxes_)
        if ploted_img is not None:
            cv2.imwrite(page_image, ploted_img)
        # ploted_img.save(page_image)
        image_infos.append((page_image, rect_images))
    pdf_document.close()
    return image_infos

def _gemini_parse_images(
        image_infos: List[Tuple[str, List[str]]],
        prompt_dict: Optional[Dict] = None,
        output_dir: str = './',
        verbose: bool = False,
        gemini_worker: int = 1,
        **args
) -> str:
    """
    Parse images to markdown content using Gemini-Flash.
    """
    if isinstance(prompt_dict, dict) and 'prompt' in prompt_dict:
        prompt = prompt_dict['prompt']
        logging.info("prompt is provided, using user prompt.")
    else:
        prompt = DEFAULT_PROMPT
        logging.info("prompt is not provided, using default prompt.")
    if isinstance(prompt_dict, dict) and 'rect_prompt' in prompt_dict:
        rect_prompt = prompt_dict['rect_prompt']
        logging.info("rect_prompt is provided, using user prompt.")
    else:
        rect_prompt = DEFAULT_RECT_PROMPT
        logging.info("rect_prompt is not provided, using default prompt.")
    if isinstance(prompt_dict, dict) and 'role_prompt' in prompt_dict:
        role_prompt = prompt_dict['role_prompt']
        logging.info("role_prompt is provided, using user prompt.")
    else:
        role_prompt = DEFAULT_ROLE_PROMPT
        logging.info("role_prompt is not provided, using default prompt.")

    def _process_page(index: int, image_info: Tuple[str, List[str]]) -> Tuple[int, str]:
        global model, current_api_key_index
        logging.info(f'gemini parse page: {index}')

        page_image, rect_images = image_info
        local_prompt = role_prompt + prompt
        if rect_images:
            local_prompt += rect_prompt % ', '.join(rect_images)

        image = Image.open(page_image)

        try:
            response = model.generate_content([local_prompt, image])
            
            # 只打印状信息
            logging.info(f"Generated content for page {index}")
            
            if not response.candidates or not response.candidates[0].content:
                reason = "blocked" if not response.candidates else "empty"
                logging.warning(f"Response for page {index} was {reason}. "
                                f"Reason: {response.candidates[0].finish_reason}")
                try:
                    content = analyze_image(local_prompt, image, index)
                except Exception as e:
                    logging.error(f"Error analyzing image for page {index}: {str(e)}")
                    return index, f"[Content for page {index} was not generated due to {reason} response.]"
            else:
                content = response.candidates[0].content.parts[0].text

            if not content:
                logging.warning(f"No text generated for page {index}.")
                return index, f"[No content was generated for page {index}.]"

            if '```markdown' in content:
                content = content.replace('```markdown\n', '')
                last_backticks_pos = content.rfind('```')
                if last_backticks_pos != -1:
                    content = content[:last_backticks_pos] + content[last_backticks_pos + 3:]

            return index, content

        except Exception as e:
            if '429' in str(e):
                logging.error(f"Error 429: Too Many Requests for API key {api_keys[current_api_key_index]}. Switching API key.")
                current_api_key_index = (current_api_key_index + 1) % len(api_keys)
                model = configure_model()
            else:
                logging.error(f"Error processing page {index}: {str(e)}. Switching API key.")
                current_api_key_index = (current_api_key_index + 1) % len(api_keys)
                model = configure_model()
            time.sleep(5)  # Sleep for 5 seconds before retrying
            return _process_page(index, image_info)  # Retry

    contents = [None] * len(image_infos)
    with concurrent.futures.ThreadPoolExecutor(max_workers=gemini_worker) as executor:
        futures = [executor.submit(_process_page, index, image_info) for index, image_info in enumerate(image_infos)]
        for future in concurrent.futures.as_completed(futures):
            index, content = future.result()
            print(content) if not verbose else None
            contents[index] = content

    output_path = os.path.join(output_dir, 'output.md')
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n\n'.join(contents))

    return '\n\n'.join(contents)

def parse_pdf(
        pdf_path: str,
        output_dir: str,
        prompt: Optional[Dict] = None,
        verbose: bool = False,
        gemini_worker: int = 1,
        **args
) -> Tuple[str, List[str]]:
    """
    Parse a PDF file to a markdown file using Gemini-Flash.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    image_infos = _parse_pdf_to_images(pdf_path, output_dir=output_dir)
    print(image_infos) if not verbose else None
    content = _gemini_parse_images(
        image_infos=image_infos,
        output_dir=output_dir,
        prompt_dict=prompt,
        verbose=verbose,
        gemini_worker=gemini_worker,
        **args
    )

    all_rect_images = []
    if not verbose:
        for page_image, rect_images in image_infos:
            if os.path.exists(page_image):
                os.remove(page_image)
            all_rect_images.extend(rect_images)
    return content, all_rect_images

def process_all_pdfs(pdf_dir: str, base_output_dir: str, verbose: bool = False, gemini_worker: int = 1):
    for filename in os.listdir(pdf_dir):
        if filename.endswith('.pdf'):
            pdf_path = os.path.join(pdf_dir, filename)
            report_name = os.path.splitext(filename)[0]
            output_dir = os.path.join(base_output_dir, report_name)
            
            logging.info(f"Processing {filename}")
            result = parse_pdf(
                pdf_path=pdf_path,
                output_dir=output_dir,
                verbose=verbose,
                gemini_worker=gemini_worker
            )
            logging.info(f"Finished processing {filename}")

if __name__ == "__main__":
    pdf_dir = 'data/esg_reports_pdf'
    process_all_pdfs(pdf_dir, base_output_dir, verbose=True, gemini_worker=1)