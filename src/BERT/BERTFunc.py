import pandas as pd
import numpy as np
from transformers import BertTokenizerFast, BertForTokenClassification, Trainer, TrainingArguments
from datasets import Dataset
import torch
import os
import glob
import json
import random
from sklearn.metrics import accuracy_score, precision_recall_fscore_support
from sklearn.utils import resample
import matplotlib.pyplot as plt

label_dict ={
        "B-ENV_GHG_AET": 0,
        "I-ENV_GHG_AET": 0,
        "B-ENV_GHG_AE1": 0,
        "I-ENV_GHG_AE1": 0,
        "B-ENV_GHG_AE2": 0,
        "I-ENV_GHG_AE2": 0,
        "B-ENV_GHG_AE3": 0,
        "I-ENV_GHG_AE3": 0,
        "B-ENV_GHG_EIT": 0,
        "I-ENV_GHG_EIT": 0,
        "B-ENV_GHG_EI1": 0,
        "I-ENV_GHG_EI1": 0,
        "B-ENV_GHG_EI2": 0,
        "I-ENV_GHG_EI2": 0,
        "B-ENV_GHG_EI3": 0,
        "I-ENV_GHG_EI3": 0,
        "B-ENV_ENC_TEC": 0,
        "I-ENV_ENC_TEC": 0,
        "B-ENV_ENC_ECI": 0,
        "I-ENV_ENC_ECI": 0,
        "B-ENV_WAC_TWC": 0,
        "I-ENV_WAC_TWC": 0,
        "B-ENV_WAC_WCI": 0,
        "I-ENV_WAC_WCI": 0,
        "B-ENV_WAG_TWG": 0,
        "I-ENV_WAG_TWG": 0,
        "B-SOC_GED_CEG_M": 0,
        "I-SOC_GED_CEG_M": 0,
        "B-SOC_GED_CEG_F": 0,
        "I-SOC_GED_CEG_F": 0,
        "B-SOC_GED_NHG_M": 0,
        "I-SOC_GED_NHG_M": 0,
        "B-SOC_GED_NHG_F": 0,
        "I-SOC_GED_NHG_F": 0,
        "B-SOC_GED_ETG_M": 0,
        "I-SOC_GED_ETG_M": 0,
        "B-SOC_GED_ETG_F": 0,
        "I-SOC_GED_ETG_F": 0,
        "B-SOC_AGD_CEA_U30": 0,
        "I-SOC_AGD_CEA_U30": 0,
        "B-SOC_AGD_CEA_B35": 0,
        "I-SOC_AGD_CEA_B35": 0,
        "B-SOC_AGD_CEA_A50": 0,
        "I-SOC_AGD_CEA_A50": 0,
        "B-SOC_AGD_NHI_U30": 0,
        "I-SOC_AGD_NHI_U30": 0,
        "B-SOC_AGD_NHI_B35": 0,
        "I-SOC_AGD_NHI_B35": 0,
        "B-SOC_AGD_NHI_A50": 0,
        "I-SOC_AGD_NHI_A50": 0,
        "B-SOC_AGD_TOR_U30": 0,
        "I-SOC_AGD_TOR_U30": 0,
        "B-SOC_AGD_TOR_B35": 0,
        "I-SOC_AGD_TOR_B35": 0,
        "B-SOC_AGD_TOR_A50": 0,
        "I-SOC_AGD_TOR_A50": 0,
        "B-SOC_DEV_ATH_M": 0,
        "I-SOC_DEV_ATH_M": 0,
        "B-SOC_DEV_ATH_F": 0,
        "I-SOC_DEV_ATH_F": 0,
        "B-SOC_OHS_FAT": 0,
        "I-SOC_OHS_FAT": 0,
        "B-SOC_OHS_HCI": 0,
        "I-SOC_OHS_HCI": 0,
        "B-SOC_OHS_REC": 0,
        "I-SOC_OHS_REC": 0,
        "B-SOC_OHS_RWI": 0,
        "I-SOC_OHS_RWI": 0,
        "B-GOV_BOC_BIN": 0,
        "I-GOV_BOC_BIN": 0,
        "B-GOV_BOC_WOB": 0,
        "I-GOV_BOC_WOB": 0,
        "B-GOV_MAD_WMT": 0,
        "I-GOV_MAD_WMT": 0,
        "B-GOV_ETB_ACD": 0,
        "I-GOV_ETB_ACD": 0,
        "B-GOV_ETB_ACT_N": 0,
        "I-GOV_ETB_ACT_N": 0,
        "B-GOV_ETB_ACT_P": 0,
        "I-GOV_ETB_ACT_P": 0,
        "B-GOV_CER_LRC": 0,
        "I-GOV_CER_LRC": 0,
        "B-GOV_ALF_AFD": 0,
        "I-GOV_ALF_AFD": 0,
        "B-GOV_ASS_ASR": 0,
        "I-GOV_ASS_ASR": 0,
        "B-VALUE": 0,
        "I-VALUE": 0,
        "B-UNIT": 0,
        "I-UNIT": 0,
        "O": 0
    }


