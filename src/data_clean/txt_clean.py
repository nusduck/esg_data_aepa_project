import re
import os
import pandas as pd
import json
import spacy

"""
    本脚本用于清洗Markdown文本，将表格转换为文本，移除Markdown格式，移除图片,小写化等内容。
Caution:
    1. 因为本脚本移除了部分特殊符号不确定是否会影响后续单位替换；
    2. 最后一行的文件保存路径需要自动根据output.md所属文件夹再命名！
    3. 文本各行前后有空格，需要进一步处理
"""

def convert_tables_in_markdown(markdown_content):
    """
    Convert Markdown tables to plain text format.
    """
    # 正则表达式匹配Markdown表格
    table_pattern = re.compile(r'((?:\|.*\|(?:\r?\n|\r)?)+)')
    
    def convert_table(match):
        table = match.group(0)
        # 分割行
        rows = [row.strip() for row in table.split('\n') if row.strip()]
        
        # 处理每一行
        processed_rows = []
        for row in rows:
            cells = [cell.strip() for cell in row.strip('|').split('|')]
            processed_rows.append(cells)
        
        # 确保所有行有相同的列数
        num_columns = len(processed_rows[0])
        processed_rows = [row for row in processed_rows if len(row) == num_columns]
        
        # 使用第一行作为表头
        header = processed_rows[0]
        data = processed_rows[1:]
        
        # 将表格转换为文本，并将每一列的表头加入到对应的单元格中
        table_text = []
        for row in data:
            row_text = []
            for i, cell in enumerate(row):
                row_text.append(f"{header[i]}: {cell}")
            table_text.append(", ".join(row_text))
        
        return "\n".join(table_text)
    
    # 替换所有表格
    converted_content = table_pattern.sub(convert_table, markdown_content)
    
    return converted_content


def remove_markdown_formatting(markdown_content):
    """
    Remove Markdown formatting from the content.
    """
    # 移除Markdown标题
    markdown_content = re.sub(r'#+ ', '', markdown_content)
    # 移除Markdown粗体和斜体
    markdown_content = re.sub(r'\*\*|__|\*|_', '', markdown_content)
    # 移除Markdown图片
    markdown_content = re.sub(r'!\[.*?\]\(.*?\)', '', markdown_content)
    # 移除Markdown图片
    markdown_content = re.sub(r'!\[.*?\] \(.*?\)', '', markdown_content)
    # 移除Markdown链接
    markdown_content = re.sub(r'\[.*?\]\(.*?\)', '', markdown_content)
    # 移除<br>标签 
    markdown_content = re.sub(r'<br>|<br', '', markdown_content)
    # 移除 • 
    markdown_content = re.sub(r'•', '', markdown_content)
    # 移除 - 连续出现超过3次的情况
    markdown_content = re.sub(r'---+', '', markdown_content)
    # 移除Markdown引用
    markdown_content = re.sub(r'> ', '', markdown_content)
    # 移除Markdown代码块
    markdown_content = re.sub(r'```.*?```', '', markdown_content, flags=re.DOTALL)
    # 移除行内代码
    markdown_content = re.sub(r'`.*?`', '', markdown_content)
    # 移除空白行
    markdown_content = re.sub(r'\n\s*\n', '\n', markdown_content)
    # 移除<sub>和<sup>标签
    markdown_content = re.sub(r'<sub>|</sub>|</sub|<sup>|</sup>|</sup', '', markdown_content)
    # 移除多余空格
    markdown_content = re.sub(r' +', ' ', markdown_content)
    # 小写化
    markdown_content = markdown_content.lower()
    # 移除首尾空格
    markdown_content = markdown_content.strip()

    return markdown_content


# 使用示例
# markdown_content = """
# **Steel**
# Emissions baseline and targets
# tCO₂/tonne
# | Year | Reduction target | 2021 baseline | MPP Tech Moratorium (global) |
# |---|---|---|---|
# | 2020 |  | 1.77 | 1.89 |
# | 2025 |  |  |  |
# | 2030 | -20% by 2030 |  | 1.42 |
# | 2035 |  |  |  |
# | 2040 |  |  |  |
# | 2045 |  |  |  |
# | 2050 | -92% by 2050 | 0.14 |  |
# **Oil and gas**
# No new project financing for upstream oil and gas projects approved for development after 2022
# ![example image](https://example.com/image.png)
# ```
# ```
# """

def unit_formatting(content, format_json):
    """
    content: str, 待处理的文本内容
    format_json: str, 单位格式化的json文件路径
    """
    with open(json_file, "r", encoding="utf-8") as file:
        loaded_dict = json.load(file)
    for unit, text in loaded_dict.items():
        content = re.sub(r'\b' + unit + r'\b', text, content)
    return content

def clean_markdown_text(md_text):
    # 移除特殊字符（#、*、-等）
    clean_text = re.sub(r'[#*`~>!\[\](){}]', '', md_text)
    # 移除空格和换行符
    clean_text = re.sub(r'\s+', ' ', clean_text).strip()
    return clean_text


def tokenize_text(text):
    nlp = spacy.load("en_core_web_sm")
    # 使用spaCy进行分词
    doc = nlp(text)
    tokens = [token.text for token in doc]
    return tokens


"""def split_text_into_sentences(text):
    # 使用正则表达式分割句子
    # 句子结束符包括 . ! ? 
    sentences = re.split(r'(?<=[.!?]) +', text)
    content = ''
    for sentence in sentences:
        content = content + sentence + '\n'
    return content"""

def split_text_into_sentences(text):
    # Split sentences with regular expressions, retaining sentence terminators
    # Sentence terminators include . ! ! 
    # Ensure that part such as "No. 1" are not splitted
    sentences = re.split(r'(?<=[.!?]) +(?=\D)', text)
    content = ''
    for sentence in sentences:
        content = content + sentence + '\n'
    return content



if __name__ == "__main__":
    
    json_file = '/data/unit_formatting_dict.json'
    folder_path = "/data/esg_parse_result/" # 待清洗的文件夹路径
    for filename in os.listdir(folder_path):
        print(filename)
        markdown_filepath = os.path.join(folder_path, f"{filename}/output.md")
        with open(markdown_filepath, "r", encoding="utf-8") as file:
            markdown_content = file.read()
            
        converted_content = convert_tables_in_markdown(markdown_content)
        converted_content = unit_formatting(converted_content, format_json=json_file)
        plain_text_content = remove_markdown_formatting(converted_content)
        plain_text_content = clean_markdown_text(plain_text_content)
        split_content = split_text_into_sentences(plain_text_content)
        
        
        processed_file_path = os.path.join('/data/esg_cleaned_report', f'{filename}.txt')
        os.makedirs(os.path.dirname(processed_file_path), exist_ok=True)
        with open(processed_file_path, "w", encoding="utf-8") as processed_file:
            processed_file.write(split_content)
            
            