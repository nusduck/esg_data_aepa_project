import re
"""
    本脚本用于清洗Markdown文本，将表格转换为文本，移除Markdown格式，移除图片,小写化等内容。
Caution:
    1. 因为本脚本移除了部分特殊符号不确定是否会影响后续单位替换；
    2. 最后一行的文件保存路径需要自动根据output.md所属文件夹再命名！
    3. 文本各行前后有空格，需要进一步处理
"""

def convert_tables_in_markdown(markdown_content):
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
# read markdown content from file data/output/United Overseas Bank Limited_report/output.md
with open("data/esg_parse_result/United Overseas Bank Limited_report/output.md", "r") as file:
    markdown_content = file.read()

# 转换表格
converted_content = convert_tables_in_markdown(markdown_content)
# 移除图片
# no_images_content = remove_images_from_markdown(converted_content)
# 移除Markdown格式
plain_text_content = remove_markdown_formatting(converted_content)

print(plain_text_content)
# 保存文件到 data/esg_cleaned_data/United_Overseas_Bank_Limited_report.txt 
# 名字保存需要自动获取所属文件夹后再命名保存到-> data/esg_cleaned_data/ 文件夹下！
with open("data/esg_cleaned_data/United_Overseas_Bank_Limited_report.txt", "w") as file:
    file.write(plain_text_content)