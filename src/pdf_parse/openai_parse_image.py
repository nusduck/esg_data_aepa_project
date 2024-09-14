import openai
import base64
from io import BytesIO
from PIL import Image
import logging
import yaml

# Load configuration
with open('config/config.yaml', 'r') as config_file:
    config = yaml.safe_load(config_file)

# add a optional parameter index to log
def analyze_image(prompt, image_input, index=None):
    logging.info(f"openai parse page {index}")
    try:
        # Check if image_input is already a PIL Image object
        if isinstance(image_input, Image.Image):
            image = image_input
        else:
            # If it's a path, open the image
            image = Image.open(image_input)

        # Convert the image to base64
        buffered = BytesIO()
        image_format = image.format.lower() if image.format else 'jpeg'
        image.save(buffered, format=image_format)
        image_base64 = base64.b64encode(buffered.getvalue()).decode("utf-8")
        mime_type = f"image/{image_format}"

        openai_api_key = config['openai']['api_key']
        openai_base_url = config['openai']['base_url']
        client = openai.OpenAI(api_key=openai_api_key, base_url=openai_base_url)

        # Create the response
        response = client.chat.completions.create(
            model=config['openai']['model'],
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:{mime_type};base64,{image_base64}",
                            }
                        },
                    ],
                }
            ],
            max_tokens=4096,
        )
        result = response.choices[0].message.content
        logging.info(f"openai parse page {index} success")
        # Return the message content
        return result

    except Exception as e:
        logging.error(f"Openai parse page {index} an error occurred: {e}")
        return None

# Example usage
if __name__ == "__main__":
    prompt = """Convert the text recognized from the image into Markdown format. Follow these rules:

1. Output the text in the same language as recognized from the image. For example, if the text is in English, output in English.
2. Directly output the content without explanations or additional text. Do not include phrases like "Here is the Markdown text from the image."
3. Use $ $ for block formulas and inline formulas where applicable. Don not use ```markdown ``` or ``` ``` to wrap the content.
4. Ignore long straight lines and page numbers.
5. Convert charts (e.g., bar, line, pie) into Markdown tables when possible. If not possible, output all text from the charts as plain text.
"""
    image_path = "data/output/United Overseas Insurance Limited_report/62.png"
    result = analyze_image(prompt, image_path)
    print(result)