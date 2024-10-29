import re
import json

with open("/Users/eddieho/Documents/NUS/DSS5105-PRJ/ESG/src/log/llm_retrieve/llm_parse_20241029_021213.log") as f:
    log_data = f.read()


# Regular expressions to extract question_id and response
question_id_pattern = re.compile(r'Retrieved data for (B-\w+)')
response_pattern = re.compile(r'\{[^}]+\}', re.DOTALL)

# Extracting data
question_ids = question_id_pattern.findall(log_data)
responses = response_pattern.findall(log_data)

# Converting to JSON format
output = {"file": []}

for question_id, response in zip(question_ids, responses):
    response_data = json.loads(response)
    output["file"].append({
        "question_id": question_id,
        "response": response_data
    })

# Print the formatted JSON
print(json.dumps(output, indent=4, ensure_ascii=False))
# save to /Users/eddieho/Documents/NUS/DSS5105-PRJ/ESG/data/esg_retrieve 
with open("/Users/eddieho/Documents/NUS/DSS5105-PRJ/ESG/data/esg_retrieve/results_20241029_021213.json", 'w') as f:
    json.dump(output, f, indent=4, ensure_ascii=False)
