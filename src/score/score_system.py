import json
import os
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

# 定义 ESG 指标和权重
indicator_weights = {
    'ENV': {'GHG': 0.4, 'Energy': 0.3, 'Water': 0.2, 'Waste': 0.1},
    'SOC': {'Diversity': 0.4, 'Employment': 0.3, 'HealthSafety': 0.2, 'Training': 0.1},
    'GOV': {'BoardComposition': 0.3, 'ManagementDiversity': 0.3, 'Ethics': 0.2, 'Transparency': 0.1, 'Certifications': 0.1}
}

# ESG 维度权重
weights = {'E': 0.3, 'S': 0.3, 'G': 0.4}

positive_metrics = ['Diversity', 'Employment', 'Training', 'HealthSafety', 'BoardComposition', 'ManagementDiversity',
                    'Ethics', 'Certifications', 'Transparency']
negative_metrics = ['GHG', 'Waste', 'Water', 'Energy']

# 完整标签映射
replacement_dict = {
    "B-ENV_GHG_AET": "GHG", "I-ENV_GHG_AET": "GHG",
    "B-ENV_GHG_AE1": "GHG", "I-ENV_GHG_AE1": "GHG",
    "B-ENV_GHG_AE2": "GHG", "I-ENV_GHG_AE2": "GHG",
    "B-ENV_GHG_AE3": "GHG", "I-ENV_GHG_AE3": "GHG",
    "B-ENV_GHG_EIT": "GHG", "I-ENV_GHG_EIT": "GHG",
    "B-ENV_GHG_EI1": "GHG", "I-ENV_GHG_EI1": "GHG",
    "B-ENV_GHG_EI2": "GHG", "I-ENV_GHG_EI2": "GHG",
    "B-ENV_GHG_EI3": "GHG", "I-ENV_GHG_EI3": "GHG",
    "B-ENV_ENC_TEC": "Energy", "I-ENV_ENC_TEC": "Energy",
    "B-ENV_ENC_ECI": "Energy", "I-ENV_ENC_ECI": "Energy",
    "B-ENV_WAC_TWC": "Water", "I-ENV_WAC_TWC": "Water",
    "B-ENV_WAC_WCI": "Water", "I-ENV_WAC_WCI": "Water",
    "B-ENV_WAG_TWG": "Waste", "I-ENV_WAG_TWG": "Waste",
    "B-SOC_GED_CEG_M": "Diversity", "I-SOC_GED_CEG_M": "Diversity",
    "B-SOC_GED_CEG_F": "Diversity", "I-SOC_GED_CEG_F": "Diversity",
    "B-SOC_GED_NHG_M": "Diversity", "I-SOC_GED_NHG_M": "Diversity",
    "B-SOC_GED_NHG_F": "Diversity", "I-SOC_GED_NHG_F": "Diversity",
    "B-SOC_GED_ETG_M": "Diversity", "I-SOC_GED_ETG_M": "Diversity",
    "B-SOC_GED_ETG_F": "Diversity", "I-SOC_GED_ETG_F": "Diversity",
    "B-SOC_AGD_CEA_U30": "Employment", "I-SOC_AGD_CEA_U30": "Employment",
    "B-SOC_AGD_CEA_B35": "Employment", "I-SOC_AGD_CEA_B35": "Employment",
    "B-SOC_AGD_CEA_A50": "Employment", "I-SOC_AGD_CEA_A50": "Employment",
    "B-SOC_AGD_NHI_U30": "Employment", "I-SOC_AGD_NHI_U30": "Employment",
    "B-SOC_AGD_NHI_B35": "Employment", "I-SOC_AGD_NHI_B35": "Employment",
    "B-SOC_AGD_NHI_A50": "Employment", "I-SOC_AGD_NHI_A50": "Employment",
    "B-SOC_AGD_TOR_U30": "Employment", "I-SOC_AGD_TOR_U30": "Employment",
    "B-SOC_AGD_TOR_B35": "Employment", "I-SOC_AGD_TOR_B35": "Employment",
    "B-SOC_AGD_TOR_A50": "Employment", "I-SOC_AGD_TOR_A50": "Employment",
    "B-SOC-DEV-ATH-HNE-MAL" :"Training", "SGX-SOC-DEV-ATH-HNE-FEM": "Training",
    "B-SOC_DEV_ATH_M": "HealthSafety", "I-SOC_DEV_ATH_M": "HealthSafety",
    "B-SOC_DEV_ATH_F": "HealthSafety", "I-SOC_DEV_ATH_F": "HealthSafety",
    "B-SOC_OHS_FAT": "HealthSafety", "I-SOC_OHS_FAT": "HealthSafety",
    "B-SOC_OHS_HCI": "HealthSafety", "I-SOC_OHS_HCI": "HealthSafety",
    "B-SOC_OHS_REC": "HealthSafety", "I-SOC_OHS_REC": "HealthSafety",
    "B-SOC_OHS_RWI": "HealthSafety", "I-SOC_OHS_RWI": "HealthSafety",
    "B-GOV_BOC_BIN": "BoardComposition", "I-GOV_BOC_BIN": "BoardComposition",
    "B-GOV_BOC_WOB": "BoardComposition", "I-GOV_BOC_WOB": "BoardComposition",
    "B-GOV_MAD_WMT": "ManagementDiversity", "I-GOV_MAD_WMT": "ManagementDiversity",
    "B-GOV_ETB_ACD": "Ethics", "I-GOV_ETB_ACD": "Ethics",
    "B-GOV_ETB_ACT_N": "Ethics", "I-GOV_ETB_ACT_N": "Ethics",
    "B-GOV_ETB_ACT_P": "Ethics", "I-GOV_ETB_ACT_P": "Ethics",
    "B-GOV_CER_LRC": "Certifications", "I-GOV_CER_LRC": "Certifications",
    "B-GOV_ALF_AFD": "Transparency", "I-GOV_ALF_AFD": "Transparency",
    "B-GOV_ASS_ASR": "Certifications", "I-GOV_ASS_ASR": "Certifications"
}


