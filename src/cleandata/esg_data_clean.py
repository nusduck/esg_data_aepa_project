import re
import os
import json
import logging
from typing import List, Dict, Optional
import spacy
from pathlib import Path

class TextProcessor:
    def __init__(self, unit_mapping_path: str, spacy_model: str = "en_core_web_sm"):
        self.unit_mappings = self._load_unit_mappings(unit_mapping_path)
        try:
            self.nlp = spacy.load(spacy_model)
        except OSError:
            logging.error(f"Failed to load spaCy model: {spacy_model}")
            raise
        
        # 定义常见缩写列表
        self.common_abbreviations = {
            'mr.', 'mrs.', 'ms.', 'dr.', 'prof.', 'sr.', 'jr.',
            'i.e.', 'e.g.', 'etc.', 'vs.', 'viz.',
            'a.m.', 'p.m.',
            'jan.', 'feb.', 'mar.', 'apr.', 'jun.', 'jul.',
            'aug.', 'sep.', 'oct.', 'nov.', 'dec.'
        }
        
        self.markdown_patterns = {
            'headers': re.compile(r'#+ '),
            'emphasis': re.compile(r'\*\*|__|\*|_'),
            'images': re.compile(r'!\[.*?\][\s]*\(.*?\)'),
            'links': re.compile(r'\[.*?\]\(.*?\)'),
            'html_tags': re.compile(r'<br>|<br/>|<sub>|</sub>|<sup>|</sup>'),
            'bullets': re.compile(r'•'),
            'horizontal_rules': re.compile(r'---+'),
            'blockquotes': re.compile(r'> '),
            'code_blocks': re.compile(r'```.*?```', re.DOTALL),
            'inline_code': re.compile(r'`.*?`'),
            'empty_lines': re.compile(r'\n\s*\n'),
            'extra_spaces': re.compile(r'\s{2,}')
        }

    def _load_unit_mappings(self, filepath: str) -> Dict[str, str]:
        try:
            with open(filepath, "r", encoding="utf-8") as file:
                mappings = json.load(file)
            return dict(sorted(mappings.items(), key=lambda x: len(x[0]), reverse=True))
        except (json.JSONDecodeError, FileNotFoundError) as e:
            logging.error(f"Failed to load unit mappings: {e}")
            raise

    def convert_tables(self, content: str) -> str:
        lines = content.split('\n')
        processed_lines = []
        i = 0
        
        while i < len(lines):
            line = lines[i]
            
            if '|' in line and i > 0:
                table_prefix = lines[i-1].strip() if 'Table' in lines[i-1] else ''
                table_lines = []
                
                while i < len(lines) and '|' in lines[i]:
                    table_lines.append(lines[i])
                    i += 1
                
                if table_lines:
                    processed_lines.append(self._process_table(table_lines, table_prefix))
                continue
            
            processed_lines.append(line)
            i += 1
        
        return '\n'.join(processed_lines)

    def _process_table(self, table_lines: List[str], table_prefix: str) -> str:
        rows = [row.strip() for row in table_lines if row.strip()]
        if not rows:
            return ""
        
        header = [cell.strip() for cell in rows[0].strip('|').split('|')]
        data_rows = rows[2:] if len(rows) > 2 else rows[1:]
        
        formatted_rows = []
        for row in data_rows:
            cells = [cell.strip() for cell in row.strip('|').split('|')]
            if len(cells) != len(header):
                continue
            
            row_pairs = [
                f"{header[j]}: {cell}" 
                for j, cell in enumerate(cells) 
                if cell.strip()
            ]
            
            if row_pairs:
                text = ", ".join(row_pairs)
                if table_prefix:
                    text = f"{table_prefix}, {text}"
                formatted_rows.append(text)
            # Ensure the last row ends with a period
        if formatted_rows and not formatted_rows[-1].endswith('.'):
            formatted_rows[-1] += ' table_end.'
        return "\n".join(formatted_rows)

    def remove_markdown_formatting(self, content: str) -> str:
        for pattern in self.markdown_patterns.values():
            content = pattern.sub(' ', content)
        return content.lower().strip()

    def apply_unit_formatting(self, content: str) -> str:
        for unit, replacement in self.unit_mappings.items():
            content = re.sub(r'\b' + re.escape(unit) + r'\b', replacement, content)
        return content

    def clean_text(self, content: str) -> str:
        content = re.sub(r'[#*`~>!\[\](){}]', ' ', content)
        content = re.sub(r'\s{2,}', ' ', content)
        return content.strip()

    def split_into_sentences(self, content: str) -> str:
        """
        改进的句子切分逻辑，避免在缩写和序号处错误断句。
        """
        # 预处理：将内容转换为小写以便比较
        content = content.replace('\n', ' ')  # 将换行符转换为空格
        
        # 初步按句号分割
        rough_sentences = []
        current_sentence = []
        words = content.split()
        
        for i, word in enumerate(words):
            current_sentence.append(word)
            
            # 检查当前词是否以句号、感叹号或问号结尾
            if word.endswith(('.', '!', '?')):
                # 检查是否是缩写或序号
                word_lower = word.lower()
                is_abbreviation = (
                    word_lower in self.common_abbreviations or  # 检查常见缩写
                    (len(word) <= 2 and word.endswith('.')) or  # 单字母缩写
                    bool(re.match(r'\d+\.', word)) or          # 数字序号
                    bool(re.match(r'[a-z]\.', word_lower))     # 字母序号
                )
                
                # 如果不是缩写，或者是句子的最后一个词，则结束当前句子
                if not is_abbreviation or i == len(words) - 1:
                    rough_sentences.append(' '.join(current_sentence))
                    current_sentence = []
        
        # 如果还有未处理的词，将它们添加为最后一个句子
        if current_sentence:
            rough_sentences.append(' '.join(current_sentence))
        
        # 清理并过滤空句子
        sentences = [s.strip() for s in rough_sentences if s.strip()]
        
        return '\n'.join(sentences)

    def process_file(self, input_path: str, output_path: str) -> None:
        try:
            with open(input_path, "r", encoding="utf-8") as file:
                content = file.read()
            
            content = self.convert_tables(content)
            content = self.apply_unit_formatting(content)
            content = self.remove_markdown_formatting(content)
            content = self.clean_text(content)
            content = self.split_into_sentences(content)
            
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            with open(output_path, "w", encoding="utf-8") as file:
                file.write(content)
                
        except Exception as e:
            logging.error(f"Error processing file {input_path}: {e}")
            raise

def main():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    
    CONFIG = {
        'unit_mapping_file': 'data/esg_unit_mapping/unit_formatting_dict.json',
        'input_folder': "data/esg_parse_result/",
        'output_folder': "data/esg_cleaned_report/",
    }
    
    try:
        processor = TextProcessor(CONFIG['unit_mapping_file'])
        
        for filename in os.listdir(CONFIG['input_folder']):
            logging.info(f"Processing {filename}")
            
            input_path = os.path.join(CONFIG['input_folder'], f"{filename}/output.md")
            output_path = os.path.join(CONFIG['output_folder'], f'{filename}.txt')
            
            if os.path.exists(input_path):
                processor.process_file(input_path, output_path)
                logging.info(f"Successfully processed {filename}")
            else:
                logging.warning(f"Input file not found: {input_path}")
                
    except Exception as e:
        logging.error(f"Processing failed: {e}")
        raise

if __name__ == "__main__":
    main()