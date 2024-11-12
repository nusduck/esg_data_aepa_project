import json
import os
def save_json(results: dict, output_path: str, specific_report: str = None):
    """
    保存 JSON 数据，支持全量写入和增量写入
    
    Args:
        results: 要保存的字典数据
        output_path: 输出文件路径
        specific_report: 特定报告名称，为 None 时进行全量写入
    """
    # 确保输出目录存在
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    if specific_report is None:
        # 全量写入
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
    else:
        # 增量写入
        existing_data = {}
        if os.path.exists(output_path):
            with open(output_path, 'r', encoding='utf-8') as f:
                try:
                    existing_data = json.load(f)
                except json.JSONDecodeError:
                    existing_data = {}
        
        # 更新现有数据
        existing_data.update(results)
        
        # 写入合并后的数据
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(existing_data, f, ensure_ascii=False, indent=2)
if __name__ == '__main__':
    results = {
        'file7': {'question1': 'answer1'},
        'file8': {'question2': 'answer2'}
    }
    output_path = 'data/esg_retrieve/esg_retrieve_result.json'
    save_json(results, output_path)