def read_json_folder(folder_path):
    # 使用glob获取文件夹中所有的JSON文件
    json_files = glob.glob(os.path.join(folder_path, "*.json"))

    all_data = []

    # 逐个读取每个JSON文件
    for file in json_files:
        with open(file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            all_data.extend(data)  # 将所有JSON文件的数据合并到一个列表中
    return all_data

def clean_errordata(all_data):
    data = [item for item in all_data if "error" not in item]
    return data

def BIO_data_extract(all_data):
    data = clean_errordata(all_data)
    
    # 提取BIO标注数据
    texts = []
    labels = []
    # err = []

    for entry in data:
        text = entry['text']
        entity_labels = ["O"] * len(text)  # 初始化为'O'

        for entity in entry['entity']:
            start, end, label = entity['start'], entity['end'], entity['labels'][0]
            if label not in label_dict:
                continue
            # 检查字典情况
            # if end > len(entity_labels):
            #     err.append(data.index(entry))
            #     continue
            for i in range(start, end):
                entity_labels[i] = label

        texts.append(list(text))
        labels.append(entity_labels)

    # 将数据转换为 DataFrame 格式
    df = pd.DataFrame({"tokens": texts, "ner_tags": labels})
    return df

def no_entity_data_filter(df):
    # 非实体句清除

    no_entity_data = df[df['ner_tags'].apply(lambda x: all(label == "O" for label in x))]
    entity_data = df[~df['ner_tags'].apply(lambda x: all(label == "O" for label in x))]

    # 保留 15% 的无实体句子
    no_entity_sample = no_entity_data.sample(frac=0.15, random_state=42)

    # 合并数据
    balanced_df = pd.concat([entity_data, no_entity_sample])

    # 打乱数据集顺序
    balanced_df = balanced_df.sample(frac=1, random_state=42).reset_index(drop=True)

    # 检查新的数据分布
    print("无实体句子数量:", len(no_entity_sample))
    print("实体句子数量:", len(entity_data))
    print("合并后的数据集样本数:", len(balanced_df))
    return balanced_df

# 定义需要合并的标签字典，将稀有标签映射到新的标签名
merge_dict = {
    "B-SOC_AGD_TOR_U30": "B-SOC_AGD_TOR",
    "I-SOC_AGD_TOR_U30": "I-SOC_AGD_TOR",
    "B-SOC_AGD_TOR_B35": "B-SOC_AGD_TOR",
    "I-SOC_AGD_TOR_B35": "I-SOC_AGD_TOR",
    "B-SOC_AGD_TOR_A50": "B-SOC_AGD_TOR",
    "I-SOC_AGD_TOR_A50": "I-SOC_AGD_TOR",
    
    'B-SOC_AGD_NHI_B35': 'B-SOC_AGD_NHI',
    'B-SOC_AGD_NHI_A50': 'B-SOC_AGD_NHI',
    'B-SOC_AGD_NHI_U30': 'B-SOC_AGD_NHI',
    'I-SOC_AGD_NHI_U30': 'I-SOC_AGD_NHI',
    'I-SOC_AGD_NHI_B35': 'I-SOC_AGD_NHI',
    'I-SOC_AGD_NHI_A50': 'I-SOC_AGD_NHI',
    
    'B-ENV_GHG_EI1' : 'B-ENV_GHG_EI',
    'I-ENV_GHG_EI1' : 'I-ENV_GHG_EI',
    'B-ENV_GHG_EI2' : 'B-ENV_GHG_EI',
    'I-ENV_GHG_EI2' : 'I-ENV_GHG_EI',
    'B-ENV_GHG_EI3' : 'B-ENV_GHG_EI',
    'I-ENV_GHG_EI3' : 'I-ENV_GHG_EI',
    
    'B-SOC_AGD_CEA_U30' : 'B-SOC_AGD_CEA',
    'I-SOC_AGD_CEA_U30' : 'I-SOC_AGD_CEA',
    'B-SOC_AGD_CEA_B35' : 'B-SOC_AGD_CEA',
    'I-SOC_AGD_CEA_B35' : 'I-SOC_AGD_CEA',
    'B-SOC_AGD_CEA_A50' : 'B-SOC_AGD_CEA',
    'I-SOC_AGD_CEA_A50' : 'I-SOC_AGD_CEA',
    
    'B-SOC_GED_ETG_F' : 'B-SOC_GED_ETG',
    'I-SOC_GED_ETG_F' : 'I-SOC_GED_ETG',
    'B-SOC_GED_ETG_M' : 'B-SOC_GED_ETG',
    'I-SOC_GED_ETG_M' : 'I-SOC_GED_ETG',
    'B-SOC_GED_NHG_M' : 'B-SOC_GED_NHG',
    'I-SOC_GED_NHG_M' : 'I-SOC_GED_NHG',
    'B-SOC_GED_NHG_F' : 'B-SOC_GED_NHG',
    'I-SOC_GED_NHG_F' : 'I-SOC_GED_NHG'
    
    # 添加更多需要合并的标签映射
}

# 定义一个函数，用于将标签序列中的稀有标签合并
def merge_labels(label_sequence, merge_dict):
    return [merge_dict.get(label, label) for label in label_sequence]

def rare_label_merge(balanced_df):
    # 应用标签合并函数到 DataFrame 的 'labels' 列
    balanced_df['ner_tags'] = balanced_df['ner_tags'].apply(lambda x: merge_labels(x, merge_dict))
    return balanced_df

def show_label(balanced_df):
    # 设置 pandas 的显示选项，防止省略
    pd.set_option('display.max_rows', None)

    # 检查标签合并后的分布
    all_labels_flat = [item for sublist in balanced_df['ner_tags'] for item in sublist]
    label_counts_after_merge = pd.Series(all_labels_flat).value_counts()

    print("合并后的标签分布:")
    print(label_counts_after_merge)

    # 恢复默认设置
    pd.reset_option('display.max_rows')
    
def over_sampling(balanced_df,low_count_threshold = 450,nsamples = 50):
    # 定义低频标签的阈值 low_count_threshold

    # 获取所有标签的数量分布
    all_labels_flat = [item for sublist in balanced_df['ner_tags'] for item in sublist]
    label_counts = pd.Series(all_labels_flat).value_counts()  # 假设这是一个标签-数量的字典或 Series

    # 找出所有低频标签
    low_frequency_labels = [label for label, count in label_counts.items() if count < low_count_threshold]

    # 初始化一个新的 DataFrame 来存储过采样的句子
    balanced_df_resampled = balanced_df.copy()

    # 遍历每一个低频标签，筛选并过采样包含该标签的句子
    for label in low_frequency_labels:
        # 筛选出包含当前标签的句子
        sentences_with_label = balanced_df[balanced_df['ner_tags'].apply(lambda x: label in x)]
        
        # 确认是否需要过采样
        if len(sentences_with_label) < low_count_threshold:
            # 过采样该标签的句子
            sentences_with_label_upsampled = resample(sentences_with_label, 
                                                    replace=True, 
                                                    n_samples=nsamples, 
                                                    random_state=42)
            
            # 将过采样后的数据合并到主数据集中
            balanced_df_resampled = pd.concat([balanced_df_resampled, sentences_with_label_upsampled])

    # 打乱数据集
    balanced_df_resampled = balanced_df_resampled.sample(frac=1, random_state=42).reset_index(drop=True)

    # 查看结果
    print("过采样后的数据集大小:", len(balanced_df_resampled))
    return balanced_df_resampled


def identity_labels(balanced_df_resampled):
    all_labels_flat = [item for sublist in balanced_df_resampled['ner_tags'] for item in sublist]
    label_counts_after_merge = pd.Series(all_labels_flat).value_counts()
    # 使用集合存储所有独特标签，避免重复
    unique_labels = set(label_counts_after_merge.index)

    # 将集合转换为列表并排序
    unique_labels = sorted(list(unique_labels))

    # 查看所有标签
    print("所有独特标签:", unique_labels)
    print(len(unique_labels))
    return unique_labels



def data_transform(balanced_df_resampled,testsize = 0.2):
    # 将数据转换为 Hugging Face 的 Dataset 格式
    dataset = Dataset.from_pandas(balanced_df_resampled)
    train_test_split = dataset.train_test_split(test_size=testsize)
    train_dataset = train_test_split['train']
    eval_dataset = train_test_split['test']
    return train_dataset,eval_dataset

def tokenize_and_align_labels(examples,tokenizer = tokenizer):
    tokenized_inputs = tokenizer(
        examples["tokens"], 
        truncation=True, 
        is_split_into_words=True, 
        padding=True
    )
    labels = []

    for i, label in enumerate(examples["ner_tags"]):
        word_ids = tokenized_inputs.word_ids(batch_index=i)
        previous_word_idx = None
        label_ids = []

        for word_idx in word_ids:
            if word_idx is None:
                label_ids.append(-100)  # 忽略位置
            elif word_idx != previous_word_idx:
                label_ids.append(label2id[label[word_idx]])  # 将标签转换为整数 ID
            else:
                # 对于当前词的子词部分，通常不需要计算损失，除非你想保持每个子词的相同标签
                label_ids.append(label2id[label[word_idx]] if label[word_idx].startswith("I-") else -100)
            previous_word_idx = word_idx

        labels.append(label_ids)

    tokenized_inputs["labels"] = labels
    return tokenized_inputs

# Define compute_metrics function for evaluation
def compute_metrics(pred):
    # Extract predictions and labels
    predictions, labels = pred
    predictions = np.argmax(predictions, axis=2)
    
    # Remove ignored index (special tokens)
    true_labels = [[label for label, pred in zip(label_row, pred_row) if label != -100] 
                   for label_row, pred_row in zip(labels, predictions)]
    true_predictions = [[pred for label, pred in zip(label_row, pred_row) if label != -100]
                        for label_row, pred_row in zip(labels, predictions)]
    
    # Flatten lists
    true_labels = [item for sublist in true_labels for item in sublist]
    true_predictions = [item for sublist in true_predictions for item in sublist]
    
    # Calculate metrics
    accuracy = accuracy_score(true_labels, true_predictions)
    precision, recall, f1, _ = precision_recall_fscore_support(true_labels, true_predictions, average='weighted')
    
    # Return results in dictionary
    return {
        'accuracy': accuracy,
        'precision': precision,
        'recall': recall,
        'f1': f1,
    }


train_dataset = train_dataset.map(tokenize_and_align_labels, batched=True)
eval_dataset = eval_dataset.map(tokenize_and_align_labels, batched=True)