# Define Letter Rating
def assign_rating(score):
    if score >= 8.571:
        return "AAA"
    elif score >= 7.143:
        return "AA"
    elif score >= 5.714:
        return "A"
    elif score >= 4.286:
        return "BBB"
    elif score >= 2.857:
        return "BB"
    elif score >= 1.429:
        return "B"
    else:
        return "CCC"

# 处理正向指标的区间评分
def positive_interval_score(value, average):
    if value >= 1.5 * average:
        return 10
    elif 1.2 * average <= value < 1.5 * average:
        return 9
    elif 1.0 * average <= value < 1.2 * average:
        return 7
    elif 0.8 * average <= value < 1.0 * average:
        return 5
    elif 0.6 * average <= value < 0.8 * average:
        return 3
    else:
        return 1

# 处理逆向指标的区间评分
def negative_interval_score(value, average):
    if value >= 1.5 * average:
        return 1
    elif 1.2 * average <= value < 1.5 * average:
        return 3
    elif 1.0 * average <= value < 1.2 * average:
        return 5
    elif 0.8 * average <= value < 1.0 * average:
        return 7
    elif 0.6 * average <= value < 0.8 * average:
        return 9
    else:
        return 10

# Extract numeric values, skip non-numeric entries
def extract_numeric_value(value_str):
    try:
        return float(value_str.replace(",", ""))  # Handle values with commas
    except (ValueError, TypeError):
        return 0.0  # Skip if value is not numeric
    
# 提取公司数据
def extract_company_data(company_data):
    esg_data = {'ENV': {}, 'SOC': {}, 'GOV': {}}
    for entry in company_data:
        question_id = entry['question_id']
        response = entry['response']
        value = extract_numeric_value(response.get('value', "0"))
        
        mapped_label = replacement_dict.get(question_id)
        if not mapped_label:
            continue
        
        if "ENV" in question_id:
            esg_data['ENV'][mapped_label] = esg_data['ENV'].get(mapped_label, 0) + value
        elif "SOC" in question_id:
            esg_data['SOC'][mapped_label] = esg_data['SOC'].get(mapped_label, 0) + value
        elif "GOV" in question_id:
            esg_data['GOV'][mapped_label] = esg_data['GOV'].get(mapped_label, 0) + value
    
    return esg_data

