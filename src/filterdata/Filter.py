import seaborn as sns
from transformers import BertTokenizer, BertForSequenceClassification, pipeline
import os
import torch

def get_result_path(input_file_path):
    # 获取输入文件的目录、文件名和扩展名
    file_dir, file_name = os.path.split(input_file_path)
    file_base, file_ext = os.path.splitext(file_name)
    
    # 创建输出目录路径，输出到 data/esg_filtered_data
    base_dir = os.path.abspath(os.path.join(file_dir, "../esg_filtered_data"))
    
    # 如果输出目录不存在，创建它
    if not os.path.exists(base_dir):
        os.makedirs(base_dir)
    
    # 创建输出文件的路径，文件名加 `_filtered`
    output_file_path = os.path.join(base_dir, f"{file_base}_filtered{file_ext}")
    # 标准化路径
    output_file_path = os.path.normpath(output_file_path)
    return output_file_path


def Plot(data):
    #展示分数分布
    s = [i[0].get('score') for i in data]

    sns.kdeplot(s)
    plt.xlabel('numerical value')
    plt.title('Data distribution density map')
    plt.show()


def see_scores(results, thresholds):
    k = [0,0,0]
    for i in range(len(results)):
        if results[i][0].get('label') != 'None':
            #得分0.9以上个数
            if results[i][0].get('score') > thresholds:
                k[0] += 1
            #得分0.8以上个数
            if results[i][0].get('score') > 0.8:
                k[1] += 1
            #所有非None类句子个数
            k[2] += 1
    print(f'得分{thresholds}以上句子数{k[0]},得分{thresholds - 0.1}以上句子数{k[1]},非None类句子数{k[2]}')


def filter_txt(input_file_path, thresholds = 0.9, max = 510, view = False):
    ## thresholds设置所取置信分数阈值
    ## max设置每句话最大字符数
    ## plot设置是否查看分数分布图和分数相应保留句子个数
    
    
    try:
        finbert = BertForSequenceClassification.from_pretrained('yiyanghkust/finbert-esg',num_labels=4)
        tokenizer = BertTokenizer.from_pretrained('yiyanghkust/finbert-esg')
        # 检查是否有可用的 GPU
        device = 0 if torch.cuda.is_available() else -1

        nlp = pipeline("text-classification", model=finbert, tokenizer=tokenizer,device=device)
        
        # 创建输出文件的路径
        output_file_path = get_result_path(input_file_path)
        
        # 打开并读取整个文件
        with open(input_file_path, "r", encoding="utf-8") as file:
            text = file.readlines()
        
        results = []

        #设置最大文本长度
        max_text_length = max

        for t in text:
            t = t.strip()
            if len(t) > 512:
                result = nlp(t[:max_text_length])
            else:
                result = nlp(t)
            results.append(result)
        
        if view == True:
            see_scores(results, thresholds)
            Plot(results)
        
        r = []
        for i in range(len(results)):
            if results[i][0].get('label') != 'None' and results[i][0].get('score') > thresholds:
                r.append(text[i])
                
        # 打开文件进行写入
        with open(output_file_path, 'w', encoding='utf-8') as file:
            for sublist in r:
                # file.write(sublist + '\n')  # 添加换行符，方便段落间隔
                file.write(sublist) #不要换行符，方便操作
                
        print(f'文本已经成功写入 {output_file_path}')
        print(f'原文本共{len(text)}句话,处理后为{len(r)}句话')
    except Exception as e:
        print(f'发生错误: {e}')
        
# filter_txt("..\data\Courage Investment Group Limited_report.txt")