# Calculate Industry averages
def calculate_industry_averages(json_folder):
    aggregate_values = {'ENV': {}, 'SOC': {}, 'GOV': {}}
    count_values = {'ENV': {}, 'SOC': {}, 'GOV': {}}
    
    for filename in os.listdir(json_folder):
        if filename.endswith('.json'):
            file_path = os.path.join(json_folder, filename)
            with open(file_path, 'r') as f:
                json_data = json.load(f)
                for company_data in json_data.values():
                    esg_values = extract_company_data(company_data)
                    for dimension, metrics in esg_values.items():
                        for metric, value in metrics.items():
                            aggregate_values[dimension][metric] = aggregate_values[dimension].get(metric, 0) + value
                            count_values[dimension][metric] = count_values[dimension].get(metric, 0) + 1
    
    industry_averages = {
        dimension: {metric: (aggregate_values[dimension][metric] / count_values[dimension][metric]) 
                    for metric in metrics}
        for dimension, metrics in aggregate_values.items()
    }
    print(industry_averages)
    return industry_averages

# 计算详细分数
def calculate_detailed_scores(values, sub_weights, averages):
    dimension_score = 0
    detailed_scores = {}
    
    for metric, weight in sub_weights.items():
        value = values.get(metric, averages.get(metric, 0))
        average = averages.get(metric, value)
        
        if metric in positive_metrics:
            adjusted_score = positive_interval_score(value, average)
        elif metric in negative_metrics:
            adjusted_score = negative_interval_score(value, average)
        else:
            adjusted_score = positive_interval_score(value, average)
        
        metric_score = adjusted_score * weight
        dimension_score += metric_score
        detailed_scores[metric] = metric_score

    return dimension_score, detailed_scores

# 计算每家公司 ESG 分数
def calculate_esg_score(company_data, industry_averages):
    esg_values = extract_company_data(company_data)
    
    env_score, env_details = calculate_detailed_scores(esg_values.get('ENV', {}), indicator_weights['ENV'], industry_averages['ENV'])
    soc_score, soc_details = calculate_detailed_scores(esg_values.get('SOC', {}), indicator_weights['SOC'], industry_averages['SOC'])
    gov_score, gov_details = calculate_detailed_scores(esg_values.get('GOV', {}), indicator_weights['GOV'], industry_averages['GOV'])
    
    total_score = env_score * weights['E'] + soc_score * weights['S'] + gov_score * weights['G']
    
    return total_score, env_score, soc_score, gov_score, env_details, soc_details, gov_details

# 主函数：计算所有公司的 ESG 分数
def calculate_all_esg_scores(json_folder):
    industry_averages = calculate_industry_averages(json_folder)
    
    results = []
    for filename in os.listdir(json_folder):
        if filename.endswith('.json'):
            file_path = os.path.join(json_folder, filename)
            with open(file_path, 'r') as f:
                json_data = json.load(f)
                for company_name, company_data in json_data.items():
                    total_score, env_score, soc_score, gov_score, env_details, soc_details, gov_details = calculate_esg_score(company_data, industry_averages)
                    
                    result = {
                        'Company': company_name,
                        'Total ESG Score': total_score,
                        'ENV Score': env_score,
                        'SOC Score': soc_score,
                        'GOV Score': gov_score,
                        **{f'ENV_{k}': v for k, v in env_details.items()},
                        **{f'SOC_{k}': v for k, v in soc_details.items()},
                        **{f'GOV_{k}': v for k, v in gov_details.items()}
                    }
                    results.append(result)
    
    df = pd.DataFrame(results)
    scaler = MinMaxScaler(feature_range=(0, 10))
    df['Normalized Score'] = scaler.fit_transform(df[['Total ESG Score']])
    df['Letter Rating'] = df['Normalized Score'].apply(assign_rating)
    
    df.to_excel("esg_scores_detailed_with_ratings.xlsx", index=False)
    
    return df

# 执行主函数
json_folder_path = 'esg_json_file'
esg_scores_df = calculate_all_esg_scores(json_folder_path)
print(esg_scores